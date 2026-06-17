import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_process = """                  int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                  
                  // DECOUPLE OSC RANGE CCs"""

new_process = """                  int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                  
                  if (cp.ccNumber < 0) {
                      cp.lastValue = currentVal;
                      continue;
                  }
                  
                  // DECOUPLE OSC RANGE CCs"""

if new_process not in content:
    content = content.replace(old_process, new_process)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Fixed bounds check in processBlock")
else:
    print("Already fixed")
