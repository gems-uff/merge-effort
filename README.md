# Merge Effort

This project aims at analyzing the merge effort of Git projects. In this regard, it calculates some metrics: 

* The number of actions (i.e., lines added or removed) in each branch
* The number of actions in the merge commit
* The rework: similar actions in both branches
* The wasted actions: actions in the branches that were not merged
* The additional actions: actions not in the branches that were added during the merge

## Getting Started

### Prerequisites

This project requires python, pygit2 and libgit2, and it was tested on the following versions:

```
python==3.6
pygit2==0.27.0
libgit2==0.27.0
```

First of all, if you are using Mac OS or Linux you need to install libgit2. If you have Anaconda installed in your computer, you can simple do:

```
$ conda install -c conda-forge libgit2
```

Otherwise, on Mac OS you can install libgit2 using homebrew:

```
$ brew install libgit2
```

On Linux you can install the latest version of libgit2 by doing:

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

### Installing

To install merge-effort you should do:

```
$ pip install merge-effort
```

## Basic Usage

To run the script with a local repository:

```
merge-effort --local [path]

```

or you can run it passing a git url:

```
merge-effort --url [git_url]

```

By defaul the script will analyze all merge commits in the repository, but you can pass one or more commits using their hash

```
merge-effort --url [git_url] --commit [commit1 commit2]

```

By default the script will retun the merge effort, but if you want to see the metrics normalized you can set --normalized

```
merge-effort --url [git_url] --normalized

```

## Team


* Tayane Silva Fernandes de Moura (UFF, Brazil)
* Leonardo Gresta Paulino Murta (UFF, Brazil)


## License

Copyright (c) 2018 Universidade Federal Fluminense (UFF)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
