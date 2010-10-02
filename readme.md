# Huh?
This is a simple script written in Python to compress images. Often, images aren't as small as they could be. 

Smooshy.py solves this problem by allowing you to compress all of those nasty extra bytes away without all the usual confusion surrounding fiddling around in the Save for Web Photoshop dialog.

# How?
In fact, Smooshy is basically just a script which takes advantage of the awesome [smush.it](http://smush.it/) -- all your images are sent for compression over to smush.it -- so [be careful you don't send something you want to keep ultra-private](http://smush.it/faq.php).

## It's all safe
Smooshy creates backups of all your files while it's sprinkling its pixie dust over your images. If something goes wrong, your originals won't disappear into a black hole.

Also, if the resulting smooshed file is no smaller than the original, it won't be used.

# Usage
## Current Directory
1. `cd <directory of your choice>`
2. `smooshy .`
3. Watch the magic.

## Specific files/directories
1. `smooshy <as many files or directories as you'd like to smush here>`
2. Watch the magic.

## Pythonic
Of course, you can always use the classes and functions directly (I do this as part of a deployment script):

    >>> from smooshy import smoosher
    >>> smoosher.Smoosher(<file path).smoosh()
    ... # Smooshes the file
    >>> smoosher.recursive_smoosher([<file or directory>... ])
    ... # Smooshes all files / all files recursively in directories

# Installation
1. `git clone git@github.com:obeattie/smooshy-py.git smooshy`
2. `cd smooshy`
3. `python setup.py install`

## Dependencies
* [simplejson](http://pypi.python.org/pypi/simplejson/)
* [Python 2.5](http://www.python.org/download/releases/2.5/) or above (probably not Python 3, though)

# Credit where credit's due…
This script is essentially a Python port of [smusher](http://github.com/grosser/smusher/tree/master) -- I'm a Python guy so I hope you'll forgive me for making my own version :)

* * *

As with [smusher](http://github.com/grosser/smusher/tree/master), consider this code in the public domain, do whatever the hell you want with it (fork away :) but don't blame me for any mess caused by it.
