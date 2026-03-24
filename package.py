'''
    organize all editable fields to top
    add argparse and format as script:
    if __name__ == '__main__'
    be verbose:
    - using blacklist...
    - excluding xx...
'''
import os
import sys
from hybrid_shell.hs import time_stamp

mode = 'blacklist'
app_dir = None
if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.realpath(__file__))

os.chdir(app_dir)
itemz = []

blacklist = ['lib', 'lib64', 'include', 'bin']
if mode == 'whitelist':
    itemz.append('"{}"'.format(
        os.path.join(app_dir, 'templates'))
)

for i in os.listdir(app_dir):
    if os.path.isfile(i):
        file = '"{}"'.format(os.path.join(app_dir, i))
        itemz.append(file)
    elif os.path.isdir(i) and mode == 'blacklist':
        if not i in blacklist:
            itemz.append('"{}"'.format(
                os.path.join(app_dir, i))
            )



name = time_stamp(True)
cmd = '7z a {} {}'.format(name, ' '.join(itemz))
print(cmd)
print('\n\n\n\n')
os.system(cmd)
