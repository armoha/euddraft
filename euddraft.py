import sys
import os
import winsound as ws
import time
import ctypes


from pluginLoader import loadPluginsFromConfig
from applyeuddraft import applyEUDDraft
from readconfig import readconfig


def MessageBox(title, text, style=0):
    """ Helper function """
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.SetForegroundWindow(hWnd)
    ctypes.windll.user32.BringWindowToTop(hWnd)
    ctypes.windll.user32.SetForegroundWindow(hWnd)
    ctypes.windll.user32.MessageBoxW(0, text, title, style)



# Intro!
print("euddraft v0.3 : Simple eudplib plugin system")

if len(sys.argv) != 2:
    raise RuntimeError("Usage : euddraft [setting file]")


# Chdir
sfname = sys.argv[1]
oldpath = os.getcwd()
dirname, sfname = os.path.split(sfname)
if dirname:
    os.chdir(dirname)


# Use simple setting system
if sfname[-4:] == '.eds':
    print(' - Running euddraft in compile mode')
    try:
        config = readconfig(sfname)
        mainSection = config['main']
        ifname = mainSection['input']
        ofname = mainSection['output']
        if ifname == ofname:
            raise RuntimeError('input and output file should be different.')

        print('---------- Loading plugins... ----------')
        pluginList, pluginFuncDict = loadPluginsFromConfig(config)

        print('--------- Injecting plugins... ---------')
        applyEUDDraft(ifname, ofname, pluginList, pluginFuncDict)

    except Exception as e:
        print("==========================================")
        print("[Error] %s" % e)
        input()


# Use daemon system
elif sfname[-4:] == '.edd':
    print(' - Running euddraft in daemon mode')
    config_mttime = None
    input_mttime = None
    ifname = None

    def checkNeedUpdate(old_mttime, fname):
        try:
            new_mttime = os.path.getmtime(fname)
        except OSError:
            new_mttime = None

        return old_mttime != new_mttime


    while True:
        needUpdate = False

        # Check if any of file is updated
        if checkNeedUpdate(config_mttime, sfname):
            needUpdate = True

        elif ifname:
            if checkNeedUpdate(input_mttime, ifname):
                needUpdate = True

        if needUpdate:
            print("\n\n[[Updating on %s]]" % time.strftime("%Y-%m-%d %H:%M:%S"))
            try:
                try:
                    config = readconfig(sfname)
                except OSError as e:
                    config_mttime = None
                    raise

                ifname = config['main']['input']
                ofname = config['main']['output']

                try:
                    config_mttime = os.path.getmtime(sfname)
                except OSError:
                    config_mttime = None
                    raise

                try:
                    input_mttime = os.path.getmtime(ifname)
                except OSError:
                    input_mttime = None
                    raise

                print('---------- Loading plugins... ----------')
                pluginList, pluginFuncDict = loadPluginsFromConfig(config)
                print('--------- Injecting plugins... ---------')
                applyEUDDraft(ifname, ofname, pluginList, pluginFuncDict)

                ws.MessageBeep(ws.MB_OK)

            except Exception as e:
                print("[Error] %s" % e)
                ws.MessageBeep(ws.MB_ICONHAND)
                MessageBox('Error', str(e))

        time.sleep(1)


# else
else:
    print("Invalid extension %s" % os.path.splitext(sfname)[1])

os.chdir(os.getcwd())
