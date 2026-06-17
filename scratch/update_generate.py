import os

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/scratch/generate.py", "r") as f:
    gen_code = f.read()

syx_map_code = """
    for (int i = 0; i < 120; ++i) {
        incomingSysExValues[i].store(-1.0f);
        syxParamMap[i] = "";
    }
    
    syxParamMap[20] = "GLIDE";
    syxParamMap[21] = "GLIDE_TYPE";
    syxParamMap[22] = "WHL_MIX";
    syxParamMap[29] = "OSC1_RANGE";
    syxParamMap[32] = "OSC1_TUNE";
    syxParamMap[37] = "OSC1_WAVE";
    syxParamMap[30] = "OSC2_RANGE";
    syxParamMap[33] = "OSC2_FINE";
    syxParamMap[38] = "OSC2_WAVE";
    syxParamMap[31] = "OSC3_RANGE";
    syxParamMap[39] = "OSC3_WAVE";
    syxParamMap[40] = "SYNC";
    syxParamMap[41] = "ENV1";
    syxParamMap[42] = "KYBD";
    syxParamMap[43] = "XMOD_MW";
    syxParamMap[46] = "XMOD_O2FLT";
    syxParamMap[47] = "XMOD_O3O2";
    syxParamMap[48] = "XMOD_O3PW";
    syxParamMap[51] = "MIX_OSC1";
    syxParamMap[52] = "MIX_OSC2";
    syxParamMap[53] = "MIX_OSC3";
    syxParamMap[50] = "MIX_FBACK";
    syxParamMap[49] = "MIX_NOISE";
    syxParamMap[55] = "CUTOFF";
    syxParamMap[58] = "EMPHASIS";
    syxParamMap[65] = "CONTOUR";
    syxParamMap[61] = "KEYTRACK_13";
    syxParamMap[62] = "KEYTRACK_23";
    syxParamMap[66] = "MTRIG";
    syxParamMap[67] = "INVERT";
    syxParamMap[68] = "REL";
    syxParamMap[69] = "GATE_LFO";
    syxParamMap[56] = "FILT_ATTACK";
    syxParamMap[59] = "FILT_DECAY";
    syxParamMap[63] = "FILT_SUSTAIN";
    syxParamMap[57] = "AMP_ATTACK";
    syxParamMap[60] = "AMP_DECAY";
    syxParamMap[64] = "AMP_SUSTAIN";
    syxParamMap[75] = "LFO_RATE";
    syxParamMap[77] = "LFO_WAVE";
    syxParamMap[76] = "LFO_OSC";
    syxParamMap[80] = "LFO_FILT";
    syxParamMap[79] = "LFO_MW_OSC";
    syxParamMap[78] = "LFO_MW_FLT";
    syxParamMap[81] = "LFO_MODE";
    syxParamMap[82] = "LFO_SYNC";
    syxParamMap[100] = "DLY_TIME";
    syxParamMap[101] = "DLY_REGEN";
    syxParamMap[102] = "DLY_AMOUNT";
"""

