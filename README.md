# wiki_MDS

Repository to run Multidimensional Scaling (MDS) on a dataset of Wikipedia articles

# Setup Instructions

## Julia
This package relies on **Julia**, which can be downloaded [here](https://julialang.org/downloads/).
This should install to your Applications folder. To be able to run Julia from the command line, add the binary directory to your PATH, e.g add:
```
export PATH="/Applications/Julia-0.6.app/Contents/Resources/julia/bin:$PATH
```
to your `.bashrc` or `.bash_profile` file.
You can also symlink the julia executable into a directory that is already on your PATH instead, e.g:
```
sudo ln -s /Applications/Julia-0.6.app/Contents/Resources/julia/bin/julia /usr/local/bin/julia
```

## Julia Packages
The Julia packages `CSV` and `MultivariateStats` are also needed. These can be installed by calling `Pkg.add('CSV')` and `Pkg.add('MultivariateStats')` in the julia command line, i.e:
```
$ julia
julia> Pkg.add('CSV')
julia> Pkg.add('MultivariateStats)
```

# Usage Example
The following will run MDS on the file 'test.csv' onto 2 dimensions.
```
$ julia runMDS.jl -f test.csv -d 2
```

# Usage Instructions
## Parsing Articles
In order to run MDS, you must first generate the CSV input file. To do this, use `parseWordsToCSV.py` in the `miner` folder.
This function takes in 2 arguments: 

1. The directory of article txt files (this is required)
2. An optional output CSV file name. Defaults to `articles.csv` The output CSV file will be saved in the parsedArticles directory.

Example: 
```
$ python3 parseWordsToCSV.py ./text_files/featured/ -o articles.csv
```
will parse all the articles in the `./text_files/featured/` directory and save the output CSV file as `articles.csv` in the parsedArticles directory.

### Running MDS
We can now run MDS on the parsed articles. To do this, use `runMDS.jl`, which takes in 4 arguments function:

1. Input filename. Called with `-f`. Should be the parsed articles CSV file.
2. Optional output filename. Called with `-o`. Defaults to `out.csv`. The name of the output CSV file containing the coordinates of each article.
Will be saved in the mdsFiles directory
3. The dimension to project the data down to. Called with `-d`. Defaults to 2 if no value is given. 
4. Input file for common words. Called with `-c`. Defaults to empty. The name of the CSV file containing the common words to take out.

Example:
```
$ julia runMDS.jl -f ./miner/parsedArticles/articles.csv -o `articleCoords.csv`
```
will run MDS on the `articles.csv` file and save the output coordinates to `mdsFiles/articleCoords.csv`

### Plotting the result
After running MDS, we can plot the resulting coordinates. To do this, use `plotMDS.py`, which takes a single argument:

1. Input filename. The filename of the MDS coordinates to plot.

Example:
```
$ python3 plotMDS.py  ./mdsFiles/articleCoords.csv
```
will plot the data in articleCoords.csv. 

The plot is interactive, and you can see the title of the plotted article by hovering over. While the plot can be saved as an image,
it will unfortunately not keep the interactivity. 

There are also 2 optional arguments:

1. -d, the dimension to plot too. Note that this dimension must match the dimension of the MDS output
2. -m, the mean file. This CSV file input contains the average word length for each article. Must be used with a word distribution MDS output.

Example:
```
$ python3 plotMDS.py ./mdsFiles/vitalDist10_1DCoords.csv -m ./mdsFiles/vitalDist10_1DCoordsMean.csv
```