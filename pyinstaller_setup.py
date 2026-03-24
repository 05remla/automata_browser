import sys, os

# if getattr(sys, "frozen", False):
#     app_dir = os.path.dirname(sys.executable)
# else:
#     app_dir = os.path.dirname(os.path.realpath(__file__))
#
# sys.path.append(os.path.join(app_dir, 'lib/python3.12/pyInstaller-packages'))
import PyInstaller.__main__

DistBasePath     = '/home/leo/.pyvirtenvs/automata_browser2.0'
ProgramBuildPath = '/home/leo/.pyvirtenvs/automata_browser2.0'
programName      = 'automata_browser'

executionList = [
    '--name=automata_browser',
    '--clean']

executionList.append('{}/{}'.format(ProgramBuildPath, 'auto_browser.py'))
PyInstaller.__main__.run(executionList)
