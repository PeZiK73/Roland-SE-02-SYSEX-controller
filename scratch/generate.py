import os

params = [
    # General/Control
    ("GLIDE", "GLIDE", 5, "knob"),
    ("GLIDE_TYPE", "TYPE", 9, "switch"),
    ("WHL_MIX", "WHL MIX", 13, "knob"),
    # Osc 1
    ("OSC1_RANGE", "RANGE", 22, "knob"),
    ("OSC1_TUNE", "TUNE", -1, "knob"),
    ("OSC1_WAVE", "WAVEFORM", 24, "knob"),
    # Osc 2
    ("OSC2_RANGE", "RANGE", 19, "knob"),
    ("OSC2_FINE", "FINE", 27, "knob"),
    ("OSC2_WAVE", "WAVEFORM", 20, "knob"),
    # Osc 3
    ("OSC3_RANGE", "RANGE", 25, "knob"),
    ("OSC3_FINE", "FINE", 28, "knob"),
    ("OSC3_WAVE", "WAVEFORM", 26, "knob"),
    # Osc settings
    ("SYNC", "SYNC", 21, "switch"),
    ("ENV1", "ENV1", 29, "knob"),
    ("KYBD", "KYBD", 30, "switch"),
    ("XMOD_MW", "TO MW", 31, "switch"),
    # XMOD
    ("XMOD_O2FLT", "O2-FILTER", 16, "knob"),
    ("XMOD_O3O2", "O3-O2", 17, "knob"),
    ("XMOD_O3PW", "O3-PW1,2", 18, "knob"),
    # Mixer
    ("MIX_OSC1", "OSC 1", 48, "knob"),
    ("MIX_OSC2", "OSC 2", 49, "knob"),
    ("MIX_OSC3", "OSC 3", 50, "knob"),
    ("MIX_FBACK", "FEEDBACK", 51, "knob"),
    ("MIX_NOISE", "NOISE", 41, "knob"),
    # Filter
    ("CUTOFF", "CUTOFF", 74, "knob"),
    ("EMPHASIS", "EMPHASIS", 71, "knob"),
    ("CONTOUR", "CONTOUR", 59, "knob"),
    ("KEYTRACK_13", "1/3", 57, "switch"),
    ("KEYTRACK_23", "2/3", 58, "switch"),
    ("MTRIG", "MTRIG", 60, "switch"),
    ("INVERT", "INVERT", 61, "switch"),
    ("REL", "REL", 62, "switch"),
    ("GATE_LFO", "LFO/GATE", 63, "switch"),
    # Envelopes
    ("FILT_ATTACK", "ATTACK", 47, "knob"),
    ("FILT_DECAY", "DECAY", 52, "knob"),
    ("FILT_SUSTAIN", "SUSTAIN", 53, "knob"),
    ("AMP_ATTACK", "ATTACK", 73, "knob"),
    ("AMP_DECAY", "DECAY", 75, "knob"),
    ("AMP_SUSTAIN", "SUSTAIN", 56, "knob"),
    # LFO
    ("LFO_RATE", "RATE", 102, "knob"),
    ("LFO_WAVE", "WAVE", 104, "knob"),
    ("LFO_OSC", "OSC", 103, "knob"),
    ("LFO_FILT", "FILTER", 105, "knob"),
    ("LFO_MW_OSC", "MWHL-OSC", 106, "switch"),
    ("LFO_MW_FLT", "MWHL-FLT", 107, "switch"),
    ("LFO_MODE", "MODE", 108, "switch"),
    ("LFO_SYNC", "SYNC", 109, "switch"),
    # Delay
    ("DLY_TIME", "TIME", 82, "knob"),
    ("DLY_REGEN", "REGEN", 83, "knob"),
    ("DLY_AMOUNT", "AMOUNT", 91, "knob")
]

