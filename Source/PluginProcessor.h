#pragma once
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

    std::vector<CcParam> ccParams;
    std::atomic<float> incomingCcValues[128];
    juce::AudioProcessorValueTreeState apvts;
    
    // SysEx / Hardware MIDI features
    std::unique_ptr<juce::MidiInput> hardwareMidiIn;
    std::unique_ptr<juce::MidiOutput> hardwareMidiOut;
    void requestSysExPreset(int packetIndex = -1);
    void pushOutgoingMidiMessage(const juce::MidiMessage& msg);
    
    // FETCH BANK PATCHES API
    void startFetchingBank(int bankIndex, bool skipExisting); // 0=A, 1=B, 2=C, 3=D, 4=USER
    void cancelFetchingBank() { isFetching = false; fetchPhase = 0; }
    bool isFetchingBank() const { return isFetching; }
    int getFetchProgress() const { return fetchPatchIndex; }
    juce::String getFetchBankName() const;
    bool doesPatchExistOnDisk(int bankIndex, int patchIndex);

    void openMidiInput(const juce::String& identifier);
    void openMidiOutput(const juce::String& identifier);
    void saveGlobalSettings();
    void loadGlobalSettings();
    void handleIncomingMidiMessage(juce::MidiInput* source, const juce::MidiMessage& message) override;
    std::atomic<bool> sendRq1Request { false };
    juce::AbstractFifo outgoingMidiFifo{1024};
    juce::MidiMessage outgoingMidiBuffer[1024];
    std::map<int, juce::String> syxParamMap;
    std::atomic<float> incomingSysExValues[256];
    std::atomic<float> currentSysExBuffer[256];
    std::atomic<int> sysExDelayCounter { -1 };
    std::atomic<int> sysExRequestPacket { 0 };
    std::atomic<int> sysExTransmitPacket { -1 };
    std::atomic<int> ccBlockTimer { 0 };
    juce::MemoryBlock outgoingSysExBuffer;
    
    std::atomic<bool> isSavingCustomPreset { false };
    juce::String customPresetSavePath;
    juce::String customPresetSaveName;
    
    void transmitSysExPatch(const juce::MemoryBlock& patchData);
    void updateGuiFromSysEx(const juce::MemoryBlock& patchData);
    float sysexToCc(const juce::String& id, float syxVal);
    
    juce::String getBankName(int index);
    void sendProgramChange();
    juce::String getPatchNameFromSysEx();
    
    int currentBankIndex = 0; // 0=A, 1=B, 2=C, 3=USER, 4=D
    int currentPreset = 1; // 1 to 128

    // FETCH BANK STATE MACHINE
    bool isFetching = false;
    int fetchBankIndex = 0;
    int fetchPatchIndex = 0;
    int fetchPhase = 0; // 0=idle, 1=send pc, 2=send sysex req, 3=wait for rx
    int fetchTimeoutCounter = 0;
    int sysExRequestPhase = 0;
    bool skipExistingPatches = false;

    // SysEx Buffer
    juce::MemoryBlock incomingSysExData;
    void processFetchStateMachine();
    void saveFetchedPresetToDisk();
    
    // Update MIDI variables so apvts knows they changed
    juce::String lastMidiInName;
    juce::String lastMidiOutName;
    bool needsTotalRecall = false;

    juce::MidiBuffer midiOutputQueue;

private:
    juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (SE02_ControllerAudioProcessor)
};
