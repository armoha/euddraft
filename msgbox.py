import sys
import ctypes

try:
    from winsound import MB_OK, MB_ICONHAND, MessageBeep

    def MessageBox(title, text, style=0):
        print("[%s]\n%s\n" % (title, text))

        """ Helper function """
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.SetForegroundWindow(hWnd)
        ctypes.windll.user32.BringWindowToTop(hWnd)
        ctypes.windll.user32.SetForegroundWindow(hWnd)
        ctypes.windll.user32.MessageBoxW(0, text, title, style)

except ImportError:
    MB_OK = 1
    MB_ICONHAND = 2

    def MessageBeep(type):
        for _ in range(type):
            sys.stdout.write("\a")

    def MessageBox(title, text, style=0):
        print("[%s]\n%s\n" % (title, text))
