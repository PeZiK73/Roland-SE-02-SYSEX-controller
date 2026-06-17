import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix 1: requestSysExPreset to request 0x02 (Temporary Patch) instead of 0x05 (Bank A Patch 1)
old_sendrq1 = """    auto sendRQ1 = [&](juce::uint8 a2, juce::uint8 a3, juce::uint8 s3) {
        juce::uint8 sysexData[] = {
            0xF0, 0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 
            0x05, 0x00, a2, a3, 
            0x00, 0x00, 0x00, s3, 
            0x00, 0xF7
        };
        int sum = 0x05 + 0x00 + a2 + a3 + 0x00 + 0x00 + 0x00 + s3;"""

new_sendrq1 = """    auto sendRQ1 = [&](juce::uint8 a2, juce::uint8 a3, juce::uint8 s3) {
        juce::uint8 sysexData[] = {
            0xF0, 0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 
            0x02, 0x00, a2, a3, 
            0x00, 0x00, 0x00, s3, 
            0x00, 0xF7
        };
        int sum = 0x02 + 0x00 + a2 + a3 + 0x00 + 0x00 + 0x00 + s3;"""

if old_sendrq1 in content:
    content = content.replace(old_sendrq1, new_sendrq1)
    print("Fixed requestSysExPreset")
else:
    print("Could not find old_sendrq1")

# Fix 2: processBlock to parse 0x02 instead of 0x05
old_parse = "if (data[8] == 0x05 && data[9] == 0x00)"
new_parse = "if (data[8] == 0x02 && data[9] == 0x00)"

if old_parse in content:
    content = content.replace(old_parse, new_parse)
    print("Fixed processBlock")
else:
    print("Could not find old_parse")

# Fix 3: Re-add OSC1_TUNE to the map
old_map = """    syxParamMap[22] = "WHL_MIX";
    
    syxParamMap[26] = "OSC1_RANGE";"""

new_map = """    syxParamMap[22] = "WHL_MIX";
    syxParamMap[25] = "OSC1_TUNE";
    
    syxParamMap[26] = "OSC1_RANGE";"""

if old_map in content:
    content = content.replace(old_map, new_map)
    print("Fixed syxParamMap")
else:
    print("Could not find old_map")


with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

