import sys
with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

content = content.replace('fetchTimeoutCounter = 10; // Wait 300ms for hardware to change patch', 'fetchTimeoutCounter = 30; // Wait 1 second for hardware to change patch')
content = content.replace('fetchTimeoutCounter = 15; // Wait 450ms for reply and APVTS update', 'fetchTimeoutCounter = 45; // Wait 1.5 seconds for reply and APVTS update')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
