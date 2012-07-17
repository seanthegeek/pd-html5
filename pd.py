#!/usr/bin/env python
'''
pd - A simple interface to a custom PD protocol
Copyright (C) 2012 Sean Whalen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import socket


class Client(object):
    """
    A client for a custom Pure Data Extended (PD) protocol over TCP
    """
    def connect(self, address, port):
        """
        Connects the socket to the server
        @param address: The address of the server
        @param port: The port of the server, as an integer
        """
        self._socket.connect((address, port))

    def __init__(self, address, port):
        """
        Creates the socket, and connects it to the server
        @param address: The address of the server
        @param port: The port of the server, as an integer
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(address, port)

    def disconnect(self):
        """
        Closes the connection
        """
        self._socket.close()

    def _send(self, atoms):
        """
        Properly terminates the message, and sends it to the server
        @param atoms: The PD atoms to send, as a string
        """
        self._socket.send(atoms + ";\n")

    def play(self, filename):
        """
        Tells the server to play the given file
        Note: Spaces in the filename are automatically escaped
        @param filename: The filename of the file to play
        """
        self._send("play " + filename.replace(" ", "\ "))

    def pause(self):
        """
        Pauses or resumes audio playback
        """
        self._send("pause")

    def set_volume(self, volume):
        """
        Tells the server to set the volume (amplitude) to a given percentage
        @param volume: An integer between 0 and 100
        """
        if volume >= 0 and volume <= 100:
            self._send("set volume %d" % volume)
        else:
            raise ValueError("Volume must be between 0 and 100")

    def set_reverb(self, reverb):
        """
        Tells the server to set the reverberation to a given percentage
        @param volume: An integer between 0 and 100
        """
        if reverb >= 0 and reverb <= 100:
            self._send("set reverb %d" % reverb)
        else:
            raise ValueError("Reverb must be between 0 and 100")
