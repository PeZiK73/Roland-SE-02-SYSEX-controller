import os

folder = r"C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\HARDWARE_PATCHES\BANK_A"
files = [f for f in os.listdir(folder) if f.endswith('.prm')]
files.sort()

# Read the first few files to see if they differ
for i in range(min(4, len(files))):
    path = os.path.join(folder, files[i])
    with open(path, 'r') as f:
        content = f.read()
    # Print the first 5 parameters
    print(f"File: {files[i]}")
    lines = content.split('\n')
    for line in lines[:15]:
        if "OSC_RANGE1" in line or "NAME1" in line or "FLT_CUTOFF" in line:
            print(f"  {line.strip()}")
