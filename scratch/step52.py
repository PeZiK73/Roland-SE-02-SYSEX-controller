import sys
import os

file1 = r'C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\HARDWARE_PATCHES\BANK_A\A-TYPICAL BASS.prm'
file2 = r'C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\CUSTOM_PRESETS\PRESET_NR_04_SOUNDS_OFF.PRM'

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

print(f"Comparing A-TYPICAL BASS to VST Saved Patch...")
diff_count = 0
for l1, l2 in zip(lines1, lines2):
    if l1 != l2:
        print(f"A-TYPICAL: {l1.strip()} | VST: {l2.strip()}")
        diff_count += 1

if diff_count == 0:
    print("THEY ARE IDENTICAL!")
