import re

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/scratch/generate.py", "r") as f:
    code = f.read()

processor_additions = """
void SE02_ControllerAudioProcessor::openMidiInput(const juce::String& identifier)
{
    auto devs = juce::MidiInput::getAvailableDevices();
    for (auto& dev : devs) {
        if (dev.identifier == identifier) {
            hardwareMidiIn = juce::MidiInput::openDevice(dev.identifier, this);
            if (hardwareMidiIn) hardwareMidiIn->start();
            break;
        }
    }
}

void SE02_ControllerAudioProcessor::openMidiOutput(const juce::String& identifier)
{
    auto devs = juce::MidiOutput::getAvailableDevices();
    for (auto& dev : devs) {
        if (dev.identifier == identifier) {
            hardwareMidiOut = juce::MidiOutput::openDevice(dev.identifier);
            break;
        }
    }
}

void SE02_ControllerAudioProcessor::handleIncomingMidiMessage(juce::MidiInput* source, const juce::MidiMessage& msg)
{
    if (msg.isSysEx())
    {
        auto data = msg.getRawData();
        int size = msg.getRawDataSize();
        
        // F0 41 10 00 00 00 44 12
        if (size > 14 && data[1] == 0x41 && data[6] == 0x44 && data[7] == 0x12)
        {
            if (data[8] == 0x05 && data[9] == 0x00)
            {
                int baseAddress = data[10] * 128 + data[11];
                int payloadOffset = 0;
                
                if (baseAddress == 0x00) payloadOffset = 0;       // 00 00
                else if (baseAddress == 0x40) payloadOffset = 32; // 00 40
                else if (baseAddress == 0x80) payloadOffset = 64; // 01 00
                else if (baseAddress == 0xC0) payloadOffset = 96; // 01 40
                else return;
                
                const juce::uint8* nibbles = data + 12;
                int nibbleCount = size - 14;
                int byteCount = nibbleCount / 2;
                
                for (int i = 0; i < byteCount; ++i)
                {
                    if (payloadOffset + i < 120)
                    {
                        juce::uint8 b = ((nibbles[i*2] & 0x0F) << 4) | (nibbles[i*2+1] & 0x0F);
                        incomingSysExValues[payloadOffset + i].store((float)b);
                    }
                }
            }
        }
    }
        
    if (msg.isController())
    {
        int ccNum = msg.getControllerNumber();
        float val = (float)msg.getControllerValue();
        incomingCcValues[ccNum].store(val);
        
        for (auto& cp : ccParams)
        {
            if (cp.ccNumber == ccNum)
            {
                cp.lastValue = val;
            }
        }
    }
}
"""

# Inject before createEditor
code = code.replace("juce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor()", processor_additions + "\njuce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor()")

# Redirect requestSysExPreset to use hardwareMidiOut if available
sys_req_repl = """
    auto sendRQ1 = [&](juce::uint8 a2, juce::uint8 a3, juce::uint8 s3) {
        juce::uint8 sysexData[] = {
            0xF0, 0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 
            0x05, 0x00, a2, a3, 
            0x00, 0x00, 0x00, s3, 
            0x00, 0xF7
        };
        int sum = 0x05 + 0x00 + a2 + a3 + 0x00 + 0x00 + 0x00 + s3;
        sysexData[16] = (128 - (sum % 128)) % 128;
        juce::MidiMessage rq1(sysexData, sizeof(sysexData));
        if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(rq1);
        else midiOutputQueue.addEvent(rq1, 0);
    };
"""
code = re.sub(r'    auto sendRQ1 = \[\&\]\(juce::uint8 a2, juce::uint8 a3, juce::uint8 s3\) \{.*?        midiOutputQueue\.addEvent\(rq1, 0\);\n    \};', sys_req_repl, code, flags=re.DOTALL)


editor_header_repl = """
#include "PluginProcessor.h"
#include "PluginEditor.h"

// We need to add ComboBox members to the PluginEditor.h, but generate.py does not write PluginEditor.h!
// I will patch it externally.
"""

editor_cpp_repl = """
    mainPanel->addAndMakeVisible(readPresetBtn);

    midiInBox.setBounds(860, 305, 120, 20);
    midiInBox.setTextWhenNothingSelected("MIDI Input...");
    mainPanel->addAndMakeVisible(midiInBox);

    midiOutBox.setBounds(990, 305, 120, 20);
    midiOutBox.setTextWhenNothingSelected("MIDI Output...");
    mainPanel->addAndMakeVisible(midiOutBox);

    auto inDevices = juce::MidiInput::getAvailableDevices();
    for (auto& dev : inDevices) midiInBox.addItem(dev.name, midiInBox.getNumItems() + 1);
    
    auto outDevices = juce::MidiOutput::getAvailableDevices();
    for (auto& dev : outDevices) midiOutBox.addItem(dev.name, midiOutBox.getNumItems() + 1);
    
    midiInBox.onChange = [this]() {
        auto devs = juce::MidiInput::getAvailableDevices();
        int idx = midiInBox.getSelectedItemIndex();
        if (idx >= 0 && idx < devs.size()) audioProcessor.openMidiInput(devs[idx].identifier);
    };
    
    midiOutBox.onChange = [this]() {
        auto devs = juce::MidiOutput::getAvailableDevices();
        int idx = midiOutBox.getSelectedItemIndex();
        if (idx >= 0 && idx < devs.size()) audioProcessor.openMidiOutput(devs[idx].identifier);
    };
"""

code = code.replace("    mainPanel->addAndMakeVisible(readPresetBtn);", editor_cpp_repl)


with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/scratch/generate.py", "w") as f:
    f.write(code)

print("generate.py rewritten for hardware MIDI.")
