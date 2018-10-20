import os
import shutil

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
                print(e)
