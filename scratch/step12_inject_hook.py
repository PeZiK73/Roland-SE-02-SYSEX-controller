import sys
with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

hook = '''                ccBlockTimer.store(20);

                if (baseAddress == 0xC0) 
                {
                    if (fetchState == FetchState::WaitingForSysEx)
                    {
                        fetchState = FetchState::SavingPatch;
                        fetchTimeoutCounter = 5; // Wait a bit for processBlock to consume sysex
                    }
                }
            }'''

content = content.replace('                ccBlockTimer.store(20);\n\n                ccBlockTimer.store(20); // Block CCs for 20 timer ticks (approx 600ms)\n\n            }', hook)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
    print("Injected hook!")
