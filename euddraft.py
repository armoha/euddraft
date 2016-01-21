import eudplib as ep
import runpy as rp
import sys
import os
import json


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


# Load input json file

if len(sys.argv) != 2:
    print("Usage : euddraft [setting file]")
    input()
    sys.exit(1)

sfname = sys.argv[1]
settings = json.load(open(sfname, 'r'))

ifname = settings['input']
ofname = settings['output']
if ifname == ofname:
    print('input and output should be different')
    input()
    sys.exit(2)

pluginSettingList = settings['plugins']


# Load plugins

print('---------- Loading plugins... ----------')

pluginList = {}


for pluginSetting in pluginSettingList:
    if isinstance(pluginSetting, str):
        pluginName = pluginSetting
        pluginArgs = {}

    else:
        pluginName = pluginSetting['pluginName']
        pluginArgs = pluginSetting.get('args', {})

    print('Loading plugin %s...' % pluginName)

    try:
        pluginPath = os.path.join(basepath, 'plugins', '%s.py' % pluginName)
        pluginDict = rp.run_path(pluginPath, pluginArgs, pluginName)

        if pluginDict:
            onPluginStart = pluginDict.get('onPluginStart', empty)
            beforeTriggerExec = pluginDict.get('beforeTriggerExec', empty)
            afterTriggerExec = pluginDict.get('afterTriggerExec', empty)
            pluginList[pluginName] = (
                onPluginStart,
                beforeTriggerExec,
                afterTriggerExec
            )

    except Exception as e:
        print('Error on loading plugin %s : %s' % (pluginName, e.__repr__()))


# Create main function


@ep.EUDFunc
def main():
    # init plugins
    for pluginName, plugin in pluginList.items():
        onPluginStart = plugin[0]
        onPluginStart()

    # do trigger loop
    if ep.EUDInfLoop()():
        for pluginName, plugin in pluginList.items():
            beforeTriggerExec = plugin[1]
            beforeTriggerExec()

        # eudplib v0.50 has bug that RunTrigTrigger don't revert Current Player
        # after RunTrigTriger call. So we have to do it manually
        currentPlayer = ep.f_getcurpl()
        ep.RunTrigTrigger()
        ep.f_setcurpl(currentPlayer)

        for pluginName, plugin in reversed(pluginList.items()):
            afterTriggerExec = plugin[2]
            afterTriggerExec()

        ep.EUDDoEvents()

    ep.EUDEndInfLoop()

# Inject


print('--------- Injecting plugins... ---------')


ep.LoadMap(ifname)
ep.SaveMap(ofname, main)
