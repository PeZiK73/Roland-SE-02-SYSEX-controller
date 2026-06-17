import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Fix sendProgramChange
old_send_pc = """    // MSB Bank A=0, B=1, C=2, USER=3, D=4
    // LSB is always 0
    int msb = currentBankIndex;
    int lsb = 0;"""

new_send_pc = """    int msb = 85; // SE-02 MSB is always 85
    int lsb = 0;
    if (currentBankIndex == 0) lsb = 0; // Bank A
    else if (currentBankIndex == 1) lsb = 1; // Bank B
    else if (currentBankIndex == 2) lsb = 2; // Bank C
    else if (currentBankIndex == 3) lsb = 3; // Bank D
    else if (currentBankIndex == 4) lsb = 4; // USER Bank"""

if old_send_pc in content:
    content = content.replace(old_send_pc, new_send_pc)
    print("Fixed sendProgramChange")
else:
    print("Could not find old_send_pc")

# 2. Fix fetch state machine
old_fetch_pc = """        int msb = fetchBankIndex; 
        int lsb = 0; 
        int pc = fetchPatchIndex;"""

new_fetch_pc = """        int msb = 85; 
        int lsb = 0;
        if (fetchBankIndex == 0) lsb = 0; // Bank A
        else if (fetchBankIndex == 1) lsb = 1; // Bank B
        else if (fetchBankIndex == 2) lsb = 2; // Bank C
        else if (fetchBankIndex == 3) lsb = 3; // Bank D
        else if (fetchBankIndex == 4) lsb = 4; // USER Bank
        int pc = fetchPatchIndex;"""

if old_fetch_pc in content:
    content = content.replace(old_fetch_pc, new_fetch_pc)
    print("Fixed fetch state machine")
else:
    print("Could not find old_fetch_pc")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

