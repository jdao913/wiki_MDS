using ArgParse
using CSV
using MultivariateStats
using JLD
using DataFrames

function occurDiff(article1, article2)::Float64
    return norm(article1 / sum(article1) - article2 / sum(article2))
end

function wordSim(article1, article2)::Float64
    total = [article1; article2]
    sameWords = minimum(total, 2)
    return 1 / sum(sameWords)
end


function getDist(data::Array{Int64, 2})::Array{Float64, 2}
    numData = size(data)[1]
    dists = Array{Float64}(numData, numData)
    for i = 1:numData
        for j = i:numData
            dist = occurDiff(data[i, :], data[j, :])
            dists[i, j] = dist
            dists[j, i] = dist
        end
    end
    return dists
end

function mdsDists(data::Array{Float64, 2})
    numData = size(data)[2]
    dists = Array{Float64}(numData, numData)
    for i = 1:numData
        for j = i:numData
            dist = norm(data[:, i] - data[:, j])
            dists[i, j] = dist
            dists[j, i] = dist
        end
    end
    return dists
end

function goodFit(trueDists::Array{Float64, 2}, mdsDists::Array{Float64, 2})
    diff = sum((trueDists - mdsDists).^2)
    stress = diff / (sum(trueDists.^2)) 
    return sqrt(stress)
end


function main()
    s = ArgParseSettings()
    @add_arg_table s begin
        "--filename", "-f"
            help = "Input file name. Must be in csv format"
            arg_type = String
            required = true
        "--outfile", "-o"
            help = "Output file name. Should be a csv. Saves to mdsFiles dir."
            arg_type = String
            default = "out.csv"
        "--dimensions", "-d"
            help = "Number of dimensions to project down to (2 or 3)"
            arg_type = Int
            default = 2
        "--common", "-c"
            help = "Input file name of common words to take out. If not given, no words are taken out."
            arg_type = String
            default = nothing
    end

    parsed_args = parse_args(ARGS, s)
    filename = parsed_args["filename"]
    outfile = parsed_args["outfile"]
    outfile = string("./mdsFiles/", outfile)
    dim = parsed_args["dimensions"]
    common = parsed_args["common"]

    if filename[end-3:end] == ".jld"
        d = load(filename)
        artNames = d["names"]
        data = d["data"]
        numArt = size(artNames)[1]
        if common != nothing
            artWords = d["words"]
            commonfile = open(common)
            words = readlines(commonfile)
            commonWords = split(words[1], ",")
            takeOut = intersect(artWords, commonWords)
            println("size", size(commonWords))
            for i = 1:size(commonWords)[1]
                if any(x->x==words[i], takeOut)
                    data[:,i] = 0           #Set all common word occurances to 0
                end
            end
        end
    else
        file = CSV.read(filename, nullable=false);
        artNames = file[1]          #Article names
        numArt = size(artNames)[1]
        artWords = Array(file[2:end])      #List of words in articles
        data = Array(file[:, 2:end]);
        commonWords = []
        println("size of file", size(data))
        #Remove common words
        if common != nothing
            commonfile = open(common)
            words = readlines(commonfile)
            commonWords = split(words[1], ",")
            takeOut = intersect(artWords, commonWords)
            for i = 1:size(commonWords)[1]
                if any(x->x==artWords[i], takeOut)
                    data[:,i] = 0           #Set all common word occurances to 0
                end
            end
            save("./miner/parsedArticles/"*basename(filename)[1:end-4]*"noCommon.jld", "names", artNames, "data", data, "words", artWords)
        else
            save("./miner/parsedArticles/"*basename(filename)[1:end-4]*".jld", "names", artNames, "data", data, "words", artWords)
        end
    end

    D = getDist(data)      #Chop off article names and pass to dist func
    println("D shape: ", size(D))
    mds = classical_mds(D, dim)
    mdsDist = mdsDists(mds)
    println("mds shape: ", size(mdsDist))
    println("Goodness of fit: ", goodFit(D, mdsDist))

    if dim == 1
        mean = sum(data.*[i for i=1:size(data)[2]]', 2)
        mean = mean ./ sum(data, 2)
        CSV.write(outfile[1:end-4]*"Mean.csv", DataFrame(mean'))
    end

    output = DataFrame(mds)
    newNames = [Symbol(artNames[i][1:end-16]) for i in 1:numArt]        #Chop off " - Wikipedia.txt"
    names!(output, newNames)
    CSV.write(outfile, output)
    println("Success")
end

println("Start")
main()