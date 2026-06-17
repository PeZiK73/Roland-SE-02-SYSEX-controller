import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Make SAVE PRESET bounds wider
# OLD: savePresetBtn.setBounds(w - (175 * scaleX), h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
content = content.replace("w - (175 * scaleX), h - (25 * scaleY), 70 * scaleX", "w - (195 * scaleX), h - (25 * scaleY), 90 * scaleX")

save_logic = '''
    savePresetBtn.onClick = [this] {
        juce::File customPresetsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
            .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
            .getChildFile("CUSTOM_PRESETS");
        
        if (!customPresetsDir.exists())
            customPresetsDir.createDirectory();
            
        juce::Time now = juce::Time::getCurrentTime();
        juce::String defaultName = "Preset_" + now.formatted("%Y%m%d_%H%M%S") + ".PRM";
        
        fileChooser = std::make_unique<juce::FileChooser> (
            "Save Preset...",
            customPresetsDir.getChildFile(defaultName),
            "*.PRM"
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
'''

content = content.replace("    updateLabels();", save_logic)

save_func = '''
void SE02_ControllerAudioProcessorEditor::savePresetToFile(const juce::File& file)
{
    juce::StringArray lines;
    lines.add("NAME1(Inbound);");
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
        
        if (maxDiscrete == 5) val = juce::roundToInt(normalizedVal * 5.0f);
        else if (maxDiscrete == 2) val = juce::roundToInt(normalizedVal * 2.0f);
        else if (maxDiscrete == 1) val = normalizedVal > 0.5f ? 1 : 0;
        else val = juce::roundToInt(normalizedVal * 255.0f);
        
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

    file.replaceWithText(lines.joinIntoString("\\n") + "\\n");
}
'''

content += "\n" + save_func

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
