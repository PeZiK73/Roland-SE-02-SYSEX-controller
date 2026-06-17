import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    text = f.read()

init_block = """    ccParams.push_back({"GLIDE", 5});
    ccParams.push_back({"GLIDE_TYPE", 9});
    ccParams.push_back({"WHL_MIX", 13});
    ccParams.push_back({"OSC1_RANGE", 22});
    ccParams.push_back({"OSC1_TUNE", -1});
    ccParams.push_back({"OSC1_WAVE", 24});
    ccParams.push_back({"OSC2_RANGE", 19});
    ccParams.push_back({"OSC2_FINE", 27});
    ccParams.push_back({"OSC2_WAVE", 20});
    ccParams.push_back({"OSC3_RANGE", 25});
    ccParams.push_back({"OSC3_FINE", 28});
    ccParams.push_back({"OSC3_WAVE", 26});
    ccParams.push_back({"SYNC", 21});
    ccParams.push_back({"ENV1", 29});
    ccParams.push_back({"KYBD", 30});
    ccParams.push_back({"XMOD_MW", 31});
    ccParams.push_back({"XMOD_O2FLT", 16});
    ccParams.push_back({"XMOD_O3O2", 17});
    ccParams.push_back({"XMOD_O3PW", 18});
    ccParams.push_back({"MIX_OSC1", 48});
    ccParams.push_back({"MIX_OSC2", 49});
    ccParams.push_back({"MIX_OSC3", 50});
    ccParams.push_back({"MIX_FBACK", 51});
    ccParams.push_back({"MIX_NOISE", 41});
    ccParams.push_back({"CUTOFF", 74});
    ccParams.push_back({"EMPHASIS", 71});
    ccParams.push_back({"CONTOUR", 59});
    ccParams.push_back({"KEYTRACK_13", 57});
    ccParams.push_back({"KEYTRACK_23", 58});
    ccParams.push_back({"MTRIG", 60});
    ccParams.push_back({"INVERT", 61});
    ccParams.push_back({"REL", 62});
    ccParams.push_back({"GATE_LFO", 63});
    ccParams.push_back({"FILT_ATTACK", 47});
    ccParams.push_back({"FILT_DECAY", 52});
    ccParams.push_back({"FILT_SUSTAIN", 53});
    ccParams.push_back({"AMP_ATTACK", 73});
    ccParams.push_back({"AMP_DECAY", 75});
    ccParams.push_back({"AMP_SUSTAIN", 56});
    ccParams.push_back({"LFO_RATE", 102});
    ccParams.push_back({"LFO_WAVE", 104});
    ccParams.push_back({"LFO_OSC", 103});
    ccParams.push_back({"LFO_FILT", 105});
    ccParams.push_back({"LFO_MW_OSC", 106});
    ccParams.push_back({"LFO_MW_FLT", 107});
    ccParams.push_back({"LFO_MODE", 108});
    ccParams.push_back({"LFO_SYNC", 109});
    ccParams.push_back({"DLY_TIME", 82});
    ccParams.push_back({"DLY_REGEN", 83});
    ccParams.push_back({"DLY_AMOUNT", 91});"""

text = text.replace('    startTimerHz(30);', '    startTimerHz(30);\n\n' + init_block)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(text)
