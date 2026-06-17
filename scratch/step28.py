import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_destructor = """SE02_ControllerAudioProcessor::~SE02_ControllerAudioProcessor() { 
    if (hardwareMidiIn) hardwareMidiIn->stop();
    stopTimer(); 
}"""

new_destructor = """SE02_ControllerAudioProcessor::~SE02_ControllerAudioProcessor() { 
    stopTimer();
    if (hardwareMidiIn) {
        hardwareMidiIn->stop();
        hardwareMidiIn.reset();
    }
    if (hardwareMidiOut) {
        hardwareMidiOut.reset();
    }
}"""

content = content.replace(old_destructor, new_destructor)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
