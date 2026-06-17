import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Update FetchState enum in PluginProcessor.h
with open('Source/PluginProcessor.h', 'r') as hf:
    h_content = hf.read()
if "FetchState { Idle, RequestingPatch, WaitingForSysEx, SavingPatch };" not in h_content:
    h_content = h_content.replace("FetchState { Idle, RequestingPatch, WaitingForSysEx };", "FetchState { Idle, RequestingPatch, WaitingForSysEx, SavingPatch };")
    with open('Source/PluginProcessor.h', 'w') as hf:
        hf.write(h_content)

# 2. Update handleIncomingMidiMessage
hook = '''                  if (baseAddress == 0xC0) 
                  {
                      if (fetchState == FetchState::WaitingForSysEx)
                      {
                          fetchState = FetchState::SavingPatch;
                          fetchTimeoutCounter = 5; // Wait a bit for processBlock to consume sysex
                      }
                  }
              }
'''
if "fetchState = FetchState::SavingPatch" not in content:
    content = content.replace("              }\n          }\n      }\n  }", hook + "          }\n      }\n  }")

# 3. Update processFetchStateMachine
sm_old = '''    else if (fetchState == FetchState::WaitingForSysEx)
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
    }'''

sm_new = '''    else if (fetchState == FetchState::WaitingForSysEx)
    {
        if (fetchTimeoutCounter > 0)
        {
            fetchTimeoutCounter--;
            if (fetchTimeoutCounter == 0)
            {
                requestSysExPreset();
                fetchTimeoutCounter = 100; // Wait 3 seconds for reply
            }
        }
        else
        {
            // Timeout! Just move to next patch
            fetchPatchIndex++;
            if (fetchPatchIndex >= 128) fetchState = FetchState::Idle;
            else fetchState = FetchState::RequestingPatch;
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
            if (fetchPatchIndex >= 128) fetchState = FetchState::Idle;
            else fetchState = FetchState::RequestingPatch;
        }
    }'''

if "SavingPatch" not in content:
    content = content.replace(sm_old, sm_new)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

