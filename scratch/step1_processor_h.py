import re

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

new_public_methods = '''    void requestSysExPreset();
    
    // FETCH BANK PATCHES API
    void startFetchingBank(int bankIndex); // 0=A, 1=B, 2=C, 3=D, 4=USER
    bool isFetchingBank() const { return fetchState != FetchState::Idle; }
    int getFetchProgress() const { return fetchPatchIndex; }
    juce::String getFetchBankName() const;
'''

content = content.replace("    void requestSysExPreset();", new_public_methods)

new_private_vars = '''    int currentPreset = 1; // 1 to 128

    // FETCH BANK STATE MACHINE
    enum class FetchState { Idle, RequestingPatch, WaitingForSysEx };
    FetchState fetchState = FetchState::Idle;
    int fetchBankIndex = 0;
    int fetchPatchIndex = 0;
    int fetchTimeoutCounter = 0;
    void processFetchStateMachine();
    void saveFetchedPresetToDisk();
'''

content = content.replace("    int currentPreset = 1; // 1 to 128", new_private_vars)

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)
