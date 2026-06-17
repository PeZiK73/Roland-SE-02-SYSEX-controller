import sys
with open('Source/PluginProcessor.cpp', 'r') as f:
    lines = f.readlines()
    
for i, line in enumerate(lines):
    if 'handleIncomingMidiMessage' in line:
        print("".join(lines[i:i+40]))
        break
