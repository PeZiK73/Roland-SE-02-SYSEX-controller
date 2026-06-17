import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

# Add #include "PresetBrowser.h"
if '#include "PresetBrowser.h"' not in content:
    content = content.replace('#include "PluginProcessor.h"', '#include "PluginProcessor.h"\n#include "PresetBrowser.h"')

# Add PresetBrowser and Fetch components to private section
hook = '''
    std::unique_ptr<juce::FileChooser> fileChooser;
    
    std::unique_ptr<PresetBrowser> presetBrowser;
    
    juce::ComboBox fetchBankSelector;
    juce::TextButton fetchBankBtn{"FETCH BANK"};
'''

if 'std::unique_ptr<PresetBrowser> presetBrowser;' not in content:
    content = content.replace('    std::unique_ptr<juce::FileChooser> fileChooser;', hook)
    with open('Source/PluginEditor.h', 'w') as f:
        f.write(content)

