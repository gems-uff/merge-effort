# Merge Effort

This script aims to analyze the effort of merge in open source projects. In this regard, it calculates three metrics: the wasted effort, the additional effort, and also the rework of parents. Moreover, it also returns the total number of actions of each parent (branch 1 and branch 2) and the total number of actions added in the merge.
## Getting Started

### Prerequisites

This project requires python, pygit2 and libgit2, and it was tested on the following versions:

```
python==3.6
pygit2==0.27.0
libgit2==0.27.0
```

First of all, if you are using Mac OS or Linux you need to install libgit2.

On Mac OS you can install libgit2 using homebrew:

```
$ brew install libgit2
```

On Linux you can install the latest version of libgit2 doing:


```
$ wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
$ tar xzf v0.27.0.tar.gz
$ cd libgit2-0.27.0/
$ cmake .
$ make
$ sudo make install
$ sudo ldconfig
```

For more information http://www.pygit2.org/install.html

Finally, after cloning our repository

```
$ git clone git@github.com:gems-uff/merge-effort.git
```

you can install all requirements running: 

```
$ pip install -r requirements.txt
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


* Tayane Silva Fernandes de Moura (UFF, Brazil)
* Leonardo Gresta Paulino Murta (UFF, Brazil)


## License

Copyright (c) 2018 Universidade Federal Fluminense (UFF)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
