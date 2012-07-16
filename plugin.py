###
# Copyright 2012 doublerebel
# Licensed WTFPL
###

import os
import string
import urllib

import supybot.utils as utils
from supybot.commands import *
import supybot.callbacks as callbacks

import simplexml


# This will be used to change the name of the class to the folder name
PluginName = os.path.dirname(__file__).split(os.sep)[-1]


class _Plugin(callbacks.Plugin):

    """Usage: @dt <searchterms> genre: <genrename>"""
    threaded = True
    def dt(self, irc, msg, args, things):
        """ <searchterms> [genre:<genrename>]
        
        Displays results from Digital-Tunes.net .
        """
        opts = {}
        
        searchTerms = ' '.join(things)
        searchTerms = string.split(searchTerms,'genre:')
        if len(searchTerms) > 1:
            genre = searchTerms[1]
        else:
            genre = False
        searchTerms = searchTerms[0].strip()
        
        searchurl = 'http://api.digital-tunes.net/tracks'
        if genre:
            searchurl += '/by_genre/' + genre
        headers = utils.web.defaultHeaders

        # Construct a URL like:
        # http://api.digital-tunes.net/tracks/by_genre/trance?key=fdee51fc1927dcc86093ga51efbdef63cbf5d&term=monkey&count=10
        
        opts['term'] = searchTerms
        opts['key'] = self.registryValue('apiKey')
        opts['count'] = self.registryValue('numResults')
        
        fd = utils.web.getUrlFd('%s?%s' % (searchurl,
                                           urllib.urlencode(opts)),
                                           headers)
        xml = simplexml.parse(fd)
        fd.close()

        if not xml:
            irc.reply('Receiving XML response from Digital-Tunes.net servers failed.')
        else:
            for i in range(self.registryValue('numResults')):
                track = xml.tracks[i]
                title = track.artists.artist[0]
                title += track.name
                url = track.release.url
                out.append('%s %s' % (title, url))
        if out:
            irc.reply(' | '.join(out))
        else:
            irc.reply('No results for the Digital-Tunes.net search: ' + ' '.join(things))
    dt = wrap(dt, [many('anything')])


_Plugin.__name__ = PluginName
Class = _Plugin
