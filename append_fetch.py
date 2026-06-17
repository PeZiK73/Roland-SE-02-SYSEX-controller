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
'''
with open('Source/PluginProcessor.cpp', 'a') as f:
    f.write(code_to_add)
