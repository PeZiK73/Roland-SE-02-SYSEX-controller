import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

bad_chunk = '''                else if (baseAddress == 0x40 && fetchState == FetchState::WaitSysEx_40) {
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

                }
            }
        }
    }'''

import re
content = content.replace(bad_chunk, '')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
