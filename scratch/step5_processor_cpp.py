import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Add a check to handle incoming SysEx when fetching
hook = '''                  updateApvtsFromSysEx(payloadOffset, payloadSize);
                  
                  if (fetchState == FetchState::WaitingForSysEx)
                  {
                      // We received a part of the SysEx dump.
                      // Wait! The dump comes in 4 packets (00 00, 00 40, 01 00, 01 40).
                      // We should only save it when the LAST packet (01 40) arrives and is processed.
                      if (baseAddress == 0xC0) 
                      {
                          saveFetchedPresetToDisk();
                          fetchPatchIndex++;
                          if (fetchPatchIndex >= 128)
                          {
                              fetchState = FetchState::Idle;
                          }
                          else
                          {
                              fetchState = FetchState::RequestingPatch;
                          }
                      }
                  }
'''
if "if (fetchState == FetchState::WaitingForSysEx)" not in content:
    content = content.replace("                  updateApvtsFromSysEx(payloadOffset, payloadSize);", hook)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Updated handleIncomingMidiMessage")
