import re

def clean_cpp_methods():
    with open('Source/PluginProcessor.cpp', 'r') as f:
        content = f.read()

    # Remove the methods at the end of the file
    content = re.sub(r'void SE02_ControllerAudioProcessor::requestSysExPreset\(\).*', '', content, flags=re.MULTILINE|re.DOTALL)
    
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)

clean_cpp_methods()
print("Cleaned trailing methods!")
