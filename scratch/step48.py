import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Just replace line by line
content = content.replace('syxParamMap[29] = "OSC1_TUNE";', '// syxParamMap[29] = "OSC1_TUNE"; // Removed, does not support sysex')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
