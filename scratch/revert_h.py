import re

def fix_processor_h():
    with open('Source/PluginProcessor.h', 'r') as f:
        content = f.read()

    # Remove all the direct hardware MIDI members
    to_remove = [
        r'    juce::MidiInput\* hardwareMidiIn = nullptr;\n',
        r'    juce::MidiOutput\* hardwareMidiOut = nullptr;\n',
        r'    void requestSysExPreset\(\);\n',
        r'    void openMidiInput\(const juce::String& identifier\);\n',
        r'    void openMidiOutput\(const juce::String& identifier\);\n',
        r'    void handleIncomingMidiMessage\(juce::MidiInput\* source, const juce::MidiMessage& message\) override;\n',
        r'    std::atomic<bool> sendRq1Request \{ false \};\n',
        r'    juce::AbstractFifo outgoingMidiFifo\{1024\};\n',
        r'    juce::MidiMessage outgoingMidiBuffer\[1024\];\n',
        r'    std::map<int, juce::String> syxParamMap;\n',
        r'    std::atomic<float> incomingSysExValues\[120\];\n'
    ]
    
    for pat in to_remove:
        content = re.sub(pat, '', content)

    # Make sure it doesn't inherit from MidiInputCallback anymore
    content = content.replace("public juce::AudioProcessor, public juce::Timer, private juce::MidiInputCallback", "public juce::AudioProcessor, public juce::Timer")

    with open('Source/PluginProcessor.h', 'w') as f:
        f.write(content)

fix_processor_h()
print("Processor.h cleaned!")
