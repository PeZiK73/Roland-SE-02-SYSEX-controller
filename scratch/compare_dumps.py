import sys

log_file = r'C:\TEMP\ANTIGRAVITIY_ROLANDS_SCRIPTS\SE02_Controller\vst_log.txt'
with open(log_file, 'r') as f:
    content = f.read()

dumps = content.split('--- NEW SYSEX READ ---')
if len(dumps) >= 3:
    dump1 = dumps[-2].strip().split('\n')
    dump2 = dumps[-1].strip().split('\n')
    
    print("Comparing last two dumps:")
    for l1, l2 in zip(dump1, dump2):
        if l1 != l2:
            print("DIFFERENCE FOUND:")
            print(f"Dump 1: {l1}")
            print(f"Dump 2: {l2}")
            print("-" * 20)
else:
    print("Not enough dumps found.")
