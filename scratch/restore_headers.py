import re

with open('Source/PluginProcessor.h', 'r') as f:
    ph_content = f.read()

if "void openMidiInput" not in ph_content:
    ph_content = ph_content.replace('void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;', 'void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;\n    void openMidiInput(const juce::String& identifier);\n    void openMidiOutput(const juce::String& identifier);')
    with open('Source/PluginProcessor.h', 'w') as f:
        f.write(ph_content)

with open('Source/PluginEditor.h', 'r') as f:
    eh_content = f.read()

if "juce::ComboBox midiInBox;" not in eh_content:
    # Need to properly match the end of the class
    eh_content = re.sub(r'std::map<juce::String, std::unique_ptr<AttachedSlider>> sliders;\s*};', 'std::map<juce::String, std::unique_ptr<AttachedSlider>> sliders;\n    juce::ComboBox midiInBox;\n    juce::ComboBox midiOutBox;\n    juce::TextButton readPresetBtn;\n    juce::TextButton showValuesBtn;\n};', eh_content)
    with open('Source/PluginEditor.h', 'w') as f:
        f.write(eh_content)

print("Restored missing headers")
