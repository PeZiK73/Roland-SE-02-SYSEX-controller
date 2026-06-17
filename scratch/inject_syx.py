import os

syx_map = {
  "GLIDE": 20, "GLIDE_TYPE": 21, "WHL_MIX": 22,
  "OSC1_RANGE": 29, "OSC1_TUNE": 32, "OSC1_WAVE": 37,
  "OSC2_RANGE": 30, "OSC2_FINE": 33, "OSC2_WAVE": 38,
  "OSC3_RANGE": 31, "OSC3_WAVE": 39,
  "SYNC": 40, "ENV1": 41, "KYBD": 42, "XMOD_MW": 43,
  "XMOD_O2FLT": 46, "XMOD_O3O2": 47, "XMOD_O3PW": 48,
  "MIX_OSC1": 51, "MIX_OSC2": 52, "MIX_OSC3": 53, "MIX_FBACK": 50, "MIX_NOISE": 49,
  "CUTOFF": 55, "EMPHASIS": 58, "CONTOUR": 65, "KEYTRACK_13": 61, "KEYTRACK_23": 62,
  "MTRIG": 66, "INVERT": 67, "REL": 68, "GATE_LFO": 69,
  "FILT_ATTACK": 56, "FILT_DECAY": 59, "FILT_SUSTAIN": 63,
  "AMP_ATTACK": 57, "AMP_DECAY": 60, "AMP_SUSTAIN": 64,
  "LFO_RATE": 75, "LFO_WAVE": 77, "LFO_OSC": 76, "LFO_FILT": 80,
  "LFO_MW_OSC": 79, "LFO_MW_FLT": 78, "LFO_MODE": 81, "LFO_SYNC": 82,
  "DLY_TIME": 100, "DLY_REGEN": 101, "DLY_AMOUNT": 102
}

map_cpp = "    // Mapping SysEx payload index to VST parameter ID\\n"
for param_id, idx in syx_map.items():
    map_cpp += f'    syxParamMap[{idx}] = "{param_id}";\\n'

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/Source/PluginProcessor.h", "r") as f:
    h_code = f.read()

if "juce::String syxParamMap" not in h_code:
    h_code = h_code.replace("std::atomic<float> incomingCcValues[128];", 
                            "std::atomic<float> incomingCcValues[128];\\n    juce::String syxParamMap[120];\\n    std::atomic<float> incomingSysExValues[120];\\n")
    with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/Source/PluginProcessor.h", "w") as f:
        f.write(h_code)

# We will read generate.py, replace the PluginProcessor.cpp generation block
# and re-run generate.py.
