import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix the SysEx parameter map
old_map = """    syxParamMap[20] = "GLIDE";
    syxParamMap[21] = "GLIDE_TYPE";
    syxParamMap[22] = "WHL_MIX";
    syxParamMap[25] = "OSC1_TUNE";
    
    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC2_FINE";
    syxParamMap[30] = "OSC3_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";
    syxParamMap[32] = "OSC2_WAVE";
    syxParamMap[33] = "OSC3_WAVE";
    syxParamMap[34] = "SYNC";
    syxParamMap[35] = "ENV1";
    syxParamMap[36] = "KYBD";
    syxParamMap[37] = "XMOD_MW";"""

new_map = """    syxParamMap[20] = "GLIDE";
    syxParamMap[21] = "GLIDE_TYPE";
    syxParamMap[22] = "WHL_MIX";
    
    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC1_TUNE";
    syxParamMap[30] = "OSC2_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";
    syxParamMap[32] = "OSC2_WAVE";
    syxParamMap[33] = "OSC3_WAVE";
    syxParamMap[34] = "SYNC";
    syxParamMap[35] = "ENV1";
    syxParamMap[36] = "KYBD";
    syxParamMap[37] = "XMOD_MW";"""

if old_map in content:
    content = content.replace(old_map, new_map)
    print("Fixed syxParamMap")
else:
    print("Could not find old_map")

# Fix the PRM format logic
old_format = """    formatLine("OSC_RANGE1", "OSC1_RANGE", 5);
    formatLine("OSC_RANGE2", "OSC2_RANGE", 5);
    formatLine("OSC_RANGE3", "OSC3_RANGE", 5);
    
    formatLine("OSC_FINE1", "OSC2_FINE", -1);
    formatLine("OSC_FINE2", "OSC3_FINE", -1);"""

new_format = """    formatLine("OSC_RANGE1", "OSC1_RANGE", 5);
    formatLine("OSC_RANGE2", "OSC2_RANGE", 5);
    formatLine("OSC_RANGE3", "OSC3_RANGE", 5);
    
    formatLine("OSC_FINE1", "OSC1_TUNE", -1);
    formatLine("OSC_FINE2", "OSC2_FINE", -1);"""

if old_format in content:
    content = content.replace(old_format, new_format)
    print("Fixed formatLine")
else:
    print("Could not find old_format")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
