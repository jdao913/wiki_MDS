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
    end

    parsed_args = parse_args(ARGS, s)

    filename = parsed_args["filename"]
    outfile = parsed_args["outfile"]
    outfile = string("./miner/parsedArticles/", outfile)

    file = CSV.read(filename, nullable=false);
    println("Size of file: ", size(file))
    artNames = file[1]          #Article names
    numArt = size(artNames)[1]
    artWords = Array(file[2:end])      #List of words in articles
    data = Array(file[:, 2:end]);
    numWords = 30000
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