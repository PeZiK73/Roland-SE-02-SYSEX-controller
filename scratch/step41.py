import sys
import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Revert CC numbers back to what worked for the user
content = content.replace('{"OSC1_TUNE", 27}', '{"OSC1_TUNE", -1}')
content = content.replace('{"OSC2_FINE", 28}', '{"OSC2_FINE", 27}')
content = content.replace('{"OSC3_FINE", -1}', '{"OSC3_FINE", 28}')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
    print("Reverted CC numbers, kept SysEx map")
