import sys

log_file = r'C:\TEMP\ANTIGRAVITIY_ROLANDS_SCRIPTS\SE02_Controller\vst_log.txt'
with open(log_file, 'r') as f:
    content = f.read()

dumps = content.split('--- NEW SYSEX READ ---')
if len(dumps) >= 3:
    print("DUMP N-2")
    print("\n".join(dumps[-3].strip().split('\n')[:5]))
    print("DUMP N-1")
    print("\n".join(dumps[-2].strip().split('\n')[:5]))
    print("DUMP N")
    print("\n".join(dumps[-1].strip().split('\n')[:5]))
