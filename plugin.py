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
            if genre == 'drum & bass' or genre == 'drum and bass' or genre == 'dnb':
                genre = 'drum_and_bass'
            searchurl += '/by_genre/' + genre
        searchurl += '/search'
        headers = utils.web.defaultHeaders

        # Construct a URL like:
        # http://api.digital-tunes.net/tracks/by_genre/trance?key=fdee51fc1927dcc86093ga51efbdef63cbf5d&term=monkey&count=10
        
        opts['term'] = searchTerms
        opts['key'] = self.registryValue('apiKey')
        numResults = self.registryValue('numResults')
        if numResults < 10:
            opts['count'] = 10
        else:
            opts['count'] = numResults
        
        print '%s?%s' % (searchurl, urllib.urlencode(opts))

        fd = utils.web.getUrlFd('%s?%s' % (searchurl,
                                           urllib.urlencode(opts)),
                                           headers)
        xml = simplexml.parse(fd)
        fd.close()

        if not xml:
            irc.reply('Receiving XML response from Digital-Tunes.net servers failed.')
        else:
            out = []
            for i in range(numResults):
                track = xml.track[i]
                title = str(track.artists.artist) + ' - ' + str(track.name)
                url = str(track.release.url)
                out.append('%s %s' % (title, url))
        if out:
            irc.reply(' | '.join(out))
        else:
            irc.reply('No results for the Digital-Tunes.net search: ' + ' '.join(things))
    dt = wrap(dt, [many('anything')])


_Plugin.__name__ = PluginName
Class = _Plugin
