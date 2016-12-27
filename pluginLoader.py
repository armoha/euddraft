#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

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


def getGlobalPluginDirectory():
    return os.path.join(basepath, 'plugins')


def getPluginPath(pluginName):
    if pluginName[-3:] == '.py':
        pluginPath = pluginName
    else:
        pluginPath = os.path.join(
            basepath, 'plugins', '%s.py' % pluginName)

    return pluginPath


def empty():
    pass


freeze_enabled = False


def isFreezeIssued():
    return freeze_enabled


def loadPluginsFromConfig(config):
    global freeze_enabled

    """ Load plugin from config file """
    pluginList = [name for name in config.keys() if name != 'main']
    pluginFuncDict = {}

    initialDirectory = os.getcwd()
    initialPath = sys.path[:]

    freeze_enabled = False

    for pluginName in pluginList:
        if pluginName == 'freeze':
            freeze_enabled = True
            print("""\
                          *                                         *
        *                                        *
                        [[ freeze activated ]]
                                  *                       *
                *                                                          *\
""")
            print("Freeze plugin loaded")
            continue

        pluginSettings = {'settings': config[pluginName]}

        print('Loading plugin %s...' % pluginName)

        # real python name
        pluginPath = getPluginPath(pluginName)

        try:
            pluginDir, _ = os.path.split(pluginPath)
            if pluginDir and pluginDir not in sys.path:
                sys.path.append(os.path.abspath(pluginDir))

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

        except Exception:
            raise RuntimeError('Error loading plugin "%s"' % pluginName)

        finally:
            os.chdir(initialDirectory)
            sys.path[:] = initialPath[:]

    if 'freeze' in pluginList:
        pluginList.remove('freeze')

    return pluginList, pluginFuncDict
