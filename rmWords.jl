using CSV
using JLD
using ArgParse

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
            default = "out.jld"
        "--common", "-c"
            help = "Input file name of common words to take out. If not given, no words are taken out."
            arg_type = String
            default = nothing
    end

    parsed_args = parse_args(ARGS, s)

    filename = parsed_args["filename"]
    outfile = parsed_args["outfile"]
    outfile = string("./miner/parsedArticles/", outfile)
    common = parsed_args["common"]
    

    file = CSV.read(filename, nullable=false);
    println("Size of file: ", size(file))
    artNames = file[1]          #Article names
    numArt = size(artNames)[1]
    artWords = Array(file[2:end])      #List of words in articles
    data = Array(file[:, 2:end]);
    numWords = 20000

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
    end

    totalWords = sum(data, 1)
    println("data: ", size(data))
    println("totalWords: ", size(totalWords), typeof(totalWords))

    newData = Array{Int64, 2}(numArt, numWords)
    println("newData", size(newData))
    for i = 1:numWords
        (val, ind) = findmax(totalWords)
        newData[:, i] = data[:, ind]
        totalWords[ind] = 0
    end
    save(outfile, "names", artNames, "data", newData, "words", artWords)
end

main()