import re

cc_map = [
    ("GLIDE", 5), ("GLIDE_TYPE", 9), ("WHL_MIX", 13),
    ("OSC1_RANGE", 22), ("OSC1_WAVE", 24), # OSC1 Tune has no CC
    ("OSC2_RANGE", 19), ("OSC2_FINE", 27), ("OSC2_WAVE", 20),
    ("OSC3_RANGE", 25), ("OSC3_FINE", 28), ("OSC3_WAVE", 26),
    ("SYNC", 21), ("ENV1", 29), ("KYBD", 30), ("XMOD_MW", 31),
    ("XMOD_O2FLT", 16), ("XMOD_O3O2", 17), ("XMOD_O3PW", 18),
    ("MIX_OSC1", 48), ("MIX_OSC2", 49), ("MIX_OSC3", 50),
    ("MIX_FBACK", 51), ("MIX_NOISE", 41),
    ("CUTOFF", 74), ("EMPHASIS", 71), ("CONTOUR", 59),
    ("KEYTRACK_13", 57), ("KEYTRACK_23", 58), ("MTRIG", 60),
    ("INVERT", 61), ("REL", 62), ("GATE_LFO", 63),
    ("FILT_ATTACK", 47), ("FILT_DECAY", 52), ("FILT_SUSTAIN", 53),
    ("AMP_ATTACK", 73), ("AMP_DECAY", 75), ("AMP_SUSTAIN", 56),
    ("LFO_RATE", 102), ("LFO_WAVE", 104), ("LFO_OSC", 103),
    ("LFO_FILT", 105), ("LFO_MW_OSC", 106), ("LFO_MW_FLT", 107),
    ("LFO_MODE", 108), ("LFO_SYNC", 109),
    ("DLY_TIME", 82), ("DLY_REGEN", 83), ("DLY_AMOUNT", 91)
]

def fix_processor():
    with open('Source/PluginProcessor.cpp', 'r') as f:
        content = f.read()

    # Revert ccParams.push_back block
    new_cc = ""
    for name, cc in cc_map:
        new_cc += f'    ccParams.push_back({{"{name}", {cc}}});\n'
    
    content = re.sub(r'ccParams\.push_back\(\{"GLIDE".*?\n(?:    ccParams\.push_back\(.*?\);\n)*', new_cc, content, flags=re.MULTILINE|re.DOTALL)
    
    # Strip out direct MIDI out logic in processBlock
    processBlock_replacement = '''void SE02_ControllerAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, buffer.getNumSamples());

    // Process incoming MIDI from host
    for (const auto meta : midiMessages)
    {
        auto msg = meta.getMessage();
        if (msg.isController())
        {
            incomingCcValues[msg.getControllerNumber()].store((float)msg.getControllerValue());
        }
    }

    // Process parameter changes to CC directly into the host's MIDI buffer
    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)
        {
            float v = *cp.param;
            if (v != cp.lastValue)
            {
                cp.lastValue = v;
                if (cp.ccNumber != -1)
                {
                    int midiVal = (int)v;
                    auto msg = juce::MidiMessage::controllerEvent(1, cp.ccNumber, midiVal);
                    midiMessages.addEvent(msg, 0);
                }
            }
        }
    }
}
'''
    content = re.sub(r'void SE02_ControllerAudioProcessor::processBlock.*?\n}\n', processBlock_replacement, content, flags=re.MULTILINE|re.DOTALL, count=1)

    # Clean out timerCallback hardware MIDI logic
    timer_replacement = '''void SE02_ControllerAudioProcessor::timerCallback()
{
    // Process incoming CCs
    for (auto& cp : ccParams)
    {
        if (cp.ccNumber >= 0 && cp.ccNumber < 128) {
            float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
            if (hwVal >= 0.0f)
            {
                if (auto* param = apvts.getParameter(cp.id))
                    param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }
}
'''
    content = re.sub(r'void SE02_ControllerAudioProcessor::timerCallback\(\).*?\n}\n', timer_replacement, content, flags=re.MULTILINE|re.DOTALL, count=1)

    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)

fix_processor()
print("Processor cleaned!")
