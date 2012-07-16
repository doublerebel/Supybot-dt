###
# Copyright 2012 doublerebel
# Licensed WTFPL
###

import supybot.conf as conf
import supybot.registry as registry
import os
#The plugin name will be based on the plugin's folder.
PluginName = os.path.dirname( __file__ ).split(os.sep)[-1]

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    dtBot = conf.registerPlugin(PluginName, True)
    
    if yn("""The Digital-Tunes plugin rocks.  Would you like these commands to
             be enabled for everyone?""", default = False):
        dtBot.userLevelRequires.setValue("")
    else:
        cap = something("""What capability would you like to require for
                           this command to be used?""", default = "Admin")
        dtBot.userLevelRequires.setValue(cap)
    
    # 905872135d3b762556484e3256bdf17aa2ddcba0
    apiKey = something("""Digital-Tunes requires an API key to access their API.
                          If you don't have one, sign up at:
                          http://www.digital-tunes.net/affiliates/new""", default = False)
    dtBot.apiKey.setValue(apiKey)

    perPage = something("""How many results would you like returned per search?
                           """, default = 5)
    dtBot.numResults.setValue(perPage)
    

P = conf.registerPlugin(PluginName)
P.__name__ = PluginName

# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(PluginName, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))

conf.registerGlobalValue(P, 'userLevelRequires',
    registry.String('', """Determines the capability required to access the
                           commands in this plugin."""))

conf.registerGlobalValue(P, 'apiKey',
    registry.String('', """Key for accessing Digital-Tunes.net API."""))

conf.registerGlobalValue(P, 'numResults',
    registry.PositiveInteger(5, """Determines the number of search results returned."""))