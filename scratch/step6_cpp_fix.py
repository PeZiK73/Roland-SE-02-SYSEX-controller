import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Update sysexToCc mapping
content = content.replace("float vals[6] = {0.0f, 26.0f, 51.0f, 77.0f, 102.0f, 127.0f};", "float vals[6] = {10.0f, 32.0f, 53.0f, 74.0f, 95.0f, 116.0f};")

# 2. Add loadGlobalSettings to constructor
content = content.replace('syxParamMap[i] = "";\n    }', 'syxParamMap[i] = "";\n    }\n    loadGlobalSettings();')

# 3. Add to openMidiInput
open_in_old = '''        if (dev.name == identifier) {
            hardwareMidiIn = juce::MidiInput::openDevice(dev.identifier, this);
            if (hardwareMidiIn) {
                hardwareMidiIn->start();
                lastMidiInName = identifier;
            }
            break;
        }'''
open_in_new = '''        if (dev.name == identifier) {
            hardwareMidiIn = juce::MidiInput::openDevice(dev.identifier, this);
            if (hardwareMidiIn) {
                hardwareMidiIn->start();
                lastMidiInName = identifier;
                saveGlobalSettings();
            }
            break;
        }'''
content = content.replace(open_in_old, open_in_new)

# 4. Add to openMidiOutput
open_out_old = '''        if (dev.name == identifier) {
            hardwareMidiOut = juce::MidiOutput::openDevice(dev.identifier);
            if (hardwareMidiOut) lastMidiOutName = identifier;
            break;
        }'''
open_out_new = '''        if (dev.name == identifier) {
            hardwareMidiOut = juce::MidiOutput::openDevice(dev.identifier);
            if (hardwareMidiOut) {
                lastMidiOutName = identifier;
                saveGlobalSettings();
            }
            break;
        }'''
content = content.replace(open_out_old, open_out_new)

# 5. Add function definitions
settings_funcs = '''
void SE02_ControllerAudioProcessor::saveGlobalSettings() {
    juce::File settingsFile = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
        .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
        .getChildFile("settings.xml");
        
    settingsFile.getParentDirectory().createDirectory();
    
    juce::XmlElement xml("SE02_SETTINGS");
    xml.setAttribute("MidiIn", lastMidiInName);
    xml.setAttribute("MidiOut", lastMidiOutName);
    xml.writeTo(settingsFile);
}

void SE02_ControllerAudioProcessor::loadGlobalSettings() {
    juce::File settingsFile = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
        .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
        .getChildFile("settings.xml");
        
    if (settingsFile.existsAsFile()) {
        if (auto xml = juce::XmlDocument::parse(settingsFile)) {
            juce::String midiIn = xml->getStringAttribute("MidiIn");
            juce::String midiOut = xml->getStringAttribute("MidiOut");
            if (midiIn.isNotEmpty()) {
                lastMidiInName = midiIn;
                openMidiInput(midiIn);
            }
            if (midiOut.isNotEmpty()) {
                lastMidiOutName = midiOut;
                openMidiOutput(midiOut);
            }
        }
    }
}
'''
content += settings_funcs

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
