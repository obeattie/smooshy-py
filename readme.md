# Huh?
This is a simple script written in Python to compress images. Often, images aren't as small as they could be. 

Smooshy.py solves this problem by allowing you to compress all of those nasty extra bytes away without all the usual confusion surrounding fiddling around in the Save for Web Photoshop dialog.

# How?
In fact, Smooshy is basically just a script which takes advantage of the awesome [smush.it](http://smush.it/) -- all your images are sent for compression over to smush.it -- so [be careful you don't send something you want to keep ultra-private](http://smush.it/faq.php).

## It's all safe
Smooshy creates backups of all your files while it's sprinkling its pixie dust over your images. If something goes wrong, your originals won't disappear into a black hole.

Also, if the resulting smooshed file is no smaller than the original, it won't be used.

# Usage
1. `cd` into a directory of your choosing
2. run `git clone git@github.com:obeattie/smooshy-py.git smooshy`
3. `cd` into a directory whose contents you'd like to compress
4. run `python <directory of your choosing>/smooshy/smoosher.py`
5. Watch the magic happen.

You can also use smoosher.py on a file instead of a directory, or another directory instead of the present working directory. Simply pass the `-s` (or `--smoosh`) argumemt to smoosher.py and it'll love that file/directory instead =)

Finally, you can, of course use the functions and classes provided by smoosher.py directly. But you already knew that.

## Dependencies
* [simplejson](http://pypi.python.org/pypi/simplejson/)
* [Python 2.5](http://www.python.org/download/releases/2.5/) or above (probably not Python 3, though)

# Credit where credit's due…
This script is essentially a Python port of [smusher](http://github.com/grosser/smusher/tree/master) -- I'm a Python guy so I hope you'll forgive me for making my own version :)