proc_code = """#include "PluginProcessor.h"
#include <fstream>
#include "PluginEditor.h"

SE02_ControllerAudioProcessor::SE02_ControllerAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                     #endif
                       ),
       apvts(*this, nullptr, "Parameters", createParameterLayout())
#endif
{
    for (int i = 0; i < 128; ++i)
        incomingCcValues[i].store(-1.0f);

    startTimerHz(30);

    for (int i = 0; i < 120; ++i) {
        incomingSysExValues[i].store(-1.0f);
        syxParamMap[i] = "";
    }
    
    syxParamMap[20] = "GLIDE";
    syxParamMap[21] = "GLIDE_TYPE";
    syxParamMap[22] = "WHL_MIX";
    
    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    // syxParamMap[25] = "OSC1_TUNE";
    syxParamMap[29] = "OSC2_FINE";
    syxParamMap[30] = "OSC3_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";
    syxParamMap[32] = "OSC2_WAVE";
    syxParamMap[33] = "OSC3_WAVE";
    syxParamMap[34] = "SYNC";
    syxParamMap[35] = "ENV1";
    syxParamMap[36] = "KYBD";
    syxParamMap[37] = "XMOD_MW";
    syxParamMap[42] = "XMOD_O2FLT";
    syxParamMap[43] = "XMOD_O3O2";
    syxParamMap[44] = "XMOD_O3PW";
    syxParamMap[45] = "MIX_OSC1";
    syxParamMap[46] = "MIX_OSC2";
    syxParamMap[47] = "MIX_OSC3";
    syxParamMap[48] = "MIX_FBACK";
    syxParamMap[49] = "MIX_NOISE";
    
    syxParamMap[55] = "CUTOFF";
    syxParamMap[58] = "EMPHASIS";
    syxParamMap[65] = "CONTOUR";
    syxParamMap[61] = "KEYTRACK_13";
    syxParamMap[62] = "KEYTRACK_23";
    syxParamMap[66] = "MTRIG";
    syxParamMap[67] = "INVERT";
    syxParamMap[68] = "REL";
    syxParamMap[69] = "GATE_LFO";
    syxParamMap[56] = "FILT_ATTACK";
    syxParamMap[59] = "FILT_DECAY";
    syxParamMap[63] = "FILT_SUSTAIN";
    syxParamMap[57] = "AMP_ATTACK";
    syxParamMap[60] = "AMP_DECAY";
    syxParamMap[64] = "AMP_SUSTAIN";
    syxParamMap[75] = "LFO_RATE";
    syxParamMap[77] = "LFO_WAVE";
    syxParamMap[76] = "LFO_OSC";
    syxParamMap[80] = "LFO_FILT";
    syxParamMap[79] = "LFO_MW_OSC";
    syxParamMap[78] = "LFO_MW_FLT";
    syxParamMap[81] = "LFO_MODE";
    syxParamMap[82] = "LFO_SYNC";
    syxParamMap[100] = "DLY_TIME";
    syxParamMap[101] = "DLY_REGEN";
    syxParamMap[102] = "DLY_AMOUNT";
}

SE02_ControllerAudioProcessor::~SE02_ControllerAudioProcessor() { stopTimer(); }
const juce::String SE02_ControllerAudioProcessor::getName() const { return JucePlugin_Name; }
bool SE02_ControllerAudioProcessor::acceptsMidi() const { return true; }
bool SE02_ControllerAudioProcessor::producesMidi() const { return true; }
bool SE02_ControllerAudioProcessor::isMidiEffect() const { return false; }
double SE02_ControllerAudioProcessor::getTailLengthSeconds() const { return 0.0; }
int SE02_ControllerAudioProcessor::getNumPrograms() { return 1; }
int SE02_ControllerAudioProcessor::getCurrentProgram() { return 0; }
void SE02_ControllerAudioProcessor::setCurrentProgram (int index) {}
const juce::String SE02_ControllerAudioProcessor::getProgramName (int index) { return {}; }
void SE02_ControllerAudioProcessor::changeProgramName (int index, const juce::String& newName) {}

void SE02_ControllerAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    ccParams.clear();
"""

for p in params:
    proc_code += f'    ccParams.push_back({{"{p[0]}", {p[2]}}});\n'

