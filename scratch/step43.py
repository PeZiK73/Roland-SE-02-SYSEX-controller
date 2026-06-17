import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Fix the syxParamMap
old_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC1_TUNE";
    syxParamMap[30] = "OSC2_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";"""

new_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC2_FINE";
    syxParamMap[30] = "OSC3_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";"""

if old_syx in content:
    content = content.replace(old_syx, new_syx)
    print("Fixed SysEx map")
else:
    print("Could not find old_syx")

# 2. Fix the decoupling logic
old_decouple = """                // DECOUPLE OSC RANGE CCs
                if (cp.ccNumber == 22 || cp.ccNumber == 26 || cp.ccNumber == 30) // OSC1, 2, 3 Range"""

new_decouple = """                // DECOUPLE OSC RANGE CCs
                if (cp.id == "OSC1_RANGE" || cp.id == "OSC2_RANGE" || cp.id == "OSC3_RANGE") // OSC1, 2, 3 Range"""

if old_decouple in content:
    content = content.replace(old_decouple, new_decouple)
    print("Fixed decoupling logic")
else:
    print("Could not find old_decouple")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

