import sys

log_file = r'C:\TEMP\ANTIGRAVITIY_ROLANDS_SCRIPTS\SE02_Controller\vst_log.txt'
with open(log_file, 'r') as f:
    content = f.read()

dumps = content.split('--- NEW SYSEX READ ---')
if len(dumps) >= 2:
    dump = dumps[-1].strip().split('\n')
    for l in dump:
        if 'Index 2' in l or 'Index 3' in l or 'Index 4' in l:
            if 'mapped' not in l:
                print(l)
