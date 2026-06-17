import sys

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

content = content.replace(
    "juce::AudioProcessorValueTreeState apvts;\n    std::vector<CcParam> ccParams;\n    std::atomic<float> incomingCcValues[128];",
    "std::vector<CcParam> ccParams;\n    std::atomic<float> incomingCcValues[128];\n    juce::AudioProcessorValueTreeState apvts;"
)

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)
    print("Fixed declaration order")
