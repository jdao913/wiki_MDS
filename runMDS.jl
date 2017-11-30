using ArgParse
using CSV
using MultivariateStats
using JLD
using DataFrames

function occurDiff(article1::Array{Int64}, article2::Array{Int64})::Float64
    return norm(article1 - article2)
end

function getDist(data::Array{Int64, 2})::Array{Float64, 2}
    numData = size(data)[1]
    dists = Array{Float64}(numData, numData)
    for i = 1:numData
        for j = i:numData
            dist = occurDiff(data[i,:], data[j,:])
            dists[i, j] = dist
            dists[j, i] = dist
        end
    end
    return dists
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
    else
        file = CSV.read(filename, nullable=false);
        artNames = file[1]          #Article names
        numArt = size(artNames)[1]
        artWords = Array(file[2:end])      #List of words in articles
        println("artWords", typeof(artWords))
        data = Array(file[:, 2:end]);
        commonWords = []
        println("size of file", size(data))
        #Remove common words
        if common != nothing
            commonfile = open(common)
            words = readlines(commonfile)
            commonWords = split(words[1], ",")
            takeOut = intersect(artWords, commonWords)
            for i = 1:size(words)
                if any(x->x==words[i], takeOut)
                    data[:,i] = 0           #Set all common word occurances to 0
                end
            end
            save("./miner/parsedArticles/"*filename[1:end-4]*"noCommon.jld", "names", artNames, "data", data, "words", words)
        else
            println(typeof(artNames))
            println(typeof(artWords))
            println(typeof(data))
            save("/tmp/"*filename[1:end-4]*".jld", "names", artNames, "data", data, "words", artWords)
        end
    end

    D = getDist(data)      #Chop off article names and pass to dist func
    mds = classical_mds(D, dim)
    output = DataFrame(mds)
    newNames = [Symbol(artNames[i][1:end-16]) for i in 1:numArt]        #Chop off " - Wikipedia.txt"
    names!(output, newNames)
    CSV.write(outfile, output)
    println("Success")
end

println("Start")
main()