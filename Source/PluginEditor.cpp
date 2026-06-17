#include "PluginProcessor.h"
#include <fstream>
#include "PluginEditor.h"
#include "BinaryData.h"

class MainPanel : public juce::Component
{
public:
    MainPanel()
    {
        bgImage = juce::ImageCache::getFromMemory(BinaryData::grid_bg_png, BinaryData::grid_bg_pngSize);
    }
    
    void paint(juce::Graphics& g) override
    {
        g.fillAll (juce::Colour (0xff171717)); // bottom bar color
        if (bgImage.isValid())
            g.drawImage(bgImage, 0, 0, 1024, 298, 0, 0, bgImage.getWidth(), bgImage.getHeight());
    }
private:
    juce::Image bgImage;
};

SE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor (SE02_ControllerAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p), resizer(this, &constrainer)
{

    mainPanel = std::make_unique<MainPanel>();
    mainPanel->setBounds(0, 0, 1024, 330);
    addAndMakeVisible(mainPanel.get());
    setSize (2048, 660);

    setResizable(true, true);
    constrainer.setFixedAspectRatio(1024.0 / 330.0);
    constrainer.setSizeLimits(1024, 330, 2048, 660);
    setConstrainer(&constrainer);


    addAndMakeVisible(midiInSelector);
    midiInSelector.setTextWhenNothingSelected("MIDI In...");
    midiInSelector.addItemList(getMidiInputNames(), 1);
    midiInSelector.onChange = [this] { audioProcessor.openMidiInput(midiInSelector.getText()); };

    addAndMakeVisible(midiOutSelector);
    midiOutSelector.setTextWhenNothingSelected("MIDI Out...");
    midiOutSelector.addItemList(getMidiOutputNames(), 1);
    midiOutSelector.onChange = [this] { audioProcessor.openMidiOutput(midiOutSelector.getText()); };

    addAndMakeVisible(loadPresetBtn);
    loadPresetBtn.onClick = [this] {
        juce::File customPresetsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
            .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
            .getChildFile("CUSTOM_PRESETS");
            
        fileChooser = std::make_unique<juce::FileChooser> (
            "Load Preset...",
            customPresetsDir,
            "*.syx;*.prm;*.SYX;*.PRM;*.SE2"
        );
        
        auto chooserFlags = juce::FileBrowserComponent::openMode | juce::FileBrowserComponent::canSelectFiles;
        
        fileChooser->launchAsync(chooserFlags, [this] (const juce::FileChooser& fc) {
            juce::File file = fc.getResult();
            if (file != juce::File{}) {
                loadPresetFromFile(file);
            }
        });
    };

    addAndMakeVisible(resizer);

    auto updateLabels = [this] {
        if (audioProcessor.currentBankIndex >= 5) {
            presetLabel.setText("CUSTOM PRESET", juce::dontSendNotification);
            return;
        }
        
        int bankIdx = audioProcessor.currentBankIndex;
        int presetIdx = audioProcessor.currentPreset; // 1-128
        
        juce::String bankId = "";
        if (bankIdx == 0) bankId = "BANK_A";
        else if (bankIdx == 1) bankId = "BANK_B";
        else if (bankIdx == 2) bankId = "BANK_C";
        else if (bankIdx == 3) bankId = "BANK_D";
        else if (bankIdx == 4) bankId = "USER";
        
        juce::String presetText = "PRESET " + juce::String(presetIdx).paddedLeft('0', 3) + ": Empty";
        
        juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
        juce::File bankDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES").getChildFile(bankId);
        
        juce::String prefix = juce::String(presetIdx).paddedLeft('0', 3) + "_";
        juce::Array<juce::File> files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.syx");
        if (files.isEmpty()) files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.prm");
        
        if (files.size() > 0) {
            juce::String name = files[0].getFileNameWithoutExtension().substring(4);
            name = name.replaceCharacter('_', ' ');
            presetText = juce::String(presetIdx).paddedLeft('0', 3) + " " + name;
        }
        
        presetLabel.setText(presetText, juce::dontSendNotification);
    };

    auto loadCurrentHardwareFile = [this] {
        juce::String bankId = "";
        if (audioProcessor.currentBankIndex == 0) bankId = "BANK_A";
        else if (audioProcessor.currentBankIndex == 1) bankId = "BANK_B";
        else if (audioProcessor.currentBankIndex == 2) bankId = "BANK_C";
        else if (audioProcessor.currentBankIndex == 3) bankId = "BANK_D";
        else if (audioProcessor.currentBankIndex == 4) bankId = "USER";
        else return;
        
        juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
        juce::File bankDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES").getChildFile(bankId);
        juce::String prefix = juce::String(audioProcessor.currentPreset).paddedLeft('0', 3) + "_";
        juce::Array<juce::File> files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.syx");
        if (files.isEmpty()) files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.prm");
        
        if (files.size() > 0) {
            loadPresetFromFile(files[0]);
        }
    };

    addAndMakeVisible(presetPrevBtn);
    presetPrevBtn.onClick = [this, updateLabels, loadCurrentHardwareFile] {
        if (audioProcessor.currentBankIndex >= 5) return;
        if (audioProcessor.currentPreset > 1) audioProcessor.currentPreset--;
        else audioProcessor.currentPreset = 128;
        audioProcessor.sendProgramChange();
        loadCurrentHardwareFile();
        updateLabels();
    };

    addAndMakeVisible(presetLabel);
    presetLabel.setJustificationType(juce::Justification::centred);
    presetLabel.setColour(juce::Label::textColourId, juce::Colours::yellow);

    addAndMakeVisible(presetNextBtn);
    presetNextBtn.onClick = [this, updateLabels, loadCurrentHardwareFile] {
        if (audioProcessor.currentBankIndex >= 5) return;
        if (audioProcessor.currentPreset < 128) audioProcessor.currentPreset++;
        else audioProcessor.currentPreset = 1;
        audioProcessor.sendProgramChange();
        loadCurrentHardwareFile();
        updateLabels();
    };

    addAndMakeVisible(bankSelectorMain);
    bankSelectorMain.addItem("BANK A", 1);
    bankSelectorMain.addItem("BANK B", 2);
    bankSelectorMain.addItem("BANK C", 3);
    bankSelectorMain.addItem("BANK D", 4);
    bankSelectorMain.addItem("USER", 5);
    bankSelectorMain.addItem("CUSTOM", 6);
    bankSelectorMain.setSelectedId(audioProcessor.currentBankIndex + 1, juce::dontSendNotification);
    bankSelectorMain.setColour(juce::ComboBox::backgroundColourId, juce::Colour(0xff222222));
    bankSelectorMain.setColour(juce::ComboBox::outlineColourId, juce::Colour(0xff555555));
    bankSelectorMain.onChange = [this, updateLabels] {
        audioProcessor.currentBankIndex = bankSelectorMain.getSelectedId() - 1;
        if (audioProcessor.currentBankIndex < 5) audioProcessor.sendProgramChange();
        updateLabels();
    };

    addAndMakeVisible(browseBtn);

    
    
    
    
    browseBtn.onClick = [this, updateLabels] {
        if (presetBrowser == nullptr) {
            presetBrowser = std::make_unique<PresetBrowser>(
                audioProcessor,
                [this, updateLabels](juce::String path) {
                    // On select
                    juce::File file = juce::File(path);
                    if (file.existsAsFile()) {
                        loadPresetFromFile(file);
                        
                        juce::String parentDir = file.getParentDirectory().getFileName();
                        if (parentDir == "BANK_A") audioProcessor.currentBankIndex = 0;
                        else if (parentDir == "BANK_B") audioProcessor.currentBankIndex = 1;
                        else if (parentDir == "BANK_C") audioProcessor.currentBankIndex = 2;
                        else if (parentDir == "BANK_D") audioProcessor.currentBankIndex = 3;
                        else if (parentDir == "USER") audioProcessor.currentBankIndex = 4;
                        else if (parentDir == "CUSTOM_PRESETS") audioProcessor.currentBankIndex = 5;
                        
                        if (audioProcessor.currentBankIndex < 5) {
                            juce::String numStr = file.getFileName().substring(0, 3);
                            audioProcessor.currentPreset = numStr.getIntValue();
                        }
                        
                        bankSelectorMain.setSelectedId(audioProcessor.currentBankIndex + 1, juce::dontSendNotification);
                        
                        if (audioProcessor.currentBankIndex >= 5) {
                            juce::String name = file.getFileNameWithoutExtension().replaceCharacter('_', ' ');
                            presetLabel.setText(name, juce::dontSendNotification);
                        } else {
                            updateLabels();
                        }
                    }
                },
                [this]() {
                    // On close
                    presetBrowser = nullptr;
                }
            );
            presetBrowser->onMorphChangeCallback = [this](juce::String pathA, juce::String pathB, float ratio) {
                if (nameA.isEmpty() || nameB.isEmpty() || stateA.empty() || stateB.empty() || lastPathA != pathA || lastPathB != pathB) {
                    stateA = getPresetState(juce::File(pathA), nameA);
                    stateB = getPresetState(juce::File(pathB), nameB);
                    lastPathA = pathA;
                    lastPathB = pathB;
                }
                
                for (auto const& [id, valA] : stateA) {
                    if (auto* param = audioProcessor.apvts.getParameter(id)) {
                        float valB = stateB.count(id) ? stateB[id] : valA;
                        float morphed = valA;
                        
                        if (id.endsWith("_WAVE")) {
                            morphed = valA * (1.0f - ratio) + valB * ratio;
                        } else if (id == "GLIDE_TYPE" || id == "SYNC" || id == "KYBD" || id == "XMOD_MW" || 
                                   id == "KEYTRACK_13" || id == "KEYTRACK_23" || id == "MTRIG" || id == "INVERT" || 
                                   id == "REL" || id == "GATE_LFO" || id == "LFO_MW_OSC" || id == "LFO_MW_FLT" || 
                                   id == "LFO_MODE" || id == "LFO_SYNC") {
                            morphed = valA;
                        } else {
                            morphed = valA * (1.0f - ratio) + valB * ratio;
                        }
                        
                        param->setValueNotifyingHost(morphed);
                    }
                }
            };

            presetBrowser->onMorphApplyCallback = [this](juce::String pathA, juce::String pathB) {
                juce::String newName = nameA.substring(0, 3) + nameB.substring(0, 3);
                juce::String padded = newName.paddedRight(' ', 16).substring(0, 16);
                for (int i = 0; i < 16; ++i) {
                    audioProcessor.currentSysExBuffer[208 + i].store((float)padded[i]);
                }
                presetLabel.setText(newName, juce::dontSendNotification);
                nameA = "";
                nameB = "";
                stateA.clear();
                stateB.clear();
            };
            
            presetBrowser->onRndPatchCallback = [this](int selectedCategoryId) {
                juce::Random& rng = juce::Random::getSystemRandom();
                
                int category = (selectedCategoryId == 1) ? rng.nextInt(4) : (selectedCategoryId - 2);
                juce::String categoryName;
                
                for (auto* param : audioProcessor.getParameters()) {
                    if (auto* rangedParam = dynamic_cast<juce::RangedAudioParameter*>(param)) {
                        juce::String id = rangedParam->paramID;
                        float val = rng.nextFloat();
                        
                        if (id == "OSC2_FINE" || id == "OSC3_FINE") {
                            val = 0.5f;
                        } else if (id == "GLIDE" || id == "DLY_TIME" || id == "DLY_REGEN" || id == "DLY_AMOUNT") {
                            val = 0.0f;
                        } else if (id == "LFO_OSC" || id == "LFO_FILT" || id == "LFO_MW_OSC" || id == "LFO_MW_FLT") {
                            val = 0.0f;
                        } else if (id == "XMOD_MW" || id == "XMOD_O2FLT" || id == "XMOD_O3O2" || id == "XMOD_O3PW") {
                            val = 0.0f;
                        } else if (id == "MIX_OSC1") {
                            val = 1.0f;
                        } else if (id == "CUTOFF") {
                            val = 0.3f + (val * 0.5f);
                        }
                        
                        if (category == 0) { // Bass
                            categoryName = "BASS";
                            if (id == "OSC1_RANGE" || id == "OSC2_RANGE" || id == "OSC3_RANGE") {
                                val = (rng.nextInt(2) + 1) / 5.0f;
                            } else if (id == "AMP_ATTACK" || id == "FILT_ATTACK") {
                                val = val * 0.1f;
                            } else if (id == "AMP_DECAY" || id == "FILT_DECAY") {
                                val = 0.1f + (val * 0.4f);
                            } else if (id == "CUTOFF") {
                                val = 0.1f + (val * 0.4f);
                            }
                        } else if (category == 1) { // Lead
                            categoryName = "LEAD";
                            if (id == "OSC1_RANGE" || id == "OSC2_RANGE" || id == "OSC3_RANGE") {
                                val = (rng.nextInt(2) + 2) / 5.0f;
                            } else if (id == "AMP_ATTACK") {
                                val = val * 0.1f;
                            } else if (id == "AMP_SUSTAIN") {
                                val = 0.6f + (val * 0.4f);
                            } else if (id == "CUTOFF") {
                                val = 0.5f + (val * 0.5f);
                            }
                        } else if (category == 2) { // Pluck
                            categoryName = "PLUK";
                            if (id == "OSC1_RANGE" || id == "OSC2_RANGE" || id == "OSC3_RANGE") {
                                val = (rng.nextInt(2) + 2) / 5.0f;
                            } else if (id == "AMP_ATTACK" || id == "FILT_ATTACK") {
                                val = 0.0f;
                            } else if (id == "AMP_DECAY" || id == "FILT_DECAY") {
                                val = 0.1f + (val * 0.3f);
                            } else if (id == "AMP_SUSTAIN" || id == "FILT_SUSTAIN") {
                                val = 0.0f;
                            }
                        } else if (category == 3) { // Pad
                            categoryName = "PAD_";
                            if (id == "OSC1_RANGE" || id == "OSC2_RANGE" || id == "OSC3_RANGE") {
                                val = (rng.nextInt(2) + 3) / 5.0f;
                            } else if (id == "AMP_ATTACK") {
                                val = 0.4f + (val * 0.6f);
                            } else if (id == "REL") {
                                val = 0.4f + (val * 0.6f);
                            } else if (id == "AMP_SUSTAIN") {
                                val = 0.6f + (val * 0.4f);
                            }
                        }
                        
                        rangedParam->setValueNotifyingHost(val);
                    }
                }
                
                juce::String newName = categoryName + "_" + juce::Time::getCurrentTime().formatted("%H%M%S");
                juce::String padded = newName.paddedRight(' ', 16).substring(0, 16);
                for (int i = 0; i < 16; ++i) {
                    audioProcessor.currentSysExBuffer[208 + i].store((float)padded[i]);
                }
                presetLabel.setText(newName, juce::dontSendNotification);
            };

            addAndMakeVisible(presetBrowser.get());
            presetBrowser->setBounds(0, 0, getWidth(), getHeight());
        } else {
            presetBrowser = nullptr;
        }
    };

    addAndMakeVisible(savePresetBtn);


    savePresetBtn.onClick = [this] {
        juce::File customPresetsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
            .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
            .getChildFile("CUSTOM_PRESETS");
        
        if (!customPresetsDir.exists())
            customPresetsDir.createDirectory();
            
        juce::Time now = juce::Time::getCurrentTime();
        juce::String currentName = presetLabel.getText().replaceCharacter(' ', '_').trim();
        if (currentName.isEmpty() || currentName == "Unknown") currentName = "Preset";
        juce::String defaultName = currentName + "_" + now.formatted("%Y%m%d_%H%M%S") + ".syx";
        
        fileChooser = std::make_unique<juce::FileChooser> (
            "Save Preset...",
            customPresetsDir.getChildFile(defaultName),
            "*.syx;*.prm;*.SYX;*.PRM"
        );
        
        auto chooserFlags = juce::FileBrowserComponent::saveMode | juce::FileBrowserComponent::canSelectFiles;
        
        fileChooser->launchAsync(chooserFlags, [this] (const juce::FileChooser& fc) {
            juce::File file = fc.getResult();
            if (file != juce::File{}) {
                savePresetToFile(file);
            }
        });
    };

    updateLabels();



    addAndMakeVisible(showValuesBtn);
    showValuesBtn.setToggleState(false, juce::dontSendNotification);
    showValuesBtn.onClick = [this] {
        bool show = showValuesBtn.getToggleState();
        customLookAndFeel.showValues = show;
        switchLookAndFeel.showValues = show;
        repaint();
    };
    customLookAndFeel.showValues = false;
    switchLookAndFeel.showValues = false;

    if (audioProcessor.lastMidiInName.isNotEmpty()) {
        for (int i = 0; i < midiInSelector.getNumItems(); ++i) {
            if (midiInSelector.getItemText(i) == audioProcessor.lastMidiInName) {
                midiInSelector.setSelectedId(midiInSelector.getItemId(i), juce::dontSendNotification);
                break;
            }
        }
    }
    if (audioProcessor.lastMidiOutName.isNotEmpty()) {
        for (int i = 0; i < midiOutSelector.getNumItems(); ++i) {
            if (midiOutSelector.getItemText(i) == audioProcessor.lastMidiOutName) {
                midiOutSelector.setSelectedId(midiOutSelector.getItemId(i), juce::dontSendNotification);
                break;
            }
        }
    }



    setLookAndFeel(&customLookAndFeel);


    int kSize = 40;
    int sWidth = 20;
    int sHeight = 40;
    
    int my1 = 126; // OSC 1
    int my2 = 162; // FEEDBACK
    int my3 = 198; // OSC 2
    int my4 = 233; // NOISE
    int my5 = 269; // OSC 3
    
    int r1 = 126;
    int r2 = 198;
    int r3 = 269;
    int cy1 = 162;
    int cy2 = 233;

    // --- EXPORTED LAYOUT ---
    addKnob("GLIDE", "GLIDE", 45, 131, 40);
    addSwitch("GLIDE_TYPE", "TYPE", 43, 213, 32, 52);
    addKnob("WHL_MIX", "WHL MIX", 45, 269, 40);
    addKnob("OSC1_RANGE", "RANGE", 115, 131, 40);
    addKnob("OSC1_TUNE", "TUNE", 185, 131, 40);
    addKnob("OSC1_WAVE", "WAVEFORM", 255, 131, 40);
    addSwitch("SYNC", "SYNC", 325, 146, 28, 48);
    addKnob("OSC2_RANGE", "RANGE", 115, 201, 40);
    addKnob("OSC2_FINE", "FINE", 185, 200, 40);
    addKnob("OSC2_WAVE", "WAVEFORM", 255, 199, 40);
    addKnob("ENV1", "ENV1", 326, 200, 40);
    addKnob("OSC3_RANGE", "RANGE", 115, 270, 40);
    addKnob("OSC3_FINE", "FINE", 186, 270, 40);
    addKnob("OSC3_WAVE", "WAVEFORM", 255, 269, 40);
    addSwitch("KYBD", "KYBD", 310, 282, 32, 52);
    addSwitch("XMOD_MW", "XMOD", 338, 281, 32, 52);
    addKnob("XMOD_O2FLT", "O2-FILTER", 395, 132, 40);
    addKnob("XMOD_O3O2", "O3-O2", 395, 201, 40);
    addKnob("XMOD_O3PW", "O3-PW1,2", 395, 271, 40);
    addKnob("MIX_OSC1", "OSC 1", 452, 128, 40);
    addKnob("MIX_OSC2", "OSC 2", 452, 198, 40);
    addKnob("MIX_OSC3", "OSC 3", 453, 269, 40);
    addKnob("MIX_FBACK", "FEEDBACK", 494, 166, 40);
    addKnob("MIX_NOISE", "NOISE", 494, 235, 40);
    addKnob("CUTOFF", "CUTOFF", 560, 131, 40);
    addKnob("EMPHASIS", "EMPHASIS", 626, 130, 40);
    addSwitch("KEYTRACK_13", "1/3", 678, 142, 20, 40);
    addSwitch("KEYTRACK_23", "2/3", 709, 142, 20, 40);
    addKnob("CONTOUR", "CONTOUR", 764, 131, 40);
    addKnob("FILT_ATTACK", "ATTACK", 560, 201, 40);
    addKnob("FILT_DECAY", "DECAY", 627, 198, 40);
    addKnob("FILT_SUSTAIN", "SUSTAIN", 693, 199, 40);
    addSwitch("MTRIG", "MTRIG", 747, 208, 20, 34);
    addSwitch("INVERT", "INVERT", 778, 207, 20, 34);
    addKnob("AMP_ATTACK", "ATTACK", 560, 271, 40);
    addKnob("AMP_DECAY", "DECAY", 627, 269, 40);
    addKnob("AMP_SUSTAIN", "SUSTAIN", 693, 270, 40);
    addSwitch("REL", "REL", 748, 281, 32, 48);
    addSwitch("GATE_LFO", "GATE", 779, 281, 32, 48);
    addKnob("LFO_RATE", "RATE", 833, 132, 40);
    addKnob("LFO_WAVE", "WAVE", 903, 131, 40);
    addKnob("LFO_OSC", "OSC", 833, 201, 40);
    addKnob("LFO_FILT", "FILTER", 904, 200, 40);
    addSwitch("LFO_MW_OSC", "MWHL OSC", 812, 279, 20, 52);
    addSwitch("LFO_MW_FLT", "MWHL FLT", 853, 280, 20, 52);
    addSwitch("LFO_MODE", "MODE", 888, 279, 20, 52);
    addSwitch("LFO_SYNC", "SYNC", 920, 277, 20, 58);
    addKnob("DLY_TIME", "TIME", 977, 131, 40);
    addKnob("DLY_REGEN", "REGEN", 977, 200, 40);
    addKnob("DLY_AMOUNT", "AMOUNT", 977, 270, 40);
    addBottomKnob("PWM_LFO_RATE", "PWM RATE", 451, 308, 25);
    addBottomKnob("PWM_LFO_DEPTH", "PWM DEPTH", 501, 308, 25);
    
    updateLabels();
}

