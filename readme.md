# Huh?
This is a simple script written in Python to compress images. Often, images aren't as small as they could be. 

Smooshy.py solves this problem by allowing you to compress all of those nasty extra bytes away without all the usual confusion surrounding fiddling around in the Save for Web Photoshop dialog.

# How?
In fact, Smooshy.py is basically just a script which takes advantage of the awesome http://smush.it/ -- all your images are sent for compression over to smush.it -- so be careful you don't send something you want to keep ultra-private :0

# Usage
1. `cd` into a directory of your choosing
2. `git clone git@github.com:obeattie/smooshy-py.git smooshy`
3. `cd` into a directory whose contents you'd like to compress
4. `python <directory of your choosing>/smooshy/smoosher.py`
5. Watch the magic happen.

You can also use smoosher.py on a file instead of a directory, or another directory instead of the present working directory. Simply pass the -s argumemt to smoosher.py and it'll love that file/directory instead :)

## Dependencies
* simplejson (http://pypi.python.org/pypi/simplejson/)
* Python 2.5
