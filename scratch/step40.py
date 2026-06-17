import sys
import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix CC numbers
content = content.replace('{"OSC1_TUNE", -1}', '{"OSC1_TUNE", 27}')
content = content.replace('{"OSC2_FINE", 27}', '{"OSC2_FINE", 28}')
content = content.replace('{"OSC3_FINE", 28}', '{"OSC3_FINE", -1}') # Assuming no CC for OSC3_FINE

# Fix SysEx map
old_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    // syxParamMap[29] = "OSC1_TUNE"; // Removed, does not support sysex
    syxParamMap[30] = "OSC2_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";"""

new_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC1_TUNE";
    syxParamMap[30] = "OSC2_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";"""

if old_syx in content:
    content = content.replace(old_syx, new_syx)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Updated CC numbers and SysEx map")
else:
    print("Could not find SysEx map to replace")