SE02_ControllerAudioProcessorEditor::~SE02_ControllerAudioProcessorEditor()
{
    setLookAndFeel(nullptr);
}

void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    cy -= 18; // Down by 2 pixels from previous -20
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - size / 2;
    int y = cy - (size / 2 + 10);
    comp->slider.setBounds(x, y, size, size + 20);
    mainPanel->addAndMakeVisible(comp->slider);

    // Name labels are baked into the background image, so we do not display JUCE text labels.
    // comp->label.setText(name, juce::dontSendNotification);
    // comp->label.setJustificationType(juce::Justification::centred);
    // comp->label.setFont(juce::Font(12.0f, juce::Font::plain));
    // comp->label.setColour(juce::Label::textColourId, juce::Colours::white);
    // comp->label.setBounds(x - 20, y - 20, size + 40, 16); // Name above knob
    // mainPanel->addAndMakeVisible(comp->label);


    comp->slider.onValueChange = [comp = comp.get()]() {
    };

    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.apvts, id, comp->slider);

    sliders[id] = std::move(comp);
}

void SE02_ControllerAudioProcessorEditor::addBottomKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - size / 2;
    int y = cy - size / 2;
    comp->slider.setBounds(x, y, size, size);
    mainPanel->addAndMakeVisible(comp->slider);

    comp->label.setText(name, juce::dontSendNotification);
    comp->label.setJustificationType(juce::Justification::centred);
    comp->label.setFont(juce::Font(10.0f, juce::Font::plain));
    comp->label.setColour(juce::Label::textColourId, juce::Colours::white);
    comp->label.setBounds(x - 20, y - 14, size + 40, 12);
    mainPanel->addAndMakeVisible(comp->label);

    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.apvts, id, comp->slider);

    sliders[id] = std::move(comp);
}

