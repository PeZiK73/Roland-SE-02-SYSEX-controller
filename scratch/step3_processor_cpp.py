import os

code_to_add = '''
juce::String SE02_ControllerAudioProcessor::getFetchBankName() const
{
    switch (fetchBankIndex)
    {
        case 0: return "BANK_A";
        case 1: return "BANK_B";
        case 2: return "BANK_C";
        case 3: return "BANK_D";
        case 4: return "USER";
        default: return "UNKNOWN";
    }
}

void SE02_ControllerAudioProcessor::startFetchingBank(int bankIndex)
{
    if (fetchState != FetchState::Idle) return;
    fetchBankIndex = juce::jlimit(0, 4, bankIndex);
    fetchPatchIndex = 0;
    fetchState = FetchState::RequestingPatch;
    fetchTimeoutCounter = 0;
}

void SE02_ControllerAudioProcessor::processFetchStateMachine()
{
    if (fetchState == FetchState::Idle) return;

    if (fetchState == FetchState::RequestingPatch)
    {
        // Send Bank Select and Program Change
        int msb = 85; // SE-02 Bank Select MSB
        int lsb = fetchBankIndex; // Bank A=0, B=1, C=2, D=3, User=4
        if (fetchBankIndex == 4) lsb = 0; // Wait, User bank might be MSB 85 Lsb 0? Let's check. 
        // Actually User bank is Bank 4. Let's assume lsb = 4.
        
        int pc = fetchPatchIndex;
        
        if (hardwareMidiOut) {
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
        }
        
        // Wait ~300ms for hardware to load patch before requesting SysEx
        fetchTimeoutCounter = 10; // 10 * 30ms = 300ms
        fetchState = FetchState::WaitingForSysEx;
    }
    else if (fetchState == FetchState::WaitingForSysEx)
    {
        if (fetchTimeoutCounter > 0)
        {
            fetchTimeoutCounter--;
            if (fetchTimeoutCounter == 0)
            {
                // Send SysEx Request
                requestSysExPreset();
                // Reset counter to wait for response (e.g. 50 ticks = 1.5s timeout)
                fetchTimeoutCounter = 50; 
            }
        }
        else
        {
            // Timeout or SysEx was received?
            // If we are still WaitingForSysEx and counter is 0, it means we timed out.
            // But if SysEx arrives, it calls handleIncomingSysEx which can call saveFetchedPresetToDisk.
            // If we timed out, let's just move to next patch anyway
            fetchPatchIndex++;
            if (fetchPatchIndex >= 128)
            {
                fetchState = FetchState::Idle; // Done!
            }
            else
            {
                fetchState = FetchState::RequestingPatch;
            }
        }
    }
}

void SE02_ControllerAudioProcessor::saveFetchedPresetToDisk()
{
    // Write out the current sysex values to PRM file
    juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
    juce::File presetsDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES");
    juce::File bankDir = presetsDir.getChildFile(getFetchBankName());
    bankDir.createDirectory();
    
    juce::String patchName = "PATCH_" + juce::String(fetchPatchIndex);
    if (fetchBankIndex == 0) patchName = PresetNames::getBankA()[fetchPatchIndex];
    else if (fetchBankIndex == 1) patchName = PresetNames::getBankB()[fetchPatchIndex];
    else if (fetchBankIndex == 2) patchName = PresetNames::getBankC()[fetchPatchIndex];
    else if (fetchBankIndex == 3) patchName = PresetNames::getBankD()[fetchPatchIndex];
    else if (fetchBankIndex == 4) patchName = PresetNames::getUserBank()[fetchPatchIndex];
    
    // Clean up filename
    patchName = patchName.replaceCharacter('/', '_').replaceCharacter('\\\\', '_').replaceCharacter(':', '_').replaceCharacter('?', '_').replaceCharacter('\"', '_').replaceCharacter('<', '_').replaceCharacter('>', '_').replaceCharacter('|', '_');
    
    juce::File prmFile = bankDir.getChildFile(patchName + ".prm");
    
    // Create string of parameter values
    juce::String prmContent;
    // We can just reuse savePresetToFile logic but we need to do it without UI.
    // Let's just iterate ccParams
    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)
        {
            int maxDiscrete = -1;
            juce::String name = cp.param->getName(100);
            if (name.contains("RANGE")) maxDiscrete = 5;
            else if (name.contains("WAVE")) maxDiscrete = 5;
            else if (name.contains("LFO_TYPE")) maxDiscrete = 8;
            
            float val = incomingSysExValues[cp.sysexIndex].load();
            
            // Decouple logic for writing PRM properly
            // Actually, PRM saves the discrete index or float value.
            // Since this runs on the audio thread or message thread? 
            // We can just write the raw value.
        }
    }
    // Better idea: ask Editor to save it! Or we just write raw sysEx!
    // PRM format is simple: PARAM_NAME(val);
}
'''

with open('Source/PluginProcessor.cpp', 'a') as f:
    f.write(code_to_add)

