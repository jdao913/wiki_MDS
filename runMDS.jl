using ArgParse
using CSV
using MultivariateStats

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
        "--dimensions", "-d"
            help = "Number of dimensions to project down to (2 or 3)"
            arg_type = Int
            default = 2
        "--common", "-c"
            help = "Input file name of common words to take out."
            arg_type = String
            default = nothing
    end

    println("get args")
    parsed_args = parse_args(ARGS, s)
    filename = parsed_args["filename"]
    dim = parsed_args["dimensions"]
    common = parsed_args["common"]
    println("set args")

    file = CSV.read(filename, nullable=false)
    global names = file[1]          #Article names
    global words = names(file)[2:end]      #List of words in articles
    data = Array(file[:, 2:end])
    global commonWords = []
    if common != nothing
        commonfile = open(common)
        words = readlines(commonfile)
        global commonWords = split(words[1], ",")
        takeOut = intersect(words, commonWords)
        for i = 1:size(words)
            if any(x->x==words[i], takeOut)
                data[:,i] = 0           #Set all common word occurances to 0
            end
        end
    end
    
    D = getDist(data, common)      #Chop off article names and pass to dist func

    mds = classical_mds(D, dim)
    println(names)
    println(D)
    println(mds)
    println("Success")
    println(parsed_args["filename"])
end

main()