void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    cy -= 30; // Down by 5 pixels from previous -35
    width = width / 2;
    height = height / 2;
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - width / 2;
    int y = cy - height / 2;
    comp->slider.setBounds(x, y, width, height + 16);
    comp->slider.setLookAndFeel(&switchLookAndFeel);
    comp->slider.setAlpha(0.5f); // 50% transparent
    mainPanel->addAndMakeVisible(comp->slider);

    // Labels are baked into background
    // comp->label.setText(name, juce::dontSendNotification);
    // comp->label.setJustificationType(juce::Justification::centred);
    // comp->label.setFont(juce::Font(12.0f, juce::Font::plain));
    // comp->label.setColour(juce::Label::textColourId, juce::Colours::white);
    // comp->label.setBounds(x - 20, y - 20, width + 40, 16); 
    // mainPanel->addAndMakeVisible(comp->label);


    comp->slider.onValueChange = [comp = comp.get()]() {
    };

    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.apvts, id, comp->slider);

    sliders[id] = std::move(comp);
}

void SE02_ControllerAudioProcessorEditor::paint (juce::Graphics& g)
{
    // Painting handled by MainPanel
}

void SE02_ControllerAudioProcessorEditor::resized()
{
    if (mainPanel != nullptr) {
        float scale = (float)getHeight() / 330.0f;
        mainPanel->setTransform(juce::AffineTransform::scale(scale));
    }

    int w = getWidth();
    int h = getHeight();
    
    // Original design was 1024x330. We scale positions.
    float scaleX = w / 1024.0f;
    float scaleY = h / 330.0f;

    resizer.setBounds(w - 16, h - 16, 16, 16);
    



    presetPrevBtn.setBounds(10 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);
    presetLabel.setBounds(30 * scaleX, h - (25 * scaleY), 110 * scaleX, 20 * scaleY);
    presetNextBtn.setBounds(140 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);

    bankSelectorMain.setBounds(170 * scaleX, h - (25 * scaleY), 80 * scaleX, 20 * scaleY);
    browseBtn.setBounds(260 * scaleX, h - (25 * scaleY), 70 * scaleX, 20 * scaleY);

    if (presetBrowser != nullptr) presetBrowser->setBounds(0, 0, w, h);
    
    
    

    
    // Right side

    midiInSelector.setBounds(w - (500 * scaleX), h - (25 * scaleY), 100 * scaleX, 20 * scaleY);
    midiOutSelector.setBounds(w - (390 * scaleX), h - (25 * scaleY), 100 * scaleX, 20 * scaleY);
    showValuesBtn.setBounds(w - (280 * scaleX), h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
    savePresetBtn.setBounds(w - (200 * scaleX), h - (25 * scaleY), 90 * scaleX, 20 * scaleY);
    loadPresetBtn.setBounds(w - (100 * scaleX), h - (25 * scaleY), 90 * scaleX, 20 * scaleY);



}



void SE02_ControllerAudioProcessorEditor::savePresetToFile(const juce::File& file)
{
    if (file.getFileExtension().toLowerCase() == ".syx") {
        audioProcessor.customPresetSavePath = file.getFullPathName();
        audioProcessor.customPresetSaveName = presetLabel.getText().replaceCharacter('_', ' ');
        audioProcessor.isSavingCustomPreset.store(true);
        audioProcessor.isFetching = true;
        audioProcessor.fetchBankIndex = 5; 
        audioProcessor.fetchPatchIndex = 0;
        audioProcessor.fetchPhase = 2; // Skip Phase 1 (Program Change) to fetch currently playing Edit Buffer
        audioProcessor.fetchTimeoutCounter = 0;
        audioProcessor.sysExRequestPhase = 0;
    }

    juce::StringArray lines;
    lines.add("NAME1(" + audioProcessor.getPatchNameFromSysEx() + ");");
    lines.add("NAME2();");
    lines.add("COM_BENDRANGE(2);");
    lines.add("COM_MOD_SENS(0);");
    lines.add("COM_AFT_SENS1(0);");
    lines.add("COM_AFT_SENS2(0);");
    lines.add("COM_DYNAMICS(0);");
    lines.add("COM_VOLUME(127);");
    lines.add("COM_PWM_RATE(0);");
    lines.add("COM_PWM_DEPTH(0);");
    lines.add("COM_OCT(0);");
    lines.add("COM_TRNS(0);");
    lines.add("COM_TRNS_SW(0);");
    
    auto getVal = [this](const juce::String& id) -> float {
        if (auto* param = audioProcessor.apvts.getParameter(id))
            return param->getValue();
        return 0.0f;
    };
    
    auto formatLine = [&](const juce::String& prmId, const juce::String& apvtsId, int maxDiscrete) {
        float normalizedVal = getVal(apvtsId);
        int val = 0;
        
        if (maxDiscrete == 5) {
            float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};
            float ccVal = normalizedVal * 127.0f;
            float minDist = 999.0f;
            int bestIdx = 0;
            for (int i=0; i<6; ++i) {
                if (std::abs(ccVal - vals[i]) < minDist) {
                    minDist = std::abs(ccVal - vals[i]);
                    bestIdx = i;
                }
            }
            val = bestIdx;
        } else if (maxDiscrete == 2) {
            float vals[3] = {0.0f, 64.0f, 127.0f};
            float ccVal = normalizedVal * 127.0f;
            float minDist = 999.0f;
            int bestIdx = 0;
            for (int i=0; i<3; ++i) {
                if (std::abs(ccVal - vals[i]) < minDist) {
                    minDist = std::abs(ccVal - vals[i]);
                    bestIdx = i;
                }
            }
            val = bestIdx;
        } else if (maxDiscrete == 1) {
            val = normalizedVal > 0.5f ? 1 : 0;
        } else {
            val = juce::roundToInt(normalizedVal * 255.0f);
        }
        
        lines.add(prmId + "(" + juce::String(val) + ");");
    };

    formatLine("CTRL_GLIDE", "GLIDE", -1);
    formatLine("CTRL_GLIDE_TYPE", "GLIDE_TYPE", 1);
    formatLine("CTRL_WHL", "WHL_MIX", -1);
    
    formatLine("OSC_RANGE1", "OSC1_RANGE", 5);
    formatLine("OSC_RANGE2", "OSC2_RANGE", 5);
    formatLine("OSC_RANGE3", "OSC3_RANGE", 5);
    
    formatLine("OSC_FINE1", "OSC2_FINE", -1);
    formatLine("OSC_FINE2", "OSC3_FINE", -1);
    
    formatLine("OSC_WAVEFORM1", "OSC1_WAVE", 5);
    formatLine("OSC_WAVEFORM2", "OSC2_WAVE", 5);
    formatLine("OSC_WAVEFORM3", "OSC3_WAVE", 5);
    
    formatLine("OSC_SYNC", "SYNC", 1);
    formatLine("OSC_ENV1", "ENV1", -1);
    formatLine("OSC_KYBD", "KYBD", 1);
    formatLine("OSC_XMOD", "XMOD_MW", 2); // wait XMOD is 3-pos (0,1,2)? My apvts says switch
    
    formatLine("XMOD_O2FLT", "XMOD_O2FLT", -1);
    formatLine("XMOD_O3TO", "XMOD_O3O2", -1);
    formatLine("XMOD_O3PW", "XMOD_O3PW", -1);
    
    formatLine("MIX_OSC1", "MIX_OSC1", -1);
    formatLine("MIX_OSC2", "MIX_OSC2", -1);
    formatLine("MIX_OSC3", "MIX_OSC3", -1);
    formatLine("MIX_FEEDBACK", "MIX_FBACK", -1);
    formatLine("MIX_NOISE", "MIX_NOISE", -1);
    
    formatLine("FLT_CUTOFF", "CUTOFF", -1);
    formatLine("FLT_ATTACK1", "FILT_ATTACK", -1);
    formatLine("FLT_ATTACK2", "AMP_ATTACK", -1);
    formatLine("FLT_EMPHASIS", "EMPHASIS", -1);
    formatLine("FLT_DECAY1", "FILT_DECAY", -1);
    formatLine("FLT_DECAY2", "AMP_DECAY", -1);
    formatLine("FLT_KEY13", "KEYTRACK_13", 1);
    formatLine("FLT_KEY23", "KEYTRACK_23", 1);
    formatLine("FLT_SUSTAIN1", "FILT_SUSTAIN", -1);
    formatLine("FLT_SUSTAIN2", "AMP_SUSTAIN", -1);
    formatLine("FLT_CONTOUR", "CONTOUR", -1);
    formatLine("FLT_MTRIG", "MTRIG", 1);
    formatLine("FLT_NORM", "INVERT", 1);
    formatLine("FLT_REL", "REL", 2);
    formatLine("FLT_GATE", "GATE_LFO", 2);
    
    formatLine("LFO_RATE", "LFO_RATE", -1);
    formatLine("LFO_OSC", "LFO_OSC", -1);
    formatLine("LFO_WAVE", "LFO_WAVE", 5);
    formatLine("LFO_FILTER", "LFO_FILT", -1);
    formatLine("LFO_OSC_SEL", "LFO_MW_OSC", 1);
    formatLine("LFO_FLT", "LFO_MW_FLT", 1);
    formatLine("LFO_MODE", "LFO_MODE", 2);
    formatLine("LFO_SYNC", "LFO_SYNC", 1);
    
    formatLine("DLY_TIME", "DLY_TIME", -1);
    formatLine("DLY_REGEN", "DLY_REGEN", -1);
    formatLine("DLY_AMOUNT", "DLY_AMOUNT", -1);

    file.replaceWithText(lines.joinIntoString("\n") + "\n");
}


