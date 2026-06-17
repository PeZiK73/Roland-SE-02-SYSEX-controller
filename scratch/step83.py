import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

content = content.replace(
    'void SE02_ControllerAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)\n{',
    'void SE02_ControllerAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)\n{\n    logdbg("START PREPARETOPLAY");'
)

content = content.replace(
    'void SE02_ControllerAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)\n{',
    'void SE02_ControllerAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)\n{\n    logdbg("START PROCESSBLOCK");'
)

content = content.replace(
    'void SE02_ControllerAudioProcessor::timerCallback()\n{',
    'void SE02_ControllerAudioProcessor::timerCallback()\n{\n    logdbg("START TIMERCALLBACK");'
)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("Injected more logs")
