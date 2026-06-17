import os

target_file = r'C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\CUSTOM_PRESETS\PRESET_NR_04_SOUNDS_OFF.PRM'
with open(target_file, 'r') as f:
    target_lines = f.readlines()

folder = r"C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\HARDWARE_PATCHES\BANK_A"
files = [f for f in os.listdir(folder) if f.endswith('.prm')]

found = False
for file in files:
    path = os.path.join(folder, file)
    with open(path, 'r') as f:
        lines = f.readlines()
    
    diff_count = 0
    for l1, l2 in zip(target_lines, lines):
        if l1 != l2:
            diff_count += 1
            
    if diff_count == 0:
        print(f"MATCH FOUND: {file} is exactly identical to PRESET_NR_04_SOUNDS_OFF.PRM")
        found = True

if not found:
    print("NO MATCH FOUND IN BANK A!")
