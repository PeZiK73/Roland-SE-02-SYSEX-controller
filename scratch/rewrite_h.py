h_content = '''#pragma once
#include <JuceHeader.h>

struct CcParam {
    juce::String id;
    int ccNumber;
    std::atomic<float>* param = nullptr;
    float lastValue = -1.0f;
};

class SE02_ControllerAudioProcessor  : public juce::AudioProcessor, public juce::Timer, private juce::MidiInputCallback
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
    
    // SysEx / Hardware MIDI features
    juce::MidiInput* hardwareMidiIn = nullptr;
    juce::MidiOutput* hardwareMidiOut = nullptr;
    void requestSysExPreset();
    void openMidiInput(const juce::String& identifier);
    void openMidiOutput(const juce::String& identifier);
    void handleIncomingMidiMessage(juce::MidiInput* source, const juce::MidiMessage& message) override;
    std::atomic<bool> sendRq1Request { false };
    juce::AbstractFifo outgoingMidiFifo{1024};
    juce::MidiMessage outgoingMidiBuffer[1024];
    std::map<int, juce::String> syxParamMap;
    std::atomic<float> incomingSysExValues[120];

private:
    juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (SE02_ControllerAudioProcessor)
};
'''

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(h_content)
