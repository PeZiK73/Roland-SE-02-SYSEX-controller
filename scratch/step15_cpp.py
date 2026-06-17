import sys
import re
with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix isFetchingBank
content = content.replace('return fetchState != FetchState::Idle;', 'return isFetching;')

# Fix startFetchingBank
hook_start = '''void SE02_ControllerAudioProcessor::startFetchingBank(int bankIndex)
{
    if (isFetching) return;
    fetchBankIndex = juce::jlimit(0, 4, bankIndex);
    fetchPatchIndex = 0;
    isFetching = true;
    fetchPhase = 1; // Start phase 1
    fetchTimeoutCounter = 0;
}'''
content = re.sub(r'void SE02_ControllerAudioProcessor::startFetchingBank\(int bankIndex\)\s*\{.*?\}', hook_start, content, flags=re.DOTALL)

# Fix processFetchStateMachine
hook_process = '''void SE02_ControllerAudioProcessor::processFetchStateMachine()
{
    if (!isFetching) return;

    if (fetchPhase == 1) // Phase 1: Send Program Change
    {
        int msb = 85; 
        int lsb = fetchBankIndex; 
        if (fetchBankIndex == 4) lsb = 0; 
        int pc = fetchPatchIndex;
        
        if (hardwareMidiOut) {
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
        }
        
        fetchPhase = 2;
        fetchTimeoutCounter = 10; // Wait 300ms for hardware to change patch
    }
    else if (fetchPhase == 2) // Phase 2: Request SysEx
    {
        if (fetchTimeoutCounter > 0) {
            fetchTimeoutCounter--;
        } else {
            requestSysExPreset(); // Fires all 4 packets at once!
            fetchPhase = 3;
            fetchTimeoutCounter = 15; // Wait 450ms for reply and APVTS update
        }
    }
    else if (fetchPhase == 3) // Phase 3: Save to Disk
    {
        if (fetchTimeoutCounter > 0) {
            fetchTimeoutCounter--;
        } else {
            saveFetchedPresetToDisk();
            
            fetchPatchIndex++;
            if (fetchPatchIndex >= 128) {
                isFetching = false;
                fetchPhase = 0;
            } else {
                fetchPhase = 1; // Loop back to next patch
            }
        }
    }
}'''
content = re.sub(r'void SE02_ControllerAudioProcessor::processFetchStateMachine\(\).*?void SE02_ControllerAudioProcessor::saveFetchedPresetToDisk\(\)', hook_process + '\nvoid SE02_ControllerAudioProcessor::saveFetchedPresetToDisk()', content, flags=re.DOTALL)

# Remove the messy SysEx hook from handleIncomingMidiMessage
hook_midi = '''                ccBlockTimer.store(20); // Block CCs for 20 timer ticks (approx 600ms)
            }
        }
    }'''
content = re.sub(r'                ccBlockTimer\.store\(20\); // Block CCs.*?\}', hook_midi, content, flags=re.DOTALL)


with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("Injected simple state machine!")
