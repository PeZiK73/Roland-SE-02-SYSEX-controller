import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

# Remove fetch elements
content = content.replace('juce::ComboBox fetchBankSelector;', '')
content = content.replace('juce::TextButton fetchBankBtn{"FETCH BANK"};', '')

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Remove addAndMakeVisible, bounds, onClick, etc.
content = re.sub(r'addAndMakeVisible\(fetchBankSelector\);.*?fetchBankSelector\.setSelectedId\(1\);', '', content, flags=re.DOTALL)
content = re.sub(r'addAndMakeVisible\(fetchBankBtn\);.*?fetchBankBtn\.setButtonText\("FETCHING\.\.\."\);\s*\};', '', content, flags=re.DOTALL)
content = re.sub(r'fetchBankSelector\.setBounds.*?;', '', content)
content = re.sub(r'fetchBankBtn\.setBounds.*?;', '', content)

# Change PresetBrowser constructor call to pass audioProcessor
content = content.replace('presetBrowser = std::make_unique<PresetBrowser>(', 'presetBrowser = std::make_unique<PresetBrowser>(\n                audioProcessor,')

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
