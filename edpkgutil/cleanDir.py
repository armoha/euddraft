import os
import shutil
import sys


def cleanDirectory(directory):
    if os.path.exists(directory):
        for the_file in os.listdir(directory):
            fpath = os.path.join(directory, the_file)
            try:
                if os.path.isfile(fpath):
                    os.unlink(fpath)
                elif os.path.isdir(fpath):
                    shutil.rmtree(fpath)
            except Exception as e:
                print(e, file=sys.stderr)


def cleanOutput(directory):
    for the_file in os.listdir(directory):
        path = os.path.splitext(the_file)
        try:
            if path[0].startswith("api-ms") and path[-1].endswith(".dll"):
                fpath = os.path.join(directory, the_file)
                newpath = os.path.join(directory, "lib", the_file)
                os.rename(fpath, newpath)
        except Exception as e:
            print(e, file=sys.stderr)
