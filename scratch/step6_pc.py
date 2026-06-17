import re

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

content = content.replace("int currentPreset = 1; // 1 to 128", "int currentPreset = 1; // 1 to 128\n    std::atomic<int> sysExDelayCounter {-1};")

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    cpp_content = f.read()

# Fix the MSB Bank mapping and trigger sysExDelayCounter
pc_logic = '''void SE02_ControllerAudioProcessor::sendProgramChange()
{
    // MSB Bank A=0, B=1, C=2, USER=3, D=4
    // LSB is always 0
    int msb = currentBankIndex;
    int lsb = 0;
    int pc = currentPreset - 1; // 0-127
    
    if (hardwareMidiOut) {
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
        
        // Wait ~330ms before requesting the SysEx patch so the synth has time to load it
        sysExDelayCounter.store(10);
    }
}'''

cpp_content = re.sub(r'void SE02_ControllerAudioProcessor::sendProgramChange\(\)\n\{.*?\n\}', pc_logic, cpp_content, flags=re.DOTALL)

# Add timer check
timer_logic = '''void SE02_ControllerAudioProcessor::timerCallback()
{
    if (sysExDelayCounter.load() > 0) {
        sysExDelayCounter.fetch_sub(1);
    } else if (sysExDelayCounter.load() == 0) {
        sysExDelayCounter.store(-1);
        requestSysExPreset();
    }
'''

cpp_content = cpp_content.replace("void SE02_ControllerAudioProcessor::timerCallback()\n{", timer_logic)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(cpp_content)

