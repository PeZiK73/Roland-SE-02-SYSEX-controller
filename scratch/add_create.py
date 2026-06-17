import os

with open('Source/PluginProcessor.cpp', 'a') as f:
    f.write('''
//==============================================================================
// This creates new instances of the plugin..
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new SE02_ControllerAudioProcessor();
}
''')
