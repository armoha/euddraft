import eudplib as ep
import os

from readconfig import readconfig
from pluginLoader import loadPluginsFromConfig


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


def applyEUDDraft(ifname, ofname, pluginList, pluginFuncDict):
    payloadMain = createPayloadMain(pluginList, pluginFuncDict)
    ep.CompressPayload(True)
    ep.SaveMap(ofname, payloadMain)
