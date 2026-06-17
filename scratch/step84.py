import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

content = content.replace(
    'SE02_ControllerAudioProcessor::~SE02_ControllerAudioProcessor()\n{',
    'SE02_ControllerAudioProcessor::~SE02_ControllerAudioProcessor()\n{\n    logdbg("START DESTRUCTOR");'
)

content = content.replace(
    'void SE02_ControllerAudioProcessor::releaseResources()',
    'void SE02_ControllerAudioProcessor::releaseResources()\n{\n    logdbg("RELEASE RESOURCES");'
)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
