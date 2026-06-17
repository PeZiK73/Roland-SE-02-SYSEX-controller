import os

folder = r"C:\Users\Notandi\Documents\SE-02_ANTIGRAVITIY_EDITOR\HARDWARE_PATCHES\BANK_A"
files = [f for f in os.listdir(folder) if f.endswith('.prm')]
files.sort()

# Read the first two files to compare all parameters
path1 = os.path.join(folder, files[0])
path2 = os.path.join(folder, files[1])
with open(path1, 'r') as f1, open(path2, 'r') as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

print(f"Comparing {files[0]} and {files[1]}...")
diff_count = 0
for l1, l2 in zip(lines1, lines2):
    if l1 != l2:
        print(f"File 1: {l1.strip()} | File 2: {l2.strip()}")
        diff_count += 1

if diff_count == 0:
    print("THE FILES ARE EXACTLY IDENTICAL!")
