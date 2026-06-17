import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Remove the completely broken decoupling logic
old_decouple = """                // DECOUPLE OSC RANGE CCs
                if (cp.id == "OSC1_RANGE" || cp.id == "OSC2_RANGE" || cp.id == "OSC3_RANGE") // OSC1, 2, 3 Range
                {
                    int idx = juce::roundToInt((currentVal / 127.0f) * 5.0f);
                    idx = juce::jlimit(0, 5, idx);
                    int hwCCs[6] = {8, 24, 40, 56, 72, 88};
                    ccValue = hwCCs[idx];
                }"""

new_decouple = """                // DECOUPLE logic removed because standard CC values 0-127 work perfectly
                // for the SE-02 range switches. The previous hardcoded logic was breaking the patches."""

if old_decouple in content:
    content = content.replace(old_decouple, new_decouple)
    print("Removed decoupling logic")
else:
    print("Could not find old_decouple")

# 2. Fix syxParamMap correctly
old_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC1_TUNE";
    syxParamMap[30] = "OSC2_FINE";"""

new_syx = """    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC2_FINE";
    syxParamMap[30] = "OSC3_FINE";"""

if old_syx in content:
    content = content.replace(old_syx, new_syx)
    print("Fixed SysEx map")
else:
    print("Could not find old_syx")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