replacement_processor = """
    juce::MidiBuffer filteredMidi;
    for (const auto meta : midiMessages)
    {
        const auto msg = meta.getMessage();
        if (msg.isAftertouch() || msg.isChannelPressure())
            continue;
            
        if (msg.isSysEx())
        {
            auto data = msg.getSysExData();
            int size = msg.getSysExDataSize();
            
            // F0 41 10 00 00 00 44 12
            if (size > 14 && data[1] == 0x41 && data[6] == 0x44 && data[7] == 0x12)
            {
                if (data[8] == 0x02 && data[9] == 0x00)
                {
                    int baseAddress = data[10] * 128 + data[11];
                    int payloadOffset = 0;
                    
                    if (baseAddress == 0x00) payloadOffset = 0;       // 00 00
                    else if (baseAddress == 0x40) payloadOffset = 32; // 00 40
                    else if (baseAddress == 0x80) payloadOffset = 64; // 01 00
                    else if (baseAddress == 0xC0) payloadOffset = 96; // 01 40
                    else continue;
                    
                    const juce::uint8* nibbles = data + 12;
                    int nibbleCount = size - 14;
                    int byteCount = nibbleCount / 2;
                    
                    for (int i = 0; i < byteCount; ++i)
                    {
                        if (payloadOffset + i < 120)
                        {
                            juce::uint8 b = ((nibbles[i*2] & 0x0F) << 4) | (nibbles[i*2+1] & 0x0F);
                            incomingSysExValues[payloadOffset + i].store((float)b);
                        }
                    }
                }
            }
        }
            
        if (msg.isController())
        {
            int ccNum = msg.getControllerNumber();
            float val = (float)msg.getControllerValue();
            incomingCcValues[ccNum].store(val);
            
            bool handled = false;
            for (auto& cp : ccParams)
            {
                if (cp.ccNumber == ccNum)
                {
                    cp.lastValue = val;
                    handled = true;
                }
            }
            if (handled) continue;
        }
        filteredMidi.addEvent(msg, meta.samplePosition);
    }
    midiMessages.swapWith(filteredMidi);
"""

# Replace the ccParams block in prepareToPlay to also initialize syx maps
gen_code = gen_code.replace("    startTimerHz(30);\n}", "    startTimerHz(30);\n" + syx_map_code + "}")

# Replace the processBlock parsing logic
import re
gen_code = re.sub(r'    juce::MidiBuffer filteredMidi;.*?    midiMessages\.swapWith\(filteredMidi\);', replacement_processor, gen_code, flags=re.DOTALL)

timer_replacement = """
    // Process CCs
    for (auto& cp : ccParams)
    {
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
        if (hwVal >= 0.0f)
        {
            if (auto* param = apvts.getParameter(cp.id))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }
    
    // Process SysEx
    for (int i = 0; i < 120; ++i)
    {
        float hwVal = incomingSysExValues[i].exchange(-1.0f);
        if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())
        {
            if (auto* param = apvts.getParameter(syxParamMap[i]))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }
"""

gen_code = re.sub(r'    for \(auto& cp : ccParams\)\n    \{\n        float hwVal = incomingCcValues\[cp\.ccNumber\].exchange\(-1\.0f\);\n        if \(hwVal >= 0\.0f\)\n        \{\n            if \(auto\* param = apvts\.getParameter\(cp\.id\)\)\n            \{\n                param->setValueNotifyingHost\(param->convertTo0to1\(hwVal\)\);\n            \}\n        \}\n    \}', timer_replacement, gen_code)

request_replacement = """
    auto sendRQ1 = [&](juce::uint8 a2, juce::uint8 a3, juce::uint8 s3) {
        juce::uint8 sysexData[] = {
            0xF0, 0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 
            0x02, 0x00, a2, a3, 
            0x00, 0x00, 0x00, s3, 
            0x00, 0xF7
        };
        int sum = 0x02 + 0x00 + a2 + a3 + 0x00 + 0x00 + 0x00 + s3;
        sysexData[16] = (128 - (sum % 128)) % 128;
        juce::MidiMessage rq1(sysexData, sizeof(sysexData));
        midiOutputQueue.addEvent(rq1, 0);
    };
    
    // F0 41 10 00 00 00 44 11 02 00 00 00 00 00 00 40 [CHK] F7
    sendRQ1(0x00, 0x00, 0x40); // 64 bytes
    sendRQ1(0x00, 0x40, 0x40); // 64 bytes
    sendRQ1(0x01, 0x00, 0x40); // 64 bytes
    sendRQ1(0x01, 0x40, 0x30); // 48 bytes
"""

gen_code = re.sub(r'    juce::uint8 sysexData\[\] = \{.*?    midiOutputQueue\.addEvent\(rq1, 0\);', request_replacement, gen_code, flags=re.DOTALL)

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/scratch/generate.py", "w") as f:
    f.write(gen_code)

print("generate.py rewritten!")
