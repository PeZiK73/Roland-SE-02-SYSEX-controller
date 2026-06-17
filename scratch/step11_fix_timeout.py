import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix the infinite loop and add a retry counter
with open('Source/PluginProcessor.h', 'r') as hf:
    h_content = hf.read()
if 'int fetchRetryCounter = 0;' not in h_content:
    h_content = h_content.replace('int fetchTimeoutCounter = 0;', 'int fetchTimeoutCounter = 0;\n    int fetchRetryCounter = 0;')
    with open('Source/PluginProcessor.h', 'w') as hf:
        hf.write(h_content)

hook_old = '''    else if (fetchState == FetchState::WaitingForSysEx)
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
    }'''

hook_new = '''    else if (fetchState == FetchState::WaitingForSysEx)
    {
        if (fetchTimeoutCounter > 0)
        {
            fetchTimeoutCounter--;
            if (fetchTimeoutCounter == 0)
            {
                if (fetchRetryCounter < 3)
                {
                    fetchRetryCounter++;
                    requestSysExPreset();
                    fetchTimeoutCounter = 60; // Wait 2 seconds for reply
                }
                else
                {
                    // Given up on this patch!
                    fetchPatchIndex++;
                    if (fetchPatchIndex >= 128) fetchState = FetchState::Idle;
                    else fetchState = FetchState::RequestingPatch;
                }
            }
        }
    }'''

content = content.replace(hook_old, hook_new)
content = content.replace('fetchState = FetchState::RequestingPatch;\n    fetchTimeoutCounter = 0;', 'fetchState = FetchState::RequestingPatch;\n    fetchTimeoutCounter = 0;\n    fetchRetryCounter = 0;')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
