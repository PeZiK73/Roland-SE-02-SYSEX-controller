import re

with open('Source/PluginEditor.cpp', 'r') as f:
    editor_content = f.read()

match = re.search(r'void SE02_ControllerAudioProcessorEditor::savePresetToFile\(const juce::File& file\)\s*\{(.*?)\n\}', editor_content, re.DOTALL)
if match:
    body = match.group(1)
    
    with open('Source/PluginProcessor.cpp', 'r') as f:
        processor_content = f.read()
        
    # Find saveFetchedPresetToDisk
    proc_match = re.search(r'void SE02_ControllerAudioProcessor::saveFetchedPresetToDisk\(\)\s*\{(.*?)\n\}', processor_content, re.DOTALL)
    if proc_match:
        proc_body = proc_match.group(1)
        
        # Replace the inner logic
        new_proc_body = '''
    juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
    juce::File presetsDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES");
    juce::File bankDir = presetsDir.getChildFile(getFetchBankName());
    bankDir.createDirectory();
    
    juce::String patchName = "PATCH_" + juce::String(fetchPatchIndex + 1);
    if (fetchBankIndex == 0) patchName = PresetNames::getBankA()[fetchPatchIndex];
    else if (fetchBankIndex == 1) patchName = PresetNames::getBankB()[fetchPatchIndex];
    else if (fetchBankIndex == 2) patchName = PresetNames::getBankC()[fetchPatchIndex];
    else if (fetchBankIndex == 3) patchName = PresetNames::getBankD()[fetchPatchIndex];
    else if (fetchBankIndex == 4) patchName = PresetNames::getUserBank()[fetchPatchIndex];
    
    patchName = patchName.replaceCharacter('/', '_').replaceCharacter('\\\\', '_').replaceCharacter(':', '_').replaceCharacter('?', '_').replaceCharacter('"', '_').replaceCharacter('<', '_').replaceCharacter('>', '_').replaceCharacter('|', '_');
    
    juce::File file = bankDir.getChildFile(patchName + ".prm");
''' + body.replace('audioProcessor.apvts', 'apvts')

        processor_content = processor_content.replace(proc_match.group(0), "void SE02_ControllerAudioProcessor::saveFetchedPresetToDisk()\n{" + new_proc_body + "\n}")
        
        with open('Source/PluginProcessor.cpp', 'w') as f:
            f.write(processor_content)
        print("Successfully merged PRM save logic into PluginProcessor")
