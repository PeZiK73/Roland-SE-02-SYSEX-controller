import sys

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

if "juce::String getPatchNameFromSysEx();" not in content:
    content = content.replace("void sendProgramChange();", "void sendProgramChange();\n    juce::String getPatchNameFromSysEx();")
    with open('Source/PluginProcessor.h', 'w') as f:
        f.write(content)
        print("Updated PluginProcessor.h")

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

func = """juce::String SE02_ControllerAudioProcessor::getPatchNameFromSysEx()
{
    juce::String name = "";
    bool hasData = false;
    for (int i = 0; i < 16; ++i) {
        float val = incomingSysExValues[i].load();
        if (val >= 0.0f) hasData = true;
        if (val >= 32.0f && val <= 126.0f) {
            name += juce::String::charToString((juce::juce_wchar)val);
        } else if (hasData) {
            name += " ";
        }
    }
    name = name.trim();
    if (name.isEmpty() || !hasData) return "Inbound";
    return name;
}
"""

if "getPatchNameFromSysEx" not in content:
    content = content.replace("juce::String SE02_ControllerAudioProcessor::getBankName(int index)", func + "\njuce::String SE02_ControllerAudioProcessor::getBankName(int index)")
    
    # Replace the hardcoded string
    content = content.replace('lines.add("NAME1(Inbound);");', 'lines.add("NAME1(" + getPatchNameFromSysEx() + ");");')
    
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Updated PluginProcessor.cpp")

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

if 'lines.add("NAME1(" + audioProcessor.getPatchNameFromSysEx() + ");");' not in content:
    content = content.replace('lines.add("NAME1(Inbound);");', 'lines.add("NAME1(" + audioProcessor.getPatchNameFromSysEx() + ");");')
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(content)
        print("Updated PluginEditor.cpp")

