import sys

with open('Source/PluginProcessor.h', 'r') as f:
    h_content = f.read()

h_content = h_content.replace('enum class FetchState { Idle, RequestingPatch, WaitingForSysEx, SavingPatch };',
    'enum class FetchState { Idle, RequestingPatch, WaitSysEx_00, WaitSysEx_40, WaitSysEx_80, WaitSysEx_C0, SavingPatch };')

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(h_content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    cpp_content = f.read()

hook_cpp = '''
void SE02_ControllerAudioProcessor::processFetchStateMachine()
{
    if (fetchState == FetchState::Idle) return;

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

    if (fetchState == FetchState::RequestingPatch)
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
        
        fetchTimeoutCounter = 10; // Wait 300ms for patch to load
        fetchState = FetchState::WaitSysEx_00;
    }
    else if (fetchState == FetchState::WaitSysEx_00 || fetchState == FetchState::WaitSysEx_40 || fetchState == FetchState::WaitSysEx_80 || fetchState == FetchState::WaitSysEx_C0)
    {
        if (fetchTimeoutCounter > 0)
        {
            fetchTimeoutCounter--;
            if (fetchTimeoutCounter == 0)
            {
                if (fetchRetryCounter < 3)
                {
                    fetchRetryCounter++;
                    if (fetchState == FetchState::WaitSysEx_00) sendRQ1(0x00, 0x00, 0x40);
                    else if (fetchState == FetchState::WaitSysEx_40) sendRQ1(0x00, 0x40, 0x40);
                    else if (fetchState == FetchState::WaitSysEx_80) sendRQ1(0x01, 0x00, 0x40);
                    else if (fetchState == FetchState::WaitSysEx_C0) sendRQ1(0x01, 0x40, 0x30);
                    
                    fetchTimeoutCounter = 30; // Wait 1 second for reply
                }
                else
                {
                    // Given up on this patch! Skip to next
                    fetchPatchIndex++;
                    fetchRetryCounter = 0;
                    if (fetchPatchIndex >= 128) fetchState = FetchState::Idle;
                    else fetchState = FetchState::RequestingPatch;
                }
            }
        }
    }
    else if (fetchState == FetchState::SavingPatch)
    {
        if (fetchTimeoutCounter > 0)
        {
            fetchTimeoutCounter--;
        }
        else
        {
            saveFetchedPresetToDisk();
            fetchPatchIndex++;
            fetchRetryCounter = 0;
            if (fetchPatchIndex >= 128) fetchState = FetchState::Idle;
            else fetchState = FetchState::RequestingPatch;
        }
    }
}
'''

import re
cpp_content = re.sub(r'void SE02_ControllerAudioProcessor::processFetchStateMachine\(\).*?void SE02_ControllerAudioProcessor::saveFetchedPresetToDisk\(\)', 
    hook_cpp + '\nvoid SE02_ControllerAudioProcessor::saveFetchedPresetToDisk()', 
    cpp_content, flags=re.DOTALL)


hook_midi = '''                ccBlockTimer.store(20); // Block CCs for 20 timer ticks (approx 600ms)

                if (baseAddress == 0x00 && fetchState == FetchState::WaitSysEx_00) {
                    fetchState = FetchState::WaitSysEx_40;
                    fetchTimeoutCounter = 1; fetchRetryCounter = 0;
                }
                else if (baseAddress == 0x40 && fetchState == FetchState::WaitSysEx_40) {
                    fetchState = FetchState::WaitSysEx_80;
                    fetchTimeoutCounter = 1; fetchRetryCounter = 0;
                }
                else if (baseAddress == 0x80 && fetchState == FetchState::WaitSysEx_80) {
                    fetchState = FetchState::WaitSysEx_C0;
                    fetchTimeoutCounter = 1; fetchRetryCounter = 0;
                }
                else if (baseAddress == 0xC0 && fetchState == FetchState::WaitSysEx_C0) {
                    fetchState = FetchState::SavingPatch;
                    fetchTimeoutCounter = 5; fetchRetryCounter = 0;
                }
            }
'''

cpp_content = re.sub(r'                ccBlockTimer.store\(20\);\n\n                if \(baseAddress == 0xC0\).*?\}', hook_midi, cpp_content, flags=re.DOTALL)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(cpp_content)

print("Injected processFetchStateMachine overhaul!")
