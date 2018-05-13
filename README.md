# Merge Effort

This script aims to analyze the effort of merge in open source projects. In this regard, it calculates four metrics: the wasted effort, the additional effort, the no effort and also the rework of parents.

## Getting Started

### Prerequisites

This project requires

```
python
pygit2
libgit2
```

On Mac OS X you can install libgit2 using homebrew and then you can use pip to install pygit2.

```
$ brew install libgit2
$ pip install pygit2
```

Or you can install pygit2 through requirements.txt

```
$ brew install libgit2
$ pip install -r requirements.txt
```


On Windows 

```
$ pip install pygit2
```

Or you can install it through requirements.txt

```
$ pip install -r requirements.txt
```


On Linux you can install the latest version of libgit2 doing:


```
$ wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
$ tar xzf v0.27.0.tar.gz
$ cd libgit2-0.27.0/
$ cmake .
$ make
$ sudo make install
```

and then install pygit2 using pip 

```
$ pip install pygit2
```


For more information http://www.pygit2.org/install.html

### Installing

To install you just need to clone the repository:

```
$ git clone git@github.com:gems-uff/merge-effort.git

```


## Basic Usage

To run the script with a local repository:

```
python merge_analysis.py --local [path]

```

or you can run it passing a git url:

```
python merge_analysis.py --url [git_url]

```

By defaul the script will analyze all merge commits in the repository, but you can pass one or more commits using their hash

```
python merge_analysis.py --url [git_url] --commit [commit1 commit2]

```


## Team


Tayane Silva Fernandes de Moura (UFF, Brazil)
Leonardo Gresta Paulino Murta (UFF, Brazil)


## License

Copyright (c) 2018 Universidade Federal Fluminense (UFF)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
