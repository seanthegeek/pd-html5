#!/usr/bin/env python
'''
webserver - Brings PD to the web
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
from os import listdir

import cherrypy

import pd


class Root(object):
    """
    The dynamic web root
    """
    @cherrypy.expose()
    def set_volume(self, value):
        """
        Sets the volume to the given percentage
        @param value: the volume percentage
        """
        value = int(value)
        if value >= 0 and value <= 100:
            self._volume = value
            self._pd.set_volume(self._volume)
        else:
            raise cherrypy._cperror.HTTPError(404)

    @cherrypy.expose()
    def set_reverb(self, value):
        """
        Sets the reverberation to the given percentage
        @param value: the reverberation percentage
        """
        value = int(value)
        if value >= 0 and value <= 100:
            self._reverb = value
            self._pd.set_reverb(self._reverb)
        else:
            raise cherrypy._cperror.HTTPError(404)

    @cherrypy.expose()
    def play(self, value):
        """
        Plays the selected track
        @param value: the index value from the list of tracks
        """
        value = int(value)
        if value >= 0 and value <= len(self._tracks) - 1:
            self._track = value
            self._pd.play(self._tracks[self._track])
        else:
            raise cherrypy._cperror.HTTPError(404)

    @cherrypy.expose()
    def pause(self):
        """
        Pauses or resumes music playback
        """
        self._pd.pause()

    def __init__(self):
        """
        Connects to PD and sets the initial values
        """
        self._pd = pd.Client("127.0.0.1", 3000)
        self._track = 0
        self.set_volume(30)
        self.set_reverb(0)

        self._tracks = sorted(listdir("music"))
        for track in self._tracks:
            if track.startswith("."):
                self._tracks.remove(track)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_tracks(self):
        """
        Returns a JSON list of tracks
        """
        return self._tracks

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_status(self):
        """
        Returns JSON pairs containing current values
        """
        return {"track": self._track,
                "volume": self._volume,
                "reverb": self._reverb}

if __name__ == '__main__':
    cherrypy.quickstart(Root(), config="webserver.conf")
