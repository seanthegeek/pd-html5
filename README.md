pd-html5
========

A proof of concept mobile web interface to a Pure Data patch.

License
-------

>Copyright (C) 2012 Sean Whalen

>Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Background
----------

This project was created in response to a college assignment. The goal was to create an informative visualization of audio. I created a simple music player in Pure Data (Pd) that allowed a user to see the changes to a waveform that occur when volume and reverberation are manipulated. An assignment from another course required that I learn how to integrate Pure Data with other software. I had a personal interest in web development, so I decided to make a mobile web interface to the music player. Any device with a network connection and modern web browser can act as a remote controller without any additional software.

This is the first web application and Pd patch that I have written. As a result, the project is unlikely to be a good representation of best practices. However, I do hope that it will demonstrate the usefulness of combining various open source platforms.

Architecture
--------------- 

jQuery Mobile generates the mobile (and developer) friendly web interface. When a user interacts with one of the UI elements, a jQuery JavaScript event is triggered, and the request is passed to the web server. The web client also continually polls for changes in the music player's current controls every five seconds, and responds accordingly. As a result, multiple clients are able to view and control the music player settings at the same time. The ability of web applications to make and respond to requests is known as AJAX. Jquery and jQuery Mobile are included in the distribution of this project so that it may be used in an environment without an internet connection.

CherryPy is a Python micro-framework for web development. It serves the HTM 5 client to the user agents (web browsers), and responds to their requests. If the user agent has requested a music player change, the request is passed along by the web server to Pd via a local TCP connection on port 3000. 

Pure Data is a software package that enables the processing and manipulation of audio and video.  Pd provides a “netreceive” object for receiving specially formatted messages over a TCP socket. The patch (program) can then parse the message and pass the data to other parts of the patch. pd.py is a Python module that implements a complimenting TCP client class.

The server has been successfully tested on Windows, Ubuntu Linux, and Mac OS X. The web client should work on a [variety of web browsers](http://jquerymobile.com/demos/1.1.0/docs/about/platforms.html).

Dependencies
-----------------

- [Pd-extended](http://puredata.info/downloads/pd-extended/)
- [Python 2.x](http://www.python.org/download/) (Not Python >= 3)
- [CherryPy](http://www.cherrypy.org/)
- [jQuery](http://jquery.com/) (included)
- [jQuery Mobile] (http://jquerymobile.com/) (included)
- WAV and/or AIFF files to play

Setup
-------

1. Install Pd-extended
2. Install Python 2.x (Mac OS X and most Linux distributions already have this)
3. Install CherryPy. Windows users can use the installer. All platforms can use [pip](http://www.pip-installer.org/) or [easy_install](http://pypi.python.org/pypi/setuptools/).
4. Place WAV and/or AIFF files in the music directory. Note: WAV and AIFF are the only audio file types (that I know of) that work with the binary distribution of Pd-extended. Additional format support can be compiled from source, if desired.
5. Open the music-player.pd patch. A waveform graph will display.
6. Users on Mac OS X, Linux, or another UNIX-like system need to mark the webserver.py file executable. Then they can run it by issuing ./webserver.py from within in the project directory. Windows users simply need to double click on webserver.py.

No output will be generated in the console while the server is running. See the logs directory for web server output. The web listens on any address at port 8080 by default (e.g. http://127.0.0.1:8080). If you would like to change this, you can edit webserver.conf. Any web browser on the same network and sub-net should be able to access the web interface, unless something (e.g. a firewall) is blocking it. If the server fails to start, ensure the pd patch is open first, and then try again.