void SE02_ControllerAudioProcessorEditor::loadPresetFromFile(const juce::File& file)
{
    if (file.getFileExtension().toLowerCase() == ".syx") {
        juce::MemoryBlock block;
        if (file.loadFileAsData(block) && block.getSize() == 240) {
            
            // Block CCs for 20 timer ticks (approx 660ms) to ensure APVTS updates don't spam the hardware
            audioProcessor.ccBlockTimer.store(20);
            
            // Transmit the pure 240-byte patch directly via SysEx DT1
            audioProcessor.transmitSysExPatch(block);
            
            // Note: In the Pure Pipeline, we bypass the mathematical nibble decoding for transmission,
            // but we use a One-Way Decoder to update the GUI knobs from the binary data so the UI reflects the patch.
            audioProcessor.updateGuiFromSysEx(block);
        }
    }
    else if (file.getFileExtension().toLowerCase() == ".prm") {
        juce::StringArray lines;
        file.readLines(lines);
        
        auto setVal = [this](const juce::String& apvtsId, int rawVal, int maxDiscrete) {
            if (auto* param = audioProcessor.apvts.getParameter(apvtsId)) {
                float normalized = 0.0f;
                if (maxDiscrete == 5) {
                    float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};
                    normalized = vals[juce::jlimit(0, 5, rawVal)] / 127.0f;
                } else if (maxDiscrete == 2) {
                    float vals[3] = {0.0f, 64.0f, 127.0f};
                    normalized = vals[juce::jlimit(0, 2, rawVal)] / 127.0f;
                } else if (maxDiscrete == 1) {
                    normalized = rawVal > 0 ? 1.0f : 0.0f;
                } else {
                    normalized = (float)rawVal / 255.0f;
                }
                param->setValueNotifyingHost(normalized);
            }
        };

        for (auto line : lines) {
            int startBracket = line.indexOfChar('(');
            int endBracket = line.indexOfChar(')');
            if (startBracket > 0 && endBracket > startBracket) {
                juce::String key = line.substring(0, startBracket).trim();
                
                if (key == "NAME1") {
                    juce::String nameStr = line.substring(startBracket + 1, endBracket).trim();
                    juce::String padded = nameStr.paddedRight(' ', 16);
                    for (int i = 0; i < 16; ++i) {
                        audioProcessor.currentSysExBuffer[208 + i].store((float)padded[i]);
                    }
                    continue;
                }
                
                int val = line.substring(startBracket + 1, endBracket).trim().getIntValue();
                
                if (key == "CTRL_GLIDE") setVal("GLIDE", val, -1);
                else if (key == "CTRL_GLIDE_TYPE") setVal("GLIDE_TYPE", val, 1);
                else if (key == "CTRL_WHL") setVal("WHL_MIX", val, -1);
                else if (key == "OSC_RANGE1") setVal("OSC1_RANGE", val, 5);
                else if (key == "OSC_RANGE2") setVal("OSC2_RANGE", val, 5);
                else if (key == "OSC_RANGE3") setVal("OSC3_RANGE", val, 5);
                else if (key == "OSC_FINE1") setVal("OSC2_FINE", val, -1);
                else if (key == "OSC_FINE2") setVal("OSC3_FINE", val, -1);
                else if (key == "OSC_WAVEFORM1") setVal("OSC1_WAVE", val, 5);
                else if (key == "OSC_WAVEFORM2") setVal("OSC2_WAVE", val, 5);
                else if (key == "OSC_WAVEFORM3") setVal("OSC3_WAVE", val, 5);
                else if (key == "OSC_SYNC") setVal("SYNC", val, 1);
                else if (key == "OSC_ENV1") setVal("ENV1", val, -1);
                else if (key == "OSC_KYBD") setVal("KYBD", val, 1);
                else if (key == "OSC_XMOD") setVal("XMOD_MW", val, 2);
                else if (key == "XMOD_O2FLT") setVal("XMOD_O2FLT", val, -1);
                else if (key == "XMOD_O3TO") setVal("XMOD_O3O2", val, -1);
                else if (key == "XMOD_O3PW") setVal("XMOD_O3PW", val, -1);
                else if (key == "MIX_OSC1") setVal("MIX_OSC1", val, -1);
                else if (key == "MIX_OSC2") setVal("MIX_OSC2", val, -1);
                else if (key == "MIX_OSC3") setVal("MIX_OSC3", val, -1);
                else if (key == "MIX_FEEDBACK") setVal("MIX_FBACK", val, -1);
                else if (key == "MIX_NOISE") setVal("MIX_NOISE", val, -1);
                else if (key == "FLT_CUTOFF") setVal("CUTOFF", val, -1);
                else if (key == "FLT_ATTACK1") setVal("FILT_ATTACK", val, -1);
                else if (key == "FLT_ATTACK2") setVal("AMP_ATTACK", val, -1);
                else if (key == "FLT_EMPHASIS") setVal("EMPHASIS", val, -1);
                else if (key == "FLT_DECAY1") setVal("FILT_DECAY", val, -1);
                else if (key == "FLT_DECAY2") setVal("AMP_DECAY", val, -1);
                else if (key == "FLT_KEY13") setVal("KEYTRACK_13", val, 1);
                else if (key == "FLT_KEY23") setVal("KEYTRACK_23", val, 1);
                else if (key == "FLT_SUSTAIN1") setVal("FILT_SUSTAIN", val, -1);
                else if (key == "FLT_SUSTAIN2") setVal("AMP_SUSTAIN", val, -1);
                else if (key == "FLT_CONTOUR") setVal("CONTOUR", val, -1);
                else if (key == "FLT_MTRIG") setVal("MTRIG", val, 1);
                else if (key == "FLT_NORM") setVal("INVERT", val, 1);
                else if (key == "FLT_REL") setVal("REL", val, 2);
                else if (key == "FLT_GATE") setVal("GATE_LFO", val, 2);
                else if (key == "LFO_RATE") setVal("LFO_RATE", val, -1);
                else if (key == "LFO_OSC") setVal("LFO_OSC", val, -1);
                else if (key == "LFO_WAVE") setVal("LFO_WAVE", val, 5);
                else if (key == "LFO_FILTER") setVal("LFO_FILT", val, -1);
                else if (key == "LFO_OSC_SEL") setVal("LFO_MW_OSC", val, 1);
                else if (key == "LFO_FLT") setVal("LFO_MW_FLT", val, 1);
                else if (key == "LFO_MODE") setVal("LFO_MODE", val, 2);
                else if (key == "LFO_SYNC") setVal("LFO_SYNC", val, 1);
                else if (key == "DLY_TIME") setVal("DLY_TIME", val, -1);
                else if (key == "DLY_REGEN") setVal("DLY_REGEN", val, -1);
                else if (key == "DLY_AMOUNT") setVal("DLY_AMOUNT", val, -1);
            }
        }
        presetLabel.setText(audioProcessor.getPatchNameFromSysEx(), juce::dontSendNotification);
        return;
    }

    juce::MemoryBlock block;
    if (file.loadFileAsData(block)) {
        if (block.getSize() == 256) {
            for (int i = 0; i < 256; ++i) {
                juce::String paramId = audioProcessor.syxParamMap[i];
                if (paramId.isNotEmpty()) {
                    float hwVal = (float)(juce::uint8)block[i];
                    if (auto* param = audioProcessor.apvts.getParameter(paramId)) {
                        float mappedVal = audioProcessor.sysexToCc(paramId, hwVal);
                        param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                    }
                }
            }
        }
    }
}

