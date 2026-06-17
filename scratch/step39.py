import sys

filename = 'C:/Users/Notandi/Documents/SE-02_ANTIGRAVITIY_EDITOR/HARDWARE_PATCHES/BANK_A/1.syx'
try:
    with open(filename, 'rb') as f:
        data = f.read()
    
    # SysEx data starts at byte 12 (0-indexed) if the header is 12 bytes long (F0 41 10 00 00 00 44 12 02 00 00 00)
    # The bytes are encoded as nibbles.
    
    if len(data) > 12:
        nibbles = data[12:-2] # remove checksum and F7
        bytes_decoded = []
        for i in range(0, len(nibbles), 2):
            b = ((nibbles[i] & 0x0F) << 4) | (nibbles[i+1] & 0x0F)
            bytes_decoded.append(b)
            
        print("Decoded patch bytes:")
        for i, b in enumerate(bytes_decoded):
            print(f"[{i:3d}] = {b}")
            
except Exception as e:
    print("Error:", e)

