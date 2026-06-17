import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix 1: Stop timerCallback from wiping out unmapped SysEx bytes (like the patch name)
old_timer = """      // Process SysEx
      for (int i = 0; i < 120; ++i)
      {
          float hwVal = incomingSysExValues[i].exchange(-1.0f);
          if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())"""

new_timer = """      // Process SysEx
      for (int i = 0; i < 120; ++i)
      {
          if (syxParamMap[i].isEmpty()) continue;
          float hwVal = incomingSysExValues[i].exchange(-1.0f);
          if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())"""

if old_timer in content:
    content = content.replace(old_timer, new_timer)
    print("Fixed timerCallback SysEx wiping")
else:
    print("Could not find old_timer")

# Fix 2: Change the filename format to 001_[patch_name]
old_filename = """      juce::String patchName = "PATCH_" + juce::String(fetchPatchIndex + 1);
      if (fetchBankIndex == 0) patchName = PresetNames::getBankA()[fetchPatchIndex];
      else if (fetchBankIndex == 1) patchName = PresetNames::getBankB()[fetchPatchIndex];
      else if (fetchBankIndex == 2) patchName = PresetNames::getBankC()[fetchPatchIndex];
      else if (fetchBankIndex == 3) patchName = PresetNames::getBankD()[fetchPatchIndex];
      else if (fetchBankIndex == 4) patchName = PresetNames::getUserBank()[fetchPatchIndex];"""

new_filename = """      juce::String indexStr = juce::String(fetchPatchIndex + 1).paddedLeft('0', 3);
      juce::String patchName = indexStr + "_" + getPatchNameFromSysEx();"""

if old_filename in content:
    content = content.replace(old_filename, new_filename)
    print("Fixed file naming logic")
else:
    print("Could not find old_filename")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

