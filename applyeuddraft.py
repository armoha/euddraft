import eudplib as ep
import traceback
import sys
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


def isEpExc(s):
    return (
        s.startswith('  File "C:\\gitclones\\euddraft\\') or
        s.startswith('  File "C:\\Python34\\lib\\site-packages\\eudplib')
    )


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
        exc_type, exc_value, exc_traceback = sys.exc_info()
        excs = traceback.format_exception(exc_type, exc_value, exc_traceback)
        in_eudplib_code = False
        formatted_excs = []


        for i, exc in enumerate(excs):
            if isEpExc(exc) and not all(isEpExc(e) for e in excs[i + 1:]):
                if in_eudplib_code:
                    continue
                in_eudplib_code = True
                exc = '<euddraft/eudplib internal code> \n'
            else:
                in_eudplib_code = False
            formatted_excs.append(exc)

        MessageBox("[Error] %s" % e, ''.join(formatted_excs))
