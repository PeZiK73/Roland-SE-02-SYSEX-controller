import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC2_FINE";
    syxParamMap[30] = "OSC3_FINE";"""

new_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC1_TUNE";
    syxParamMap[30] = "OSC2_FINE";"""

if old_syx in content:
    content = content.replace(old_syx, new_syx)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Reverted SysEx map")
else:
    print("Could not revert SysEx map")