std::map<juce::String, float> SE02_ControllerAudioProcessorEditor::getPresetState(const juce::File& file, juce::String& outName)
{
    std::map<juce::String, float> state;
    outName = "Unknown";
    
    if (file.getFileExtension().toLowerCase() == ".syx") {
        juce::MemoryBlock block;
        file.loadFileAsData(block);
        if (block.getSize() == 240 || block.getSize() == 256) {
            outName = juce::String::createStringFromData((const char*)block.getData() + 208, 16).trim();
            for (int i = 0; i < 107; ++i) {
                if (audioProcessor.syxParamMap.find(i) != audioProcessor.syxParamMap.end()) {
                    juce::uint8 highNibble = block[i * 2];
                    juce::uint8 lowNibble = block[i * 2 + 1];
                    juce::uint8 hwVal = (highNibble << 4) | (lowNibble & 0x0F);
                    
                    juce::String apvtsId = audioProcessor.syxParamMap[i];
                    float ccVal = audioProcessor.sysexToCc(apvtsId, (float)hwVal);
                    state[apvtsId] = ccVal / 127.0f;
                }
            }
        }
    }
    else if (file.getFileExtension().toLowerCase() == ".prm") {
        juce::StringArray lines;
        file.readLines(lines);
        
        auto setVal = [&state](const juce::String& apvtsId, int rawVal, int maxDiscrete) {
            float normalized = 0.0f;
            if (maxDiscrete == 5) {
                float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};
                normalized = vals[juce::jlimit(0, 5, rawVal)] / 127.0f;
            } else if (maxDiscrete == 2) {
                float vals[3] = {0.0f, 64.0f, 127.0f};
                normalized = vals[juce::jlimit(0, 2, rawVal)] / 127.0f;
            } else if (maxDiscrete == 1) {
                normalized = rawVal > 0 ? 1.0f : 0.0f;
            } else {
                normalized = (float)rawVal / 255.0f;
            }
            state[apvtsId] = normalized;
        };

        for (auto line : lines) {
            int startBracket = line.indexOfChar('(');
            int endBracket = line.indexOfChar(')');
            if (startBracket > 0 && endBracket > startBracket) {
                juce::String key = line.substring(0, startBracket).trim();
                
                if (key == "NAME1") {
                    outName = line.substring(startBracket + 1, endBracket).trim();
                    continue;
                }
                
                int val = line.substring(startBracket + 1, endBracket).trim().getIntValue();
                
                if (key == "CTRL_GLIDE") setVal("GLIDE", val, -1);
                else if (key == "CTRL_GLIDE_TYPE") setVal("GLIDE_TYPE", val, 1);
                else if (key == "CTRL_WHL") setVal("WHL_MIX", val, -1);
                else if (key == "OSC_RANGE1") setVal("OSC1_RANGE", val, 5);
                else if (key == "OSC_RANGE2") setVal("OSC2_RANGE", val, 5);
                else if (key == "OSC_RANGE3") setVal("OSC3_RANGE", val, 5);
                else if (key == "OSC_FINE1") setVal("OSC2_FINE", val, -1);
                else if (key == "OSC_FINE2") setVal("OSC3_FINE", val, -1);
                else if (key == "OSC_WAVEFORM1") setVal("OSC1_WAVE", val, 5);
                else if (key == "OSC_WAVEFORM2") setVal("OSC2_WAVE", val, 5);
                else if (key == "OSC_WAVEFORM3") setVal("OSC3_WAVE", val, 5);
                else if (key == "OSC_SYNC") setVal("SYNC", val, 1);
                else if (key == "OSC_ENV1") setVal("ENV1", val, -1);
                else if (key == "OSC_KYBD") setVal("KYBD", val, 1);
                else if (key == "OSC_XMOD") setVal("XMOD_MW", val, 2);
                else if (key == "XMOD_O2FLT") setVal("XMOD_O2FLT", val, -1);
                else if (key == "XMOD_O3TO") setVal("XMOD_O3O2", val, -1);
                else if (key == "XMOD_O3PW") setVal("XMOD_O3PW", val, -1);
                else if (key == "MIX_OSC1") setVal("MIX_OSC1", val, -1);
                else if (key == "MIX_OSC2") setVal("MIX_OSC2", val, -1);
                else if (key == "MIX_OSC3") setVal("MIX_OSC3", val, -1);
                else if (key == "MIX_FEEDBACK") setVal("MIX_FBACK", val, -1);
                else if (key == "MIX_NOISE") setVal("MIX_NOISE", val, -1);
                else if (key == "FLT_CUTOFF") setVal("CUTOFF", val, -1);
                else if (key == "FLT_ATTACK1") setVal("FILT_ATTACK", val, -1);
                else if (key == "FLT_ATTACK2") setVal("AMP_ATTACK", val, -1);
                else if (key == "FLT_EMPHASIS") setVal("EMPHASIS", val, -1);
                else if (key == "FLT_DECAY1") setVal("FILT_DECAY", val, -1);
                else if (key == "FLT_DECAY2") setVal("AMP_DECAY", val, -1);
                else if (key == "FLT_KEY13") setVal("KEYTRACK_13", val, 1);
                else if (key == "FLT_KEY23") setVal("KEYTRACK_23", val, 1);
                else if (key == "FLT_SUSTAIN1") setVal("FILT_SUSTAIN", val, -1);
                else if (key == "FLT_SUSTAIN2") setVal("AMP_SUSTAIN", val, -1);
                else if (key == "FLT_CONTOUR") setVal("CONTOUR", val, -1);
                else if (key == "FLT_MTRIG") setVal("MTRIG", val, 1);
                else if (key == "FLT_NORM") setVal("INVERT", val, 1);
                else if (key == "FLT_REL") setVal("REL", val, 2);
                else if (key == "FLT_GATE") setVal("GATE_LFO", val, 2);
                else if (key == "LFO_RATE") setVal("LFO_RATE", val, -1);
                else if (key == "LFO_OSC") setVal("LFO_OSC", val, -1);
                else if (key == "LFO_WAVE") setVal("LFO_WAVE", val, 5);
                else if (key == "LFO_FILTER") setVal("LFO_FILT", val, -1);
                else if (key == "LFO_OSC_SEL") setVal("LFO_MW_OSC", val, 1);
                else if (key == "LFO_FLT") setVal("LFO_MW_FLT", val, 1);
                else if (key == "LFO_MODE") setVal("LFO_MODE", val, 2);
                else if (key == "LFO_SYNC") setVal("LFO_SYNC", val, 1);
                else if (key == "DLY_TIME") setVal("DLY_TIME", val, -1);
                else if (key == "DLY_REGEN") setVal("DLY_REGEN", val, -1);
                else if (key == "DLY_AMOUNT") setVal("DLY_AMOUNT", val, -1);
            }
        }
    }
    
    return state;
}
