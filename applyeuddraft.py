import eudplib as ep
import traceback
from readconfig import readconfig
from pluginLoader import loadPluginsFromConfig
from msgbox import MessageBox, MessageBeep, MB_OK, MB_ICONHAND


def createPayloadMain(pluginList, pluginFuncDict):
    @ep.EUDFunc
    def payloadMain():
        """ Main function of euddraft payload """
        # init plugins
        for pluginName in pluginList:
            onPluginStart = pluginFuncDict[pluginName][0]
            onPluginStart()

        # Do trigger loop
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

    return payloadMain


def applyEUDDraft(sfname):
    try:
        config = readconfig(sfname)
        mainSection = config['main']
        ifname = mainSection['input']
        ofname = mainSection['output']
        if ifname == ofname:
            raise RuntimeError('input and output file should be different.')

        print('---------- Loading plugins... ----------')
        ep.LoadMap(ifname)
        pluginList, pluginFuncDict = loadPluginsFromConfig(config)

        print('--------- Injecting plugins... ---------')

        payloadMain = createPayloadMain(pluginList, pluginFuncDict)
        ep.CompressPayload(True)
        ep.SaveMap(ofname, payloadMain)
        MessageBeep(MB_OK)

    except Exception as e:
        print("==========================================")
        MessageBeep(MB_ICONHAND)
        MessageBox("[Error] %s" % e, traceback.format_exc())
