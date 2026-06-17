import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

content = content.replace("juce::TextButton readPresetBtn{\\"READ PRESET\\"};", "juce::TextButton loadPresetBtn{\\"LOAD PRESET\\"};")
content = content.replace("void savePresetToFile(const juce::File& file);", "void savePresetToFile(const juce::File& file);\n    void loadPresetFromFile(const juce::File& file);")

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

content = content.replace("readPresetBtn", "loadPresetBtn")

load_logic = '''loadPresetBtn.onClick = [this] {
        juce::File customPresetsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
            .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
            .getChildFile("CUSTOM_PRESETS");
            
        fileChooser = std::make_unique<juce::FileChooser> (
            "Load Preset...",
            customPresetsDir,
            "*.PRM"
        );
        
        auto chooserFlags = juce::FileBrowserComponent::openMode | juce::FileBrowserComponent::canSelectFiles;
        
        fileChooser->launchAsync(chooserFlags, [this] (const juce::FileChooser& fc) {
            juce::File file = fc.getResult();
            if (file != juce::File{}) {
                loadPresetFromFile(file);
            }
        });
    };'''

content = re.sub(r'loadPresetBtn\.onClick = \[this\] \{ audioProcessor\.requestSysExPreset\(\); \};', load_logic, content)


load_func = '''
void SE02_ControllerAudioProcessorEditor::loadPresetFromFile(const juce::File& file)
{
    juce::StringArray lines;
    file.readLines(lines);
    
    auto setVal = [this](const juce::String& apvtsId, int rawVal, int maxDiscrete) {
        if (auto* param = audioProcessor.apvts.getParameter(apvtsId)) {
            float normalized = 0.0f;
            if (maxDiscrete == 5) {
                normalized = (float)rawVal / 5.0f;
            } else if (maxDiscrete == 2) {
                normalized = (float)rawVal / 2.0f;
            } else if (maxDiscrete == 1) {
                normalized = rawVal > 0 ? 1.0f : 0.0f;
            } else {
                normalized = (float)rawVal / 255.0f;
            }
            param->setValueNotifyingHost(normalized);
            
            for (auto& cp : audioProcessor.ccParams) {
                if (cp.id == apvtsId) {
                    // Update APVTS correctly. The processBlock will handle sending the MIDI automatically 
                    // because the APVTS value has changed and cp.lastValue is still the old value.
                }
            }
        }
    };

    for (auto line : lines) {
        int startBracket = line.indexOfChar('(');
        int endBracket = line.indexOfChar(')');
        if (startBracket > 0 && endBracket > startBracket) {
            juce::String key = line.substring(0, startBracket).trim();
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
'''

content += "\n" + load_func

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
