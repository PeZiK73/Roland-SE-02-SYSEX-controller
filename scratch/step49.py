import sys

file1 = r'C:\Users\Notandi\Desktop\SE_02_BACKUP\PATCH\SE02_PATCH4.PRM'
file2 = r'C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\CUSTOM_PRESETS\PRESET_NR_04_SOUNDS_OFF.PRM'

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

print(f"Comparing Hardware Original to VST Saved Patch...")
for l1, l2 in zip(lines1, lines2):
    if l1 != l2:
        print(f"Original: {l1.strip()} | VST: {l2.strip()}")
