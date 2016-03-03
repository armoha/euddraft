import eudplib as ep
import runpy as rp
import sys
import os
import traceback
import configparser

config = configparser.ConfigParser()

try:
    print("euddraft v0.02 : Simple eudplib plugin system")

    # Get absolute path of current executable
    if getattr(sys, 'frozen', False):
        # frozen
        basepath = os.path.dirname(sys.executable)
    else:
        # unfrozen
        basepath = os.path.dirname(os.path.realpath(__file__))

    # Needed for defaulting function
    def empty():
        pass

    # --------------------------------------
    # --------------------------------------
    # --------------------------------------

    # Load input setting file

    if len(sys.argv) != 2:
        print("Usage : euddraft [setting file]")
        input()
        sys.exit(1)

    sfname = sys.argv[1]

    dirname, filename = os.path.split(sfname)
    if dirname:
        os.chdir(dirname)

    if not config.read(filename):
        print('Cannot read setting file \"%s\".' % sfname)
        input()
        sys.exit(3)

    if 'main' not in config:
        print('Setting file doesn\'t have \"main\" section.')
        input()
        sys.exit(3)

    mainSection = config['main']
    ifname = mainSection['input']
    ofname = mainSection['output']
    if ifname == ofname:
        print('input and output should be different')
        input()
        sys.exit(2)

    # Load plugins

    print('---------- Loading plugins... ----------')

    pluginList = list(filter(lambda x: x != 'main', config.sections()))

    pluginFuncDict = {}
    loadedPluginList = []
    for pluginName in pluginList:
        if pluginName == 'main':  # Map settings -> pass
            pass

        pluginSettings = {
            'settings': config[pluginName]
        }

        print('Loading plugin %s...' % pluginName)

        try:
            # real python name
            if pluginName[-3:] == 'py':
                pluginPath = pluginName
            else:
                pluginPath = os.path.join(
                    basepath, 'plugins', '%s.py' % pluginName)

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

        except Exception as e:
            raise RuntimeError('Error on loading plugin \"%s\"' % pluginName)

    # Create main function

    @ep.EUDFunc
    def main():
        # init plugins
        for pluginName in pluginList:
            onPluginStart = pluginFuncDict[pluginName][0]
            onPluginStart()

        # do trigger loop
        if ep.EUDInfLoop()():
            for pluginName in pluginList:
                beforeTriggerExec = pluginFuncDict[pluginName][1]
                beforeTriggerExec()

            # eudplib v0.50 has bug that RunTrigTrigger don't revert Current
            # player after RunTrigTriger call, so we have to do it manually.
            currentPlayer = ep.f_getcurpl()
            ep.RunTrigTrigger()
            ep.f_setcurpl(currentPlayer)

            for pluginName in reversed(pluginList):
                afterTriggerExec = pluginFuncDict[pluginName][2]
                afterTriggerExec()

            ep.EUDDoEvents()

        ep.EUDEndInfLoop()

    # Inject

    print('--------- Injecting plugins... ---------')

    ep.LoadMap(ifname)
    ep.SaveMap(ofname, main)


except Exception as e:
    print("==========================================")
    print("==========================================")
    print("Exception occured while running euddraft.")

    traceback.print_exc()
    input()
