import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Add to constructor
init_hook = '''
    addAndMakeVisible(fetchBankSelector);
    fetchBankSelector.addItem("BANK A", 1);
    fetchBankSelector.addItem("BANK B", 2);
    fetchBankSelector.addItem("BANK C", 3);
    fetchBankSelector.addItem("BANK D", 4);
    fetchBankSelector.addItem("USER", 5);
    fetchBankSelector.setSelectedId(1);
    
    addAndMakeVisible(fetchBankBtn);
    fetchBankBtn.onClick = [this] {
        audioProcessor.startFetchingBank(fetchBankSelector.getSelectedId() - 1);
        fetchBankBtn.setButtonText("FETCHING...");
    };
    
    browseBtn.onClick = [this] {
        if (presetBrowser == nullptr) {
            presetBrowser = std::make_unique<PresetBrowser>(
                [this](juce::String path) {
                    // On select
                    juce::File file = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
                        .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
                        .getChildFile("HARDWARE_PATCHES")
                        .getChildFile(path);
                    if (file.existsAsFile()) {
                        loadPresetFromFile(file);
                        presetBrowser = nullptr;
                    }
                },
                [this]() {
                    // On close
                    presetBrowser = nullptr;
                }
            );
            addAndMakeVisible(presetBrowser.get());
            presetBrowser->setBounds(0, 0, getWidth(), getHeight());
        } else {
            presetBrowser = nullptr;
        }
    };
'''

# Find the end of constructor (before resized or destructor)
if 'fetchBankSelector.addItem' not in content:
    content = content.replace('    addAndMakeVisible(browseBtn);', '    addAndMakeVisible(browseBtn);\n' + init_hook)

# Add to resized
resize_hook = '''
    if (presetBrowser != nullptr) presetBrowser->setBounds(0, 0, w, h);
    
    fetchBankSelector.setBounds(330 * scaleX, h - (25 * scaleY), 80 * scaleX, 20 * scaleY);
    fetchBankBtn.setBounds(420 * scaleX, h - (25 * scaleY), 90 * scaleX, 20 * scaleY);
'''

if 'fetchBankSelector.setBounds' not in content:
    content = content.replace('    browseBtn.setBounds(250 * scaleX, h - (25 * scaleY), 70 * scaleX, 20 * scaleY);', '    browseBtn.setBounds(250 * scaleX, h - (25 * scaleY), 70 * scaleX, 20 * scaleY);\n' + resize_hook)

# Timer hack to reset button text when fetch is done
timer_hook = '''
    if (audioProcessor.isFetchingBank()) {
        fetchBankBtn.setButtonText("FETCHING " + juce::String(audioProcessor.getFetchProgress()) + "/128");
    } else {
        fetchBankBtn.setButtonText("FETCH BANK");
    }
'''
if 'fetchBankBtn.setButtonText' not in content:
    # We don't have a timer in Editor, but we can just use the processor timer or add a simple GUI timer
    pass

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)