proc_code += """
    for (auto& cp : ccParams)
    {
        cp.param = apvts.getRawParameterValue(cp.id);
        if (cp.param != nullptr)
            cp.lastValue = *cp.param;
    }
}

void SE02_ControllerAudioProcessor::releaseResources() {}
bool SE02_ControllerAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const { return true; }

void SE02_ControllerAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, buffer.getNumSamples());


    juce::MidiBuffer filteredMidi;
    for (const auto meta : midiMessages)
    {
        const auto msg = meta.getMessage();
        if (msg.isAftertouch() || msg.isChannelPressure())
            continue;
            
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
                    else continue;
                    
                    const juce::uint8* nibbles = data + 12;
                    int nibbleCount = size - 14;
                    int byteCount = nibbleCount / 2;
                    
                    for (int i = 0; i < byteCount; ++i)
                    {
                        if (payloadOffset + i < 120)
                        {
                            juce::uint8 b = ((nibbles[i*2] & 0x0F) << 4) | (nibbles[i*2+1] & 0x0F);
                            incomingSysExValues[payloadOffset + i].store((float)b);
                            juce::Logger::writeToLog("SysEx_DUMP Byte " + juce::String(payloadOffset + i) + " = " + juce::String(b));
                        }
                    }
                    
                    ccBlockTimer.store(20); // Block CCs for 20 timer ticks (approx 600ms)

                }
            }
        }
            
        if (msg.isController())
        {
            int ccNum = msg.getControllerNumber();
            float val = (float)msg.getControllerValue();
            incomingCcValues[ccNum].store(val);
            
            bool handled = false;
            for (auto& cp : ccParams)
            {
                if (cp.ccNumber == ccNum)
                {
                    cp.lastValue = val;
                    handled = true;
                }
            }
            if (handled) continue;
        }
        filteredMidi.addEvent(msg, meta.samplePosition);
    }
    midiMessages.swapWith(filteredMidi);


    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)
        {
            float currentVal = *cp.param;
            if (std::abs(currentVal - cp.lastValue) > 0.1f)
            {
                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);
                midiOutputQueue.addEvent(message, 0);
                cp.lastValue = currentVal;
            }
        }
    }

    midiMessages.addEvents(midiOutputQueue, 0, buffer.getNumSamples(), 0);
    midiOutputQueue.clear();
}

bool SE02_ControllerAudioProcessor::hasEditor() const { return true; }

void SE02_ControllerAudioProcessor::timerCallback()
{
    // Process CCs
    for (auto& cp : ccParams)
    {
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
        if (hwVal >= 0.0f)
        {
            if (auto* param = apvts.getParameter(cp.id))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }
    
    auto sysexToCc = [](const juce::String& id, float syxVal) -> float {
        int maxDiscrete = -1;
        
        // 2-position switches (0, 1)
        if (id == "GLIDE_TYPE" || id == "SYNC" || id == "KYBD" || 
            id == "KEYTRACK_13" || id == "KEYTRACK_23" || id == "MTRIG" || 
            id == "INVERT" || id == "LFO_MW_FLT" || id == "LFO_MW_OSC" || 
            id == "LFO_SYNC") {
            maxDiscrete = 1;
        } 
        // 3-position switches (0, 1, 2)
        else if (id == "REL" || id == "GATE_LFO" || id == "LFO_MODE" || id == "XMOD_MW") {
            maxDiscrete = 2;
        } 
        // 6-position digital switches (0, 1, 2, 3, 4, 5)
        else if (id == "OSC1_RANGE" || id == "OSC2_RANGE" || id == "OSC3_RANGE" || 
                 id == "OSC1_WAVE" || id == "OSC2_WAVE" || id == "OSC3_WAVE" || 
                 id == "LFO_WAVE") {
            maxDiscrete = 5;
        }
        

        
        if (maxDiscrete == 5) {
            // 6 positions: mathematically robust centers that evaluate correctly under any common synth division logic
            float vals[6] = {0.0f, 26.0f, 51.0f, 77.0f, 102.0f, 127.0f};
            return vals[juce::jlimit(0, 5, (int)syxVal)];
        } else if (maxDiscrete == 2) {
            // 3 positions
            float vals[3] = {0.0f, 64.0f, 127.0f};
            return vals[juce::jlimit(0, 2, (int)syxVal)];
        } else if (maxDiscrete == 1) {
            // 2 positions
            return syxVal > 0.0f ? 127.0f : 0.0f;
        }
        
        // Continuous analog potentiometers (including Range knobs which are analog) use the full 0-255 scale
        return (syxVal / 255.0f) * 127.0f;
    };

    if (ccBlockTimer.load() > 0) ccBlockTimer.fetch_sub(1);

    bool wroteLog = false;
    std::ofstream logFile;
    
    // Process SysEx
    for (int i = 0; i < 120; ++i)
    {
        float hwVal = incomingSysExValues[i].exchange(-1.0f);
        if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())
        {
            if (!wroteLog) {
                logFile.open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/vst_log.txt", std::ios_base::app);
                logFile << "--- NEW SYSEX READ ---" << std::endl;
                wroteLog = true;
            }
            logFile << "Index " << i << " (" << syxParamMap[i] << ") rawSysEx=" << hwVal << std::endl;
            
            if (auto* param = apvts.getParameter(syxParamMap[i]))
            {
                float mappedVal = sysexToCc(syxParamMap[i], hwVal);
                logFile << "  -> mapped to CC value: " << mappedVal << std::endl;
                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                
                for (auto& cp : ccParams) {
                    if (cp.id == syxParamMap[i]) {
                        cp.lastValue = mappedVal;
                    }
                }
            }
        }
    }
    if (wroteLog) logFile.close();
}

void SE02_ControllerAudioProcessor::requestSysExPreset()
{
    // Roland RQ1 Request (Data Request 1)
    // F0 41 {DeviceID} {ModelID} 11 {Address} {Size} {Checksum} F7
    // SE-02 Model ID is likely 00 00 00 3C or 00 00 00 48, Device ID is usually 10
    // Let's send a standard request to the temporary patch buffer.
    // Since we don't know the exact address yet, we'll try a common Roland structure 
    // and wait for the user to dump a patch so we can see the real address.
    
    // As a placeholder, we'll construct a dummy RQ1 just to trigger activity,
    // but the main goal right now is for the user to send a patch from the hardware!


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

    
    // F0 41 10 00 00 00 44 11 05 00 00 00 00 00 00 40 [CHK] F7
    sendRQ1(0x00, 0x00, 0x40); // 64 bytes
    sendRQ1(0x00, 0x40, 0x40); // 64 bytes
    sendRQ1(0x01, 0x00, 0x40); // 64 bytes
    sendRQ1(0x01, 0x40, 0x30); // 48 bytes

}


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
                ccBlockTimer.store(20);

                ccBlockTimer.store(20); // Block CCs for 20 timer ticks (approx 600ms)

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

juce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor() { return new SE02_ControllerAudioProcessorEditor (*this); }

void SE02_ControllerAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    auto state = apvts.copyState();
    std::unique_ptr<juce::XmlElement> xml (state.createXml());
    copyXmlToBinary (*xml, destData);
}

void SE02_ControllerAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    std::unique_ptr<juce::XmlElement> xmlState (getXmlFromBinary (data, sizeInBytes));
    if (xmlState.get() != nullptr)
        if (xmlState->hasTagName (apvts.state.getType()))
            apvts.replaceState (juce::ValueTree::fromXml (*xmlState));
}

juce::AudioProcessorValueTreeState::ParameterLayout SE02_ControllerAudioProcessor::createParameterLayout()
{
    juce::AudioProcessorValueTreeState::ParameterLayout layout;
    
    auto addCcParam = [&](const juce::String& id, const juce::String& name, float min, float max, float defaultVal) {
        layout.add(std::make_unique<juce::AudioParameterFloat>(
            juce::ParameterID(id, 1), name, juce::NormalisableRange<float>(min, max, 1.0f), defaultVal));
    };

"""

