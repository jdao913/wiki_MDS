# wiki_MDS

Repository to run Multidimensional Scaling (MDS) on a dataset of Wikipedia articles

# Setup Instructions

## Julia
This package relies on 'Julia', which can be downloaded [here] (https://julialang.org/downloads/).
This should install to your Applications folder. To be able to run Julia from the command line, add the binary directory to your PATH, e.g add:
'''
export PATH="/Applications/Julia-0.6.app/Contents/Resources/julia/bin:$PATH
'''
to your '.bashrc' or '.bash_profile' file.
You can also symlink the julia executable into a directory that is already on your PATH instead, e.g:
'''
sudo ln -s /Applications/Julia-0.6.app/Contents/Resources/julia/bin/julia /usr/local/bin/julia
'''

## Julia Packages
The Julia packages 'CSV' and 'MultivariateStats' are also needed. These can be installed by calling 'Pkg.add('CSV')' and Pkg.add('MultivariateStats') in the julia command line, i.e:
'''
$ julia
julia> Pkg.add('CSV')
julia> Pkg.add('MultivariateStats)
'''

# Usage Example
The following will run MDS on the file 'test.csv' onto 2 dimensions.
'''
$ julia runMDS.jl -f test.csv -d 2
'''