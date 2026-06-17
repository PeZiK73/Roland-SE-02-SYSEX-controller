import re

# Read the file
with open("c:\\TEMP\\ANTIGRAVITIY_ROLANDS_SCRIPTS\\SE02_Controller\\sysex_mapping_results.txt", "r", encoding="utf-16le") as f:
    lines = f.readlines()

cc_to_idx = {}

for line in lines:
    # Example: CC #84 -> Chunk 1, Payload Offset 4 (Byte Index 15) [Values: 0 -> 7]
    match = re.search(r"CC #(\d+) -> Chunk (\d+), Payload Offset (\d+)", line)
    if match:
        cc = int(match.group(1))
        chunk = int(match.group(2))
        offset = int(match.group(3))
        
        # We only care about the FIRST payload offset for a CC (which is usually the MSB or LSB depending on Roland, but it is the base address for the parameter)
        if cc not in cc_to_idx:
            if chunk == 1: idx = offset
            elif chunk == 2: idx = 64 + offset
            elif chunk == 3: idx = 128 + offset
            elif chunk == 4: idx = 192 + offset
            cc_to_idx[cc] = idx

# Now we need to map CC to Parameter IDs
# From createParameterLayout in PluginProcessor.cpp:
cc_map = {
    5: "GLIDE",
    65: "GLIDE_TYPE",
    1: "WHL_MIX",
    12: "OSC1_RANGE",
    13: "OSC1_TUNE",
    14: "OSC1_WAVE",
    15: "OSC2_RANGE",
    16: "OSC2_FINE",
    17: "OSC2_WAVE",
    18: "OSC3_RANGE",
    19: "OSC3_FINE",
    20: "OSC3_WAVE",
    21: "SYNC",
    22: "ENV1",
    23: "KYBD",
    24: "XMOD_MW",
    25: "XMOD_O2FLT",
    26: "XMOD_O3O2",
    27: "XMOD_O3PW",
    28: "MIX_OSC1",
    29: "MIX_OSC2",
    30: "MIX_OSC3",
    31: "MIX_FBACK",
    35: "MIX_NOISE",
    74: "CUTOFF",
    71: "EMPHASIS",
    79: "CONTOUR",
    75: "KEYTRACK_13",
    76: "KEYTRACK_23",
    77: "MTRIG",
    78: "INVERT",
    80: "REL",
    81: "GATE_LFO",
    73: "FILT_ATTACK",
    102: "FILT_DECAY",
    103: "FILT_SUSTAIN",
    104: "AMP_ATTACK",
    105: "AMP_DECAY",
    106: "AMP_SUSTAIN",
    82: "LFO_RATE",
    83: "LFO_OSC",
    84: "LFO_WAVE",
    85: "LFO_FILT",
    86: "LFO_MW_OSC",
    87: "LFO_MW_FLT",
    88: "LFO_MODE",
    89: "LFO_SYNC",
    91: "DLY_TIME",
    92: "DLY_REGEN",
    93: "DLY_AMOUNT"
}

# The PWM LFO params are:
# Chunk 1, offset 13 (idx 13) -> PWM_LFO_RATE
# Chunk 1, offset 15 (idx 15) -> PWM_LFO_DEPTH
# We will manually add them.

print("    for (int i = 0; i < 256; ++i) syxParamMap[i] = \"\";")
for cc, param in cc_map.items():
    if cc in cc_to_idx:
        print(f"    syxParamMap[{cc_to_idx[cc]}] = \"{param}\";")
    else:
        print(f"    // WARNING: CC {cc} ({param}) was not found in the mapping results!")

print(f"    syxParamMap[13] = \"PWM_LFO_RATE\";")
print(f"    syxParamMap[15] = \"PWM_LFO_DEPTH\";")

