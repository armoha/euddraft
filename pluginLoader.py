import os
import runpy as rp
import sys


# Get absolute path of current executable
if getattr(sys, 'frozen', False):
    # frozen
    basepath = os.path.dirname(sys.executable)
else:
    # unfrozen
    basepath = os.path.dirname(os.path.realpath(__file__))


def loadPluginsFromConfig(config):
    """ Load plugin from config file """
    pluginList = [name for name in config.keys() if name != 'main']
    pluginFuncDict = {}
    empty = lambda: None  # Do-nothing function

    for pluginName in pluginList:
        pluginSettings = {'settings': config[pluginName]}

        print('Loading plugin %s...' % pluginName)

        # real python name
        if pluginName[-3:] == '.py':
            pluginPath = pluginName
        else:
            pluginPath = os.path.join(
                basepath, 'plugins', '%s.py' % pluginName)

        try:
            pluginDict = rp.run_path(pluginPath, pluginSettings, pluginName)

            if pluginDict:
                onPluginStart = pluginDict.get('onPluginStart', empty)
                beforeTriggerExec = pluginDict.get('beforeTriggerExec', empty)
                afterTriggerExec = pluginDict.get('afterTriggerExec', empty)
                pluginFuncDict[pluginName] = (
                    onPluginStart,
                    beforeTriggerExec,
                    afterTriggerExec
                )

        except (KeyboardInterrupt, SystemExit):
            raise

        except Exception as e:
            raise RuntimeError('Error loading plugin "%s" : %s' % (pluginName, e))

    return pluginList, pluginFuncDict
