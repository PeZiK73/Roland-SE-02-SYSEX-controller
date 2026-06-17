import os

cc_map = [
    ("GLIDE", "GLIDE", 5),
    ("GLIDE_TYPE", "TYPE", 9),
    ("WHL_MIX", "WHL MIX", 13),
    ("OSC1_RANGE", "RANGE", 22),
    ("OSC1_TUNE", "TUNE", -1),
    ("OSC1_WAVE", "WAVEFORM", 24),
    ("OSC2_RANGE", "RANGE", 19),
    ("OSC2_FINE", "FINE", 27),
    ("OSC2_WAVE", "WAVEFORM", 20),
    ("OSC3_RANGE", "RANGE", 25),
    ("OSC3_FINE", "FINE", 28),
    ("OSC3_WAVE", "WAVEFORM", 26),
    ("SYNC", "SYNC", 21),
    ("ENV1", "ENV1", 29),
    ("KYBD", "KYBD", 30),
    ("XMOD_MW", "TO MW", 31),
    ("XMOD_O2FLT", "O2-FILTER", 16),
    ("XMOD_O3O2", "O3-O2", 17),
    ("XMOD_O3PW", "O3-PW1,2", 18),
    ("MIX_OSC1", "OSC 1", 48),
    ("MIX_OSC2", "OSC 2", 49),
    ("MIX_OSC3", "OSC 3", 50),
    ("MIX_FBACK", "FEEDBACK", 51),
    ("MIX_NOISE", "NOISE", 41),
    ("CUTOFF", "CUTOFF", 74),
    ("EMPHASIS", "EMPHASIS", 71),
    ("CONTOUR", "CONTOUR", 59),
    ("KEYTRACK_13", "1/3", 57),
    ("KEYTRACK_23", "2/3", 58),
    ("MTRIG", "MTRIG", 60),
    ("INVERT", "INVERT", 61),
    ("REL", "REL", 62),
    ("GATE_LFO", "LFO/GATE", 63),
    ("FILT_ATTACK", "ATTACK", 47),
    ("FILT_DECAY", "DECAY", 52),
    ("FILT_SUSTAIN", "SUSTAIN", 53),
    ("AMP_ATTACK", "ATTACK", 73),
    ("AMP_DECAY", "DECAY", 75),
    ("AMP_SUSTAIN", "SUSTAIN", 56),
    ("LFO_RATE", "RATE", 102),
    ("LFO_WAVE", "WAVE", 104),
    ("LFO_OSC", "OSC", 103),
    ("LFO_FILT", "FILTER", 105),
    ("LFO_MW_OSC", "MWHL-OSC", 106),
    ("LFO_MW_FLT", "MWHL-FLT", 107),
    ("LFO_MODE", "MODE", 108),
    ("LFO_SYNC", "SYNC", 109),
    ("DLY_TIME", "TIME", 82),
    ("DLY_REGEN", "REGEN", 83),
    ("DLY_AMOUNT", "AMOUNT", 91)
]

h_code = '''#pragma once
#include <JuceHeader.h>

struct CcParam {
    juce::String id;
    int ccNumber;
    std::atomic<float>* param = nullptr;
    float lastValue = -1.0f;
};

class SE02_ControllerAudioProcessor  : public juce::AudioProcessor, public juce::Timer
{
public:
    SE02_ControllerAudioProcessor();
    ~SE02_ControllerAudioProcessor() override;

    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;
    void timerCallback() override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    const juce::String getName() const override;
    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    juce::AudioProcessorValueTreeState apvts;
    std::vector<CcParam> ccParams;
    std::atomic<float> incomingCcValues[128];

private:
    juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (SE02_ControllerAudioProcessor)
};
'''

cpp_code = '''#include "PluginProcessor.h"
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
'''

for p in cc_map:
    cpp_code += f'    ccParams.push_back({{"{p[0]}", {p[2]}}});\n'

cpp_code += '''
    for (auto& cp : ccParams)
    {
        cp.param = apvts.getRawParameterValue(cp.id);
        if (cp.param != nullptr)
            cp.lastValue = *cp.param;
    }
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
    for (auto& cp : ccParams) {
        if (cp.param != nullptr) {
            cp.lastValue = *cp.param;
        }
    }
}

void SE02_ControllerAudioProcessor::releaseResources() {}

#ifndef JucePlugin_PreferredChannelConfigurations
bool SE02_ControllerAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
    return true;
  #else
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;
   #if ! JucePlugin_IsSynth
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;
   #endif
    return true;
  #endif
}
#endif

void SE02_ControllerAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, buffer.getNumSamples());

    // Process incoming MIDI from host
    for (const auto meta : midiMessages)
    {
        auto msg = meta.getMessage();
        if (msg.isController())
        {
            incomingCcValues[msg.getControllerNumber()].store((float)msg.getControllerValue());
        }
    }

    // Process parameter changes to CC directly into the host's MIDI buffer
    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)
        {
            float v = *cp.param;
            if (v != cp.lastValue)
            {
                cp.lastValue = v;
                if (cp.ccNumber != -1)
                {
                    int midiVal = (int)v;
                    auto msg = juce::MidiMessage::controllerEvent(1, cp.ccNumber, midiVal);
                    midiMessages.addEvent(msg, 0);
                }
            }
        }
    }
}

bool SE02_ControllerAudioProcessor::hasEditor() const { return true; }
juce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor() { return new SE02_ControllerAudioProcessorEditor(*this); }

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

void SE02_ControllerAudioProcessor::timerCallback()
{
    // Process incoming CCs from the host routing
    for (auto& cp : ccParams)
    {
        if (cp.ccNumber >= 0 && cp.ccNumber < 128) {
            float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
            if (hwVal >= 0.0f)
            {
                if (auto* param = apvts.getParameter(cp.id))
                    param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }
}

juce::AudioProcessorValueTreeState::ParameterLayout SE02_ControllerAudioProcessor::createParameterLayout()
{
    juce::AudioProcessorValueTreeState::ParameterLayout layout;
    auto addCcParam = [&](const juce::String& id, const juce::String& name, float min, float max, float defaultVal) {
        layout.add(std::make_unique<juce::AudioParameterFloat>(
            juce::ParameterID(id, 1), name, juce::NormalisableRange<float>(min, max, 1.0f), defaultVal));
    };
'''

for p in cc_map:
    cpp_code += f'    addCcParam("{p[0]}", "{p[1]}", 0.0f, 127.0f, 64.0f if "{p[0]}" == "OSC2_FINE" or "{p[0]}" == "OSC3_FINE" else 0.0f);\n'

cpp_code += '''
    return layout;
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter() { return new SE02_ControllerAudioProcessor(); }
'''

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(h_code)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(cpp_code)

print("Headers and CPP fully restored to pure VST MIDI logic!")
