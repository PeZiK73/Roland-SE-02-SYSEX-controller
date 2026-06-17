import sys

filename = 'C:/Users/Notandi/Documents/SE-02_ANTIGRAVITIY_EDITOR/HARDWARE_PATCHES/CUSTOM PRESETS/A01.syx'
try:
    with open(filename, 'rb') as f:
        data = f.read()
    
    # SysEx patch files might have multiple packets. Let's just find the DT1 packet for Temporary Patch (02 00 00 00)
    # F0 41 10 00 00 00 44 12 02 00 00 00 ...
    
    # Just print the whole file as hex
    print(" ".join([f"{b:02X}" for b in data]))

except Exception as e:
    print("Error:", e)

