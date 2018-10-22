import os
import zipfile


def packageZip(buildDir, fname, version):
    """Package zip
    
    Arguments:
        buildDir {str} -- Build destination dir
        fname {str} -- Output .zip file
        version {str} -- Version of .zip file
    """
    oldDir = os.getcwd()
    with zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        os.chdir(buildDir)
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.startswith('.'):
                    continue
                zipf.write(os.path.join(root, file))
        zipf.writestr('VERSION', str(version))
        os.chdir(oldDir)
