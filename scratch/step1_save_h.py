import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

# Add savePresetToFile
content = content.replace("    void resized() override;", "    void resized() override;\n    void savePresetToFile(const juce::File& file);")

# Add FileChooser
content = content.replace("    juce::TextButton savePresetBtn{\"SAVE PR\"};", "    juce::TextButton savePresetBtn{\"SAVE PRESET\"};\n    std::unique_ptr<juce::FileChooser> fileChooser;")

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)