for p in params:
    proc_code += f'    addCcParam("{p[0]}", "{p[1]}", 0.0f, 127.0f, 0.0f);\n'

proc_code += """
    return layout;
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter() { return new SE02_ControllerAudioProcessor(); }
"""

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/Source/PluginProcessor.cpp", "w") as f:
    f.write(proc_code)

editor_code = """#include "PluginProcessor.h"
#include <fstream>
#include "PluginEditor.h"
#include "BinaryData.h"

class MainPanel : public juce::Component
{
public:
    MainPanel()
    {
        bgImage = juce::ImageCache::getFromMemory(BinaryData::bg_png, BinaryData::bg_pngSize);
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
    setSize (1024, 330);
    mainPanel = std::make_unique<MainPanel>();
    mainPanel->setBounds(0, 0, 1024, 330);
    addAndMakeVisible(mainPanel.get());

    setResizable(true, true);
    constrainer.setFixedAspectRatio(1024.0 / 330.0);
    constrainer.setSizeLimits(1024, 330, 2048, 660);
    setConstrainer(&constrainer);

    addAndMakeVisible(resizer);

    juce::LookAndFeel::setDefaultLookAndFeel(&customLookAndFeel);

    readPresetBtn.setButtonText("READ PRESET");
    readPresetBtn.setBounds(890, 302, 120, 24);
    readPresetBtn.onClick = [this]() {
        audioProcessor.requestSysExPreset();
    };
    mainPanel->addAndMakeVisible(readPresetBtn);

    showValuesBtn.setButtonText("SHOW VALUES");
    showValuesBtn.setToggleState(false, juce::dontSendNotification);
    showValuesBtn.setBounds(480, 302, 120, 24);
    showValuesBtn.onClick = [this]() {
        bool show = showValuesBtn.getToggleState();
        customLookAndFeel.showValues = show;
        switchLookAndFeel.showValues = show;
        mainPanel->repaint();
    };
    mainPanel->addAndMakeVisible(showValuesBtn);

    midiInBox.setBounds(630, 302, 120, 24);
    midiInBox.setTextWhenNothingSelected("MIDI Input...");
    mainPanel->addAndMakeVisible(midiInBox);

    midiOutBox.setBounds(760, 302, 120, 24);
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
    
    addKnob("GLIDE", "GLIDE", 46, r1, kSize);
    addSwitch("GLIDE_TYPE", "TYPE", 46, r2, sWidth, sHeight);
    addKnob("WHL_MIX", "WHL MIX", 46, r3, kSize);

    // OSCILLATORS
    int ox1 = 116, ox2 = 186, ox3 = 256, ox4 = 324;
    addKnob("OSC1_RANGE", "RANGE", ox1, r1, kSize);
    addKnob("OSC1_TUNE", "TUNE", ox2, r1, kSize);
    addKnob("OSC1_WAVE", "WAVEFORM", ox3, r1, kSize);
    addSwitch("SYNC", "SYNC", ox4, r1, sWidth, sHeight);

    addKnob("OSC2_RANGE", "RANGE", ox1, r2, kSize);
    addKnob("OSC2_FINE", "FINE", ox2, r2, kSize);
    addKnob("OSC2_WAVE", "WAVEFORM", ox3, r2, kSize);
    addKnob("ENV1", "ENV1", ox4, r2, kSize);

    addKnob("OSC3_RANGE", "RANGE", ox1, r3, kSize);
    addKnob("OSC3_FINE", "FINE", ox2, r3, kSize);
    addKnob("OSC3_WAVE", "WAVEFORM", ox3, r3, kSize);
    addSwitch("KYBD", "KYBD", 311, r3, sWidth, sHeight);
    addSwitch("XMOD_MW", "XMOD", 341, r3, sWidth, sHeight);

    // XMOD
    int xx = 394;
    addKnob("XMOD_O2FLT", "O2-FILTER", xx, r1, kSize);
    addKnob("XMOD_O3O2", "O3-O2", xx, r2, kSize);
    addKnob("XMOD_O3PW", "O3-PW1,2", xx, r3, kSize);

    // MIXER
    int mx1 = 460, mx2 = 501;
    addKnob("MIX_OSC1", "OSC 1", mx1, r1, kSize);
    addKnob("MIX_OSC2", "OSC 2", mx1, r2, kSize);
    addKnob("MIX_OSC3", "OSC 3", mx1, r3, kSize);
    addKnob("MIX_FBACK", "FEEDBACK", mx2, cy1, kSize);
    addKnob("MIX_NOISE", "NOISE", mx2, cy2, kSize);

    // FILTER/ENVELOPES
    int fx1 = 560, fx2 = 628, fx3 = 696, fx4 = 764;
    addKnob("CUTOFF", "CUTOFF", fx1, r1, kSize);
    addKnob("EMPHASIS", "EMPHASIS", fx2, r1, kSize);
    addSwitch("KEYTRACK_13", "1/3", 681, r1, sWidth, sHeight);
    addSwitch("KEYTRACK_23", "2/3", 711, r1, sWidth, sHeight);
    addKnob("CONTOUR", "CONTOUR", fx4, r1, kSize);

    addKnob("FILT_ATTACK", "ATTACK", fx1, r2, kSize);
    addKnob("FILT_DECAY", "DECAY", fx2, r2, kSize);
    addKnob("FILT_SUSTAIN", "SUSTAIN", fx3, r2, kSize);
    addSwitch("MTRIG", "MTRIG", 749, r2, sWidth, sHeight);
    addSwitch("INVERT", "INVERT", 779, r2, sWidth, sHeight);

    addKnob("AMP_ATTACK", "ATTACK", fx1, r3, kSize);
    addKnob("AMP_DECAY", "DECAY", fx2, r3, kSize);
    addKnob("AMP_SUSTAIN", "SUSTAIN", fx3, r3, kSize);
    addSwitch("REL", "REL", 749, r3, sWidth, sHeight);
    addSwitch("GATE_LFO", "GATE", 779, r3, sWidth, sHeight);

    // LFO
    int lx1 = 834, lx2 = 905;
    addKnob("LFO_RATE", "RATE", lx1, r1, kSize);
    addKnob("LFO_WAVE", "WAVE", lx2, r1, kSize);
    addKnob("LFO_OSC", "OSC", lx1, r2, kSize);
    addKnob("LFO_FILT", "FILTER", lx2, r2, kSize);
    
    // Switches arranged horizontally: MWHL OSC, MWHL FLT, MODE, SYNC
    addSwitch("LFO_MW_OSC", "MWHL OSC", 816, r3, sWidth, sHeight);
    addSwitch("LFO_MW_FLT", "MWHL FLT", 852, r3, sWidth, sHeight);
    addSwitch("LFO_MODE", "MODE", 888, r3, sWidth, sHeight);
    addSwitch("LFO_SYNC", "SYNC", 924, r3, sWidth, sHeight);

    // DELAY
    int dx = 977;
    addKnob("DLY_TIME", "TIME", dx, r1, kSize);
    addKnob("DLY_REGEN", "REGEN", dx, r2, kSize);
    addKnob("DLY_AMOUNT", "AMOUNT", dx, r3, kSize);
}

SE02_ControllerAudioProcessorEditor::~SE02_ControllerAudioProcessorEditor()
{
    juce::LookAndFeel::setDefaultLookAndFeel(nullptr);
}

void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - width / 2;
    int y = cy - height / 2;
    comp->slider.setBounds(x, y, width, height + 16);
    comp->slider.setLookAndFeel(&switchLookAndFeel);
    mainPanel->addAndMakeVisible(comp->slider);

    // Labels are baked into background
    // comp->label.setText(name, juce::dontSendNotification);
    // comp->label.setJustificationType(juce::Justification::centred);
    // comp->label.setFont(10.0f);
    // comp->label.attachToComponent(&comp->slider, false);
    // mainPanel->addAndMakeVisible(comp->label);

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
    float scale = (float)getHeight() / 330.0f;
    mainPanel->setTransform(juce::AffineTransform::scale(scale));
    resizer.setBounds(getWidth() - 16, getHeight() - 16, 16, 16);
}
"""

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/Source/PluginEditor.cpp", "w") as f:
    f.write(editor_code)

print("Generated PluginProcessor.cpp and PluginEditor.cpp")
