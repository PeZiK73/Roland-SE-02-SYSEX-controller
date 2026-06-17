#include "PluginProcessor.h"
#include "PresetNames.h"
#include <fstream>
#include "PluginEditor.h"

SE02_ControllerAudioProcessor::SE02_ControllerAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                     #endif
                       ),
       apvts(*this, nullptr, "Parameters", createParameterLayout())
#endif
{
    for (int i = 0; i < 128; ++i)
        incomingCcValues[i].store(-1.0f);

    // Start the timer immediately in the constructor.
    // The timer only touches atomic variables and sends MIDI, so it is safe
    // to run before prepareToPlay. We need it running even when the DAW
    // transport is stopped, otherwise MIDI sent via pushOutgoingMidiMessage
    // will pile up in the FIFO and never be drained by processBlock.
    startTimerHz(30);

    for (int i = 0; i < 256; ++i) {
        incomingSysExValues[i].store(-1.0f);
        currentSysExBuffer[i].store(-1.0f);
        syxParamMap[i] = "";
    }
    // DO NOT load global settings in the constructor. 
    // Stealing hardware MIDI ports during VST3 instantiation crashes Bitwig instantly.
    // loadGlobalSettings();
    
    syxParamMap[6] = "PWM_LFO_RATE";
    syxParamMap[7] = "PWM_LFO_DEPTH";
    
    syxParamMap[20] = "GLIDE";
    syxParamMap[21] = "GLIDE_TYPE";
    syxParamMap[22] = "WHL_MIX";
    
    syxParamMap[26] = "OSC1_RANGE";
    syxParamMap[27] = "OSC2_RANGE";
    syxParamMap[28] = "OSC3_RANGE";
    syxParamMap[29] = "OSC2_FINE";
    syxParamMap[30] = "OSC3_FINE";
    
    syxParamMap[31] = "OSC1_WAVE";
    syxParamMap[32] = "OSC2_WAVE";
    syxParamMap[33] = "OSC3_WAVE";
    syxParamMap[34] = "SYNC";
    syxParamMap[35] = "ENV1";
    syxParamMap[36] = "KYBD";
    syxParamMap[37] = "XMOD_MW";
    syxParamMap[42] = "XMOD_O2FLT";
    syxParamMap[43] = "XMOD_O3O2";
    syxParamMap[44] = "XMOD_O3PW";
    syxParamMap[45] = "MIX_OSC1";
    syxParamMap[46] = "MIX_OSC2";
    syxParamMap[47] = "MIX_OSC3";
    syxParamMap[48] = "MIX_FBACK";
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
}

SE02_ControllerAudioProcessor::~SE02_ControllerAudioProcessor() { stopTimer(); }
const juce::String SE02_ControllerAudioProcessor::getName() const { return JucePlugin_Name; }
bool SE02_ControllerAudioProcessor::acceptsMidi() const { return true; }
bool SE02_ControllerAudioProcessor::producesMidi() const { return true; }
bool SE02_ControllerAudioProcessor::isMidiEffect() const { return false; }
double SE02_ControllerAudioProcessor::getTailLengthSeconds() const { return 0.0; }
int SE02_ControllerAudioProcessor::getNumPrograms() { return 1; }
int SE02_ControllerAudioProcessor::getCurrentProgram() { return 0; }
void SE02_ControllerAudioProcessor::setCurrentProgram (int index) {}
const juce::String SE02_ControllerAudioProcessor::getProgramName (int index) { return {}; }
void SE02_ControllerAudioProcessor::changeProgramName (int index, const juce::String& newName) {}

void SE02_ControllerAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    stopTimer(); // Stop any previous timer before rebuilding ccParams
    ccParams.clear();
    ccParams.push_back({"GLIDE", 5});
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
    ccParams.push_back({"DLY_AMOUNT", 91});
    ccParams.push_back({"PWM_LFO_RATE", -1});
    ccParams.push_back({"PWM_LFO_DEPTH", -1});

    for (auto& cp : ccParams)
    {
        cp.param = apvts.getRawParameterValue(cp.id);
        if (cp.param != nullptr) {
            if (needsTotalRecall) cp.lastValue = -1.0f;
            else cp.lastValue = *cp.param;
        }
    }

    // Now safe to start the timer — ccParams is fully populated
    startTimerHz(30);

    // Deferred MIDI port opening: restore saved names
    if (lastMidiInName.isNotEmpty()) openMidiInput(lastMidiInName);
    if (lastMidiOutName.isNotEmpty()) openMidiOutput(lastMidiOutName);

    if (needsTotalRecall) {
        sendProgramChange();
        needsTotalRecall = false;
    }
}

void SE02_ControllerAudioProcessor::releaseResources() {}
bool SE02_ControllerAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
    return true;
  #else
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

   #if ! JucePlugin_IsSynth
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;
   #endif

    return true;
  #endif
}

void SE02_ControllerAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels  = getTotalNumInputChannels();

    for (auto i = totalNumInputChannels; i < buffer.getNumChannels(); ++i)
        buffer.clear (i, 0, buffer.getNumSamples());


    juce::MidiBuffer filteredMidi;
    for (const auto meta : midiMessages)
    {
        const auto msg = meta.getMessage();
        
        // DAW Passthrough mode: if direct port is closed, route incoming DAW MIDI to state machine
        if (!hardwareMidiIn) handleIncomingMidiMessage(nullptr, msg);
        
        if (msg.isAftertouch() || msg.isChannelPressure())
            continue;
            
        if (msg.isSysEx())
        {
            auto data = msg.getRawData();
            int size = msg.getRawDataSize();
            
            // F0 41 10 00 00 00 44 12
            if (size > 14 && data[1] == 0x41 && data[6] == 0x44 && data[7] == 0x12)
            {
                if (data[8] == 0x05 && data[9] == 0x00)
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
                            juce::Logger::writeToLog("SysEx_DUMP Byte " + juce::String(payloadOffset + i) + " = " + juce::String(b));
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

    // Process CCs
    bool blockCCs = (ccBlockTimer.load() > 0);
    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)
        {
            float currentVal = *cp.param;
            if (std::abs(currentVal - cp.lastValue) > 0.001f)
            {
                int newCcValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                int oldCcValue = juce::jlimit(0, 127, juce::roundToInt(cp.lastValue));
                
                // DECOUPLE OSC RANGE CCs
                if (cp.ccNumber == 22 || cp.ccNumber == 26 || cp.ccNumber == 30) // OSC1, 2, 3 Range
                {
                    int idxNew = juce::roundToInt((currentVal / 127.0f) * 5.0f);
                    idxNew = juce::jlimit(0, 5, idxNew);
                    int hwCCs[6] = {8, 24, 40, 56, 72, 88};
                    newCcValue = hwCCs[idxNew];
                    
                    int idxOld = juce::roundToInt((cp.lastValue / 127.0f) * 5.0f);
                    idxOld = juce::jlimit(0, 5, idxOld);
                    oldCcValue = hwCCs[idxOld];
                }
                
                if (newCcValue != oldCcValue || cp.lastValue < 0.0f) {
                    if (!blockCCs) {
                        if (cp.ccNumber >= 0 && cp.ccNumber <= 127) {
                            auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, newCcValue);
                            if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(message);
                            midiOutputQueue.addEvent(message, 0);
                        } else if (cp.ccNumber == -1) {
                            int paramIdx = -1;
                            for (int i = 0; i < 120; ++i) {
                                if (syxParamMap[i] == cp.id) { paramIdx = i; break; }
                            }
                            if (paramIdx >= 0) {
                                int rawByteIndex = paramIdx * 2;
                                juce::uint8 a2 = rawByteIndex / 128;
                                juce::uint8 a3 = rawByteIndex % 128;
                                
                                int totalSize = 16;
                                juce::MemoryBlock sysexData(totalSize, true);
                                juce::uint8* data = (juce::uint8*)sysexData.getData();
                                
                                data[0] = 0xF0; data[1] = 0x41; data[2] = 0x10; data[3] = 0x00;
                                data[4] = 0x00; data[5] = 0x00; data[6] = 0x44; data[7] = 0x12;
                                data[8] = 0x05; data[9] = 0x00; data[10] = a2; data[11] = a3;
                                
                                int syxVal;
                                if (cp.id == "PWM_LFO_RATE" || cp.id == "PWM_LFO_DEPTH") {
                                    syxVal = juce::roundToInt(currentVal);
                                } else {
                                    syxVal = juce::roundToInt((currentVal / 127.0f) * 255.0f);
                                }
                                
                                juce::uint8 nibble1 = (syxVal >> 4) & 0x0F;
                                juce::uint8 nibble2 = syxVal & 0x0F;
                                
                                data[12] = nibble1;
                                data[13] = nibble2;
                                
                                int sum = 0x05 + 0x00 + a2 + a3 + nibble1 + nibble2;
                                data[14] = (128 - (sum % 128)) & 0x7F;
                                data[15] = 0xF7;
                                
                                auto message = juce::MidiMessage((const void*)sysexData.getData(), sysexData.getSize());
                                if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(message);
                                midiOutputQueue.addEvent(message, 0);
                            }
                        }
                    }
                }
                cp.lastValue = currentVal;
            }
        }
    }

    // Process the lock-free FIFO queue containing outgoing messages from the GUI thread
    int start1, size1, start2, size2;
    outgoingMidiFifo.prepareToRead(1024, start1, size1, start2, size2);
    auto processFifoChunk = [&](int start, int size) {
        for (int i = 0; i < size; ++i) {
            auto msg = outgoingMidiBuffer[start + i];
            if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(msg);
            else midiOutputQueue.addEvent(msg, 0);
        }
    };
    if (size1 > 0) processFifoChunk(start1, size1);
    if (size2 > 0) processFifoChunk(start2, size2);
    outgoingMidiFifo.finishedRead(size1 + size2);

    midiMessages.addEvents(midiOutputQueue, 0, buffer.getNumSamples(), 0);
    midiOutputQueue.clear();
}

bool SE02_ControllerAudioProcessor::hasEditor() const { return true; }

void SE02_ControllerAudioProcessor::timerCallback()
{
    if (sysExDelayCounter.load() > 0) {
        sysExDelayCounter.fetch_sub(1);
    } else if (sysExDelayCounter.load() == 0) {
        if (sysExRequestPacket.load() < 4) {
            requestSysExPreset(sysExRequestPacket.load());
            sysExRequestPacket.fetch_add(1);
            if (sysExRequestPacket.load() < 4) {
                sysExDelayCounter.store(3); // 100ms between packets
            } else {
                sysExDelayCounter.store(-1);
            }
        } else if (sysExTransmitPacket.load() >= 0 && sysExTransmitPacket.load() <= 4) {
            // Pure Transmitter: Bit-Perfect 1-to-1 clone to Edit Buffer (05 00 00 00)
            int packetIndex = sysExTransmitPacket.load();
            auto sendDT1 = [&](juce::uint8 a1, juce::uint8 a2, juce::uint8 a3, int rawByteOffset, int byteCount) {
                int totalSize = 12 + byteCount + 2;
                juce::MemoryBlock sysexData(totalSize, true);
                juce::uint8* data = (juce::uint8*)sysexData.getData();
                
                data[0] = 0xF0; data[1] = 0x41; data[2] = 0x10; data[3] = 0x00;
                data[4] = 0x00; data[5] = 0x00; data[6] = 0x44; data[7] = 0x12;
                data[8] = 0x05; data[9] = a1; data[10] = a2; data[11] = a3; // Address 05 a1 a2 a3 (Temporary Patch)
                
                int sum = 0x05 + a1 + a2 + a3;
                for (int i = 0; i < byteCount; ++i) {
                    juce::uint8 b = (juce::uint8)outgoingSysExBuffer[rawByteOffset + i];
                    data[12 + i] = b;
                    sum += b;
                }
                
                juce::uint8 checksum = (128 - (sum % 128)) & 0x7F;
                data[totalSize - 2] = checksum;
                data[totalSize - 1] = 0xF7;
                
                juce::MidiMessage dt1((const void*)sysexData.getData(), sysexData.getSize());
                // Send directly to hardware - bypassing the FIFO which requires processBlock to drain
                if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(dt1);
                else pushOutgoingMidiMessage(dt1);
            };
            
            if (packetIndex == 0) sendDT1(0x00, 0x00, 0x00, 0, 64);      // 05 00 00 00
            else if (packetIndex == 1) sendDT1(0x00, 0x00, 0x40, 64, 64);  // 05 00 00 40
            else if (packetIndex == 2) sendDT1(0x00, 0x01, 0x00, 128, 64); // 05 00 01 00
            else if (packetIndex == 3) sendDT1(0x00, 0x01, 0x40, 192, 48); // 05 00 01 40
            else if (packetIndex == 4) {
                // Done transmitting to Edit Buffer. No Program Change needed!
                sysExTransmitPacket.store(-1);
                sysExDelayCounter.store(-1);
                return;
            }
            
            sysExTransmitPacket.fetch_add(1);
            if (sysExTransmitPacket.load() < 4) {
                sysExDelayCounter.store(3); // 100ms between DT1 packets
            } else {
                sysExTransmitPacket.store(-1);
                sysExDelayCounter.store(-1);
            }
        } else {
            sysExDelayCounter.store(-1);
        }
    }

    // Process CCs
    for (auto& cp : ccParams)
    {
        if (cp.ccNumber < 0 || cp.ccNumber >= 128) continue;
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
        if (hwVal >= 0.0f)
        {
            if (auto* param = apvts.getParameter(cp.id))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }
    
    processFetchStateMachine();

    if (ccBlockTimer.load() > 0) ccBlockTimer.fetch_sub(1);

    // Process SysEx
    for (int i = 0; i < 256; ++i)
    {
        float hwVal = incomingSysExValues[i].exchange(-1.0f);
        if (hwVal >= 0.0f && i < 120 && syxParamMap[i].isNotEmpty())
        {
            if (auto* param = apvts.getParameter(syxParamMap[i]))
            {
                float mappedVal = this->sysexToCc(syxParamMap[i], hwVal);
                
                if (!isFetchingBank()) {
                    param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                }
                
                for (auto& cp : ccParams) {
                    if (cp.id == syxParamMap[i]) {
                        cp.lastValue = mappedVal;
                    }
                }
            }
        }
    }
}


juce::String SE02_ControllerAudioProcessor::getPatchNameFromSysEx()
{
    // The SE-02 does not transmit patch names in the 240-byte SysEx payload.
    // The names are hardcoded in the ROM.
    if (isFetching) {
        if (fetchBankIndex == 0) return PresetNames::getBankA()[fetchPatchIndex];
        if (fetchBankIndex == 1) return PresetNames::getBankB()[fetchPatchIndex];
        if (fetchBankIndex == 2) return PresetNames::getBankC()[fetchPatchIndex];
        if (fetchBankIndex == 3) return PresetNames::getBankD()[fetchPatchIndex];
        if (fetchBankIndex == 4) return PresetNames::getUserBank()[fetchPatchIndex];
    }
    return "CustomPreset";
}

juce::String SE02_ControllerAudioProcessor::getBankName(int index) {
    if (index == 0) return "A";
    if (index == 1) return "B";
    if (index == 2) return "C";
    if (index == 3) return "D";
    if (index == 4) return "USER";
    return "A";
}

void SE02_ControllerAudioProcessor::sendProgramChange()
{
    int msb = 0;
    int lsb = 0;
    if (currentBankIndex == 0) msb = 0; // Bank A
    else if (currentBankIndex == 1) msb = 1; // Bank B
    else if (currentBankIndex == 2) msb = 2; // Bank C
    else if (currentBankIndex == 3) msb = 4; // Bank D
    else if (currentBankIndex == 4) msb = 3; // USER Bank
    int pc = currentPreset - 1; // 0-127
    
    // Send directly to hardware — bypassing the FIFO (which requires processBlock to drain)
    if (hardwareMidiOut) {
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
    } else {
        pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 0, msb));
        pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 32, lsb));
        pushOutgoingMidiMessage(juce::MidiMessage::programChange(1, pc));
    }
        
    // Wait ~330ms before requesting the SysEx patch so the synth has time to load it
    sysExRequestPacket.store(0);
    sysExDelayCounter.store(10);
}


void SE02_ControllerAudioProcessor::pushOutgoingMidiMessage(const juce::MidiMessage& msg)
{
    int start1, size1, start2, size2;
    outgoingMidiFifo.prepareToWrite(1, start1, size1, start2, size2);
    if (size1 > 0) {
        outgoingMidiBuffer[start1] = msg;
        outgoingMidiFifo.finishedWrite(1);
    }
}

void SE02_ControllerAudioProcessor::requestSysExPreset(int packetIndex)
{
    // Roland RQ1 Request (Data Request 1)
    // F0 41 {DeviceID} {ModelID} 11 {Address} {Size} {Checksum} F7
    // SE-02 Model ID is likely 00 00 00 3C or 00 00 00 48, Device ID is usually 10
    // Let's send a standard request to the temporary patch buffer.
    // Since we don't know the exact address yet, we'll try a common Roland structure 
    // and wait for the user to dump a patch so we can see the real address.
    
    // As a placeholder, we'll construct a dummy RQ1 just to trigger activity,
    // but the main goal right now is for the user to send a patch from the hardware!
    auto sendRQ1 = [&](juce::uint8 a1, juce::uint8 a2, juce::uint8 a3, juce::uint8 s3) {
        juce::uint8 sysexData[] = {
            0xF0, 0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 
            0x05, a1, a2, a3, 
            0x00, 0x00, 0x00, s3, 
            0x00, 0xF7
        };
        int sum = 0x05 + a1 + a2 + a3 + 0x00 + 0x00 + 0x00 + s3;
        sysexData[16] = (128 - (sum % 128)) % 128;

        juce::MidiMessage rq1(sysexData, sizeof(sysexData));
        // Send directly to hardware - bypassing the FIFO (which requires processBlock to drain)
        if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(rq1);
        else pushOutgoingMidiMessage(rq1);
    };

    
    if (packetIndex == -1 || packetIndex == 0) sendRQ1(0x00, 0x00, 0x00, 0x40); // 05 00 00 00
    if (packetIndex == -1 || packetIndex == 1) sendRQ1(0x00, 0x00, 0x40, 0x40); // 05 00 00 40
    if (packetIndex == -1 || packetIndex == 2) sendRQ1(0x00, 0x01, 0x00, 0x40); // 05 00 01 00
    if (packetIndex == -1 || packetIndex == 3) sendRQ1(0x00, 0x01, 0x40, 0x30); // 05 00 01 40

}


void SE02_ControllerAudioProcessor::openMidiInput(const juce::String& identifier)
{
    if (hardwareMidiIn) hardwareMidiIn->stop();
    hardwareMidiIn.reset();
    lastMidiInName = identifier;

    if (identifier == "[ DAW Passthrough ]") {
        saveGlobalSettings();
        return;
    }

    auto devs = juce::MidiInput::getAvailableDevices();
    for (auto& dev : devs) {
        if (dev.name == identifier) {
            hardwareMidiIn = juce::MidiInput::openDevice(dev.identifier, this);
            if (hardwareMidiIn) {
                hardwareMidiIn->start();
                saveGlobalSettings();
            }
            break;
        }
    }
}

void SE02_ControllerAudioProcessor::openMidiOutput(const juce::String& identifier)
{
    hardwareMidiOut.reset();
    lastMidiOutName = identifier;

    if (identifier == "[ DAW Passthrough ]") {
        saveGlobalSettings();
        return;
    }

    auto devs = juce::MidiOutput::getAvailableDevices();
    for (auto& dev : devs) {
        if (dev.name == identifier) {
            hardwareMidiOut = juce::MidiOutput::openDevice(dev.identifier);
            if (hardwareMidiOut) {
                saveGlobalSettings();
            }
            break;
        }
    }
}

void SE02_ControllerAudioProcessor::handleIncomingMidiMessage(juce::MidiInput* source, const juce::MidiMessage& msg)
{
    if (msg.isSysEx())
    {
        auto data = msg.getRawData();
        int size = msg.getRawDataSize();
        
        // F0 41 10 00 00 00 44 12
        if (size > 14 && data[1] == 0x41 && data[6] == 0x44 && data[7] == 0x12)
        {
            if (data[8] == 0x05 && data[9] == 0x00)
            {
                int a1 = data[9];
                int a2 = data[10];
                int a3 = data[11];
                
                int baseAddress = a2 * 128 + a3;
                int payloadOffset = 0;
                
                // Actual hardware sends 240 bytes (4 packets). 
                // We map this into an internal 240-byte array.
                if (baseAddress == 0x00) payloadOffset = 0;       // 05 00 00 00 (64 bytes)
                else if (baseAddress == 0x40) payloadOffset = 64; // 05 00 00 40 (64 bytes)
                else if (baseAddress == 0x80) payloadOffset = 128;// 05 00 01 00 (64 bytes)
                else if (baseAddress == 0xC0) payloadOffset = 192;// 05 00 01 40 (48 bytes)
                else return;
                
                const juce::uint8* payload = data + 12;
                int payloadSize = size - 14; // Un-nibblized raw bytes in this packet
                
                for (int i = 0; i < payloadSize; ++i)
                {
                    int rawByteIndex = payloadOffset + i;
                    
                    // 1. Pure Pipeline: Store exact raw byte to currentSysExBuffer
                    currentSysExBuffer[rawByteIndex].store((float)payload[i]);
                    
                    // 2. Hybrid Pipeline: Decode nibbles for GUI update
                    if (rawByteIndex < 214) {
                        if (i % 2 == 1) { 
                            int paramIndex = rawByteIndex / 2;
                            juce::uint8 b = ((payload[i - 1] & 0x0F) << 4) | (payload[i] & 0x0F);
                            incomingSysExValues[paramIndex].store((float)b);
                        }
                    } else if (rawByteIndex >= 214 && rawByteIndex < 240) {
                        int paramIndex = 107 + (rawByteIndex - 214);
                        incomingSysExValues[paramIndex].store((float)payload[i]);
                    }
                }
                ccBlockTimer.store(20); // Block CCs for 20 timer ticks (approx 600ms)
            }
        }
    }

        
    if (msg.isController())
    {
        int ccNum = msg.getControllerNumber();
        float val = (float)msg.getControllerValue();
        incomingCcValues[ccNum].store(val);
        
        for (auto& cp : ccParams)
        {
            if (cp.ccNumber == ccNum)
            {
                cp.lastValue = val;
            }
        }
    }
}

juce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor() 
{ 
    loadGlobalSettings();
    return new SE02_ControllerAudioProcessorEditor (*this); 
}

void SE02_ControllerAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{

    auto state = apvts.copyState();
    if (lastMidiInName.isNotEmpty()) state.setProperty("midiIn", lastMidiInName, nullptr);
    if (lastMidiOutName.isNotEmpty()) state.setProperty("midiOut", lastMidiOutName, nullptr);
    state.setProperty("currentBank", currentBankIndex, nullptr);
    state.setProperty("currentPreset", currentPreset, nullptr);

    std::unique_ptr<juce::XmlElement> xml (state.createXml());
    copyXmlToBinary (*xml, destData);

}

void SE02_ControllerAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{

    std::unique_ptr<juce::XmlElement> xmlState (getXmlFromBinary (data, sizeInBytes));
    if (xmlState.get() != nullptr)
    {
        if (xmlState->hasTagName (apvts.state.getType()))
        {
            auto vt = juce::ValueTree::fromXml (*xmlState);
            apvts.replaceState (vt);
            
            // Save MIDI port names for deferred opening in prepareToPlay.
            // Do NOT open ports here — this runs during plugin scan/load
            // and stealing MIDI ports crashes the host's sandbox engine.
            if (vt.hasProperty("midiIn")) lastMidiInName = vt.getProperty("midiIn").toString();
            if (vt.hasProperty("midiOut")) lastMidiOutName = vt.getProperty("midiOut").toString();
            if (vt.hasProperty("currentBank")) currentBankIndex = vt.getProperty("currentBank");
            if (vt.hasProperty("currentPreset")) currentPreset = vt.getProperty("currentPreset");
            needsTotalRecall = true;
        }
    }

}

juce::AudioProcessorValueTreeState::ParameterLayout SE02_ControllerAudioProcessor::createParameterLayout()
{
    juce::AudioProcessorValueTreeState::ParameterLayout layout;
    
    auto addCcParam = [&](const juce::String& id, const juce::String& name, float min, float max, float defaultVal) {
        layout.add(std::make_unique<juce::AudioParameterFloat>(
            juce::ParameterID(id, 1), name, juce::NormalisableRange<float>(min, max, 1.0f), defaultVal));
    };

    addCcParam("GLIDE", "GLIDE", 0.0f, 127.0f, 0.0f);
    addCcParam("GLIDE_TYPE", "TYPE", 0.0f, 127.0f, 0.0f);
    addCcParam("WHL_MIX", "WHL MIX", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC1_RANGE", "RANGE", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC1_TUNE", "TUNE", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC1_WAVE", "WAVEFORM", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC2_RANGE", "RANGE", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC2_FINE", "FINE", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC2_WAVE", "WAVEFORM", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC3_RANGE", "RANGE", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC3_FINE", "FINE", 0.0f, 127.0f, 0.0f);
    addCcParam("OSC3_WAVE", "WAVEFORM", 0.0f, 127.0f, 0.0f);
    addCcParam("SYNC", "SYNC", 0.0f, 127.0f, 0.0f);
    addCcParam("ENV1", "ENV1", 0.0f, 127.0f, 0.0f);
    addCcParam("KYBD", "KYBD", 0.0f, 127.0f, 0.0f);
    addCcParam("XMOD_MW", "TO MW", 0.0f, 127.0f, 0.0f);
    addCcParam("XMOD_O2FLT", "O2-FILTER", 0.0f, 127.0f, 0.0f);
    addCcParam("XMOD_O3O2", "O3-O2", 0.0f, 127.0f, 0.0f);
    addCcParam("XMOD_O3PW", "O3-PW1,2", 0.0f, 127.0f, 0.0f);
    addCcParam("MIX_OSC1", "OSC 1", 0.0f, 127.0f, 0.0f);
    addCcParam("MIX_OSC2", "OSC 2", 0.0f, 127.0f, 0.0f);
    addCcParam("MIX_OSC3", "OSC 3", 0.0f, 127.0f, 0.0f);
    addCcParam("MIX_FBACK", "FEEDBACK", 0.0f, 127.0f, 0.0f);
    addCcParam("MIX_NOISE", "NOISE", 0.0f, 127.0f, 0.0f);
    addCcParam("CUTOFF", "CUTOFF", 0.0f, 127.0f, 0.0f);
    addCcParam("EMPHASIS", "EMPHASIS", 0.0f, 127.0f, 0.0f);
    addCcParam("CONTOUR", "CONTOUR", 0.0f, 127.0f, 0.0f);
    addCcParam("KEYTRACK_13", "1/3", 0.0f, 127.0f, 0.0f);
    addCcParam("KEYTRACK_23", "2/3", 0.0f, 127.0f, 0.0f);
    addCcParam("MTRIG", "MTRIG", 0.0f, 127.0f, 0.0f);
    addCcParam("INVERT", "INVERT", 0.0f, 127.0f, 0.0f);
    addCcParam("REL", "REL", 0.0f, 127.0f, 0.0f);
    addCcParam("GATE_LFO", "LFO/GATE", 0.0f, 127.0f, 0.0f);
    addCcParam("FILT_ATTACK", "ATTACK", 0.0f, 127.0f, 0.0f);
    addCcParam("FILT_DECAY", "DECAY", 0.0f, 127.0f, 0.0f);
    addCcParam("FILT_SUSTAIN", "SUSTAIN", 0.0f, 127.0f, 0.0f);
    addCcParam("AMP_ATTACK", "ATTACK", 0.0f, 127.0f, 0.0f);
    addCcParam("AMP_DECAY", "DECAY", 0.0f, 127.0f, 0.0f);
    addCcParam("AMP_SUSTAIN", "SUSTAIN", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_RATE", "RATE", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_WAVE", "WAVE", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_OSC", "OSC", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_FILT", "FILTER", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_MW_OSC", "MWHL-OSC", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_MW_FLT", "MWHL-FLT", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_MODE", "MODE", 0.0f, 127.0f, 0.0f);
    addCcParam("LFO_SYNC", "SYNC", 0.0f, 127.0f, 0.0f);
    addCcParam("DLY_TIME", "TIME", 0.0f, 127.0f, 0.0f);
    addCcParam("DLY_REGEN", "REGEN", 0.0f, 127.0f, 0.0f);
    addCcParam("DLY_AMOUNT", "AMOUNT", 0.0f, 127.0f, 0.0f);
    addCcParam("PWM_LFO_RATE", "PWM RATE", 0.0f, 127.0f, 0.0f);
    addCcParam("PWM_LFO_DEPTH", "PWM DEPTH", 0.0f, 127.0f, 0.0f);

    return layout;
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter() { return new SE02_ControllerAudioProcessor(); }


void SE02_ControllerAudioProcessor::saveGlobalSettings() {
    juce::File settingsFile = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
        .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
        .getChildFile("settings.xml");
        
    settingsFile.getParentDirectory().createDirectory();
    
    juce::XmlElement xml("SE02_SETTINGS");
    xml.setAttribute("MidiIn", lastMidiInName);
    xml.setAttribute("MidiOut", lastMidiOutName);
    xml.writeTo(settingsFile);
}

void SE02_ControllerAudioProcessor::loadGlobalSettings() {
    juce::File settingsFile = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
        .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
        .getChildFile("settings.xml");
        
    if (settingsFile.existsAsFile()) {
        if (auto xml = juce::XmlDocument::parse(settingsFile)) {
            juce::String midiIn = xml->getStringAttribute("MidiIn");
            juce::String midiOut = xml->getStringAttribute("MidiOut");
            if (midiIn.isNotEmpty()) {
                lastMidiInName = midiIn;
                openMidiInput(midiIn);
            }
            if (midiOut.isNotEmpty()) {
                lastMidiOutName = midiOut;
                openMidiOutput(midiOut);
            }
        }
    }
}

// (Duplicate definitions removed — originals are on lines 692-723)


juce::String SE02_ControllerAudioProcessor::getFetchBankName() const
{
    switch (fetchBankIndex)
    {
        case 0: return "BANK_A";
        case 1: return "BANK_B";
        case 2: return "BANK_C";
        case 3: return "BANK_D";
        case 4: return "USER";
        default: return "UNKNOWN";
    }
}

bool SE02_ControllerAudioProcessor::doesPatchExistOnDisk(int bankIndex, int patchIndex)
{
    juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
    juce::File presetsDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES");
    
    juce::String bankFolderName;
    switch (bankIndex) {
        case 0: bankFolderName = "BANK_A"; break;
        case 1: bankFolderName = "BANK_B"; break;
        case 2: bankFolderName = "BANK_C"; break;
        case 3: bankFolderName = "BANK_D"; break;
        case 4: bankFolderName = "USER"; break;
        default: return false;
    }
    
    juce::File bankDir = presetsDir.getChildFile(bankFolderName);
    
    if (!bankDir.exists()) return false;
    
    juce::String prefix = juce::String(patchIndex + 1).paddedLeft('0', 3) + "_";
    juce::Array<juce::File> files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.syx");
    

    if (files.size() > 0) return true;
    files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.prm");
    
    return files.size() > 0;
}

void SE02_ControllerAudioProcessor::startFetchingBank(int bankIndex, bool skipExisting)
{
    if (isFetching || bankIndex >= 5) return;
    fetchBankIndex = juce::jlimit(0, 4, bankIndex);
    fetchPatchIndex = 0;
    skipExistingPatches = skipExisting;
    
    while (skipExistingPatches && fetchPatchIndex < 128 && doesPatchExistOnDisk(fetchBankIndex, fetchPatchIndex)) {
        fetchPatchIndex++;
    }
    
    if (fetchPatchIndex >= 128) {
        return;
    }
    
    isFetching = true;
    fetchPhase = 1; // Start phase 1
    fetchTimeoutCounter = 0;
}

void SE02_ControllerAudioProcessor::processFetchStateMachine()
{
    if (!isFetching) return;

    if (fetchPhase == 1) // Phase 1: Send Program Change
    {

        int msb = 0;
        int lsb = 0;
        if (fetchBankIndex == 0) msb = 0; // Bank A
        else if (fetchBankIndex == 1) msb = 1; // Bank B
        else if (fetchBankIndex == 2) msb = 2; // Bank C
        else if (fetchBankIndex == 3) msb = 4; // Bank D
        else if (fetchBankIndex == 4) msb = 3; // USER Bank
        int pc = fetchPatchIndex;
        
        // Send directly to hardware — bypassing the FIFO (which requires processBlock) 
        if (hardwareMidiOut) {
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
        } else {
            pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 0, msb));
            pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 32, lsb));
            pushOutgoingMidiMessage(juce::MidiMessage::programChange(1, pc));
        }
        
        fetchPhase = 2;
        fetchTimeoutCounter = 30; // Wait 1 second for hardware to change patch
    }
    else if (fetchPhase == 2) // Phase 2: Request SysEx
    {
        if (fetchTimeoutCounter > 0) {
            fetchTimeoutCounter--;
        } else {
            for (int i=0; i<256; ++i) currentSysExBuffer[i].store(-1.0f);
            sysExRequestPacket.store(0);
            sysExDelayCounter.store(1); // Trigger staggered SysEx sequence
            fetchPhase = 3;
            fetchTimeoutCounter = 15; // Wait ~0.5 seconds for reply
        }
    }
    else if (fetchPhase == 3) // Phase 3: Save to Disk
    {
        if (fetchTimeoutCounter > 0) {
            fetchTimeoutCounter--;
        } else {
            bool wasSavingCustom = isSavingCustomPreset.load();
            saveFetchedPresetToDisk();
            
            if (wasSavingCustom) {
                isFetching = false;
                fetchPhase = 0;
            } else {
                fetchPatchIndex++;
                while (skipExistingPatches && fetchPatchIndex < 128 && doesPatchExistOnDisk(fetchBankIndex, fetchPatchIndex)) {
                    fetchPatchIndex++;
                }
                
                if (fetchPatchIndex >= 128) {
                    isFetching = false;
                    fetchPhase = 0;
                } else {
                    fetchPhase = 1; // Loop back to next patch
                }
            }
        }
    }
}

void SE02_ControllerAudioProcessor::saveFetchedPresetToDisk()
{
    juce::File bankFolder;
    juce::String fileName;
    juce::String safeName = getPatchNameFromSysEx().replaceCharacter('/', '_').replaceCharacter('\\', '_');
    
    if (isSavingCustomPreset.load()) {
        if (customPresetSaveName.isNotEmpty()) {
            juce::String padded = customPresetSaveName.paddedRight(' ', 16).substring(0, 16);
            for (int i = 0; i < 16; ++i) {
                currentSysExBuffer[208 + i].store((float)padded[i]);
            }
        }
        
        bankFolder = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
            .getChildFile("SE-02_ANTIGRAVITIY_EDITOR")
            .getChildFile("CUSTOM_PRESETS");
        bankFolder.createDirectory();
        
        juce::Time now = juce::Time::getCurrentTime();
        if (customPresetSavePath.isNotEmpty()) {
            juce::File customFile(customPresetSavePath);
            bankFolder = customFile.getParentDirectory();
            fileName = customFile.getFileName();
        } else {
            fileName = "Preset_" + now.formatted("%Y%m%d_%H%M%S") + "_" + safeName + ".syx";
        }
        
        isSavingCustomPreset.store(false);
    } else {
        juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
        bankFolder = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES").getChildFile(getFetchBankName());
        bankFolder.createDirectory();
        fileName = juce::String(fetchPatchIndex + 1).paddedLeft('0', 3) + "_" + safeName + ".syx";
    }
    
    juce::File presetFile = bankFolder.getChildFile(fileName);
    
    juce::MemoryBlock block;
    block.setSize(240, true);
    for (int i = 0; i < 240; ++i) {
        float val = currentSysExBuffer[i].load();
        if (val >= 0.0f) {
            block[i] = (char)(juce::uint8)val;
        } else {
            block[i] = 0; // Default if no data
        }
    }
    presetFile.replaceWithData(block.getData(), block.getSize());
}

void SE02_ControllerAudioProcessor::updateGuiFromSysEx(const juce::MemoryBlock& patchData)
{
    if (patchData.getSize() != 240) return;
    
    // Block CCs so we don't spam the hardware while the GUI updates
    ccBlockTimer.store(40);
    
    const juce::uint8* data = (const juce::uint8*)patchData.getData();
    for (int i = 0; i < 107; ++i) {
        juce::uint8 highNibble = data[i * 2];
        juce::uint8 lowNibble = data[i * 2 + 1];
        juce::uint8 hwVal = (highNibble << 4) | (lowNibble & 0x0F);
        
        juce::String paramId = syxParamMap[i];
        if (paramId.isNotEmpty()) {
            if (auto* param = apvts.getParameter(paramId)) {
                float mappedVal = this->sysexToCc(paramId, (float)hwVal);
                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                
                // Update internal CC params to prevent feedback
                for (auto& cp : ccParams) {
                    if (cp.id == paramId) cp.lastValue = mappedVal;
                }
            }
        }
    }
}

float SE02_ControllerAudioProcessor::sysexToCc(const juce::String& id, float syxVal)
{
    int maxDiscrete = -1;
    
    // 2-position switches (0, 1)
    if (id == "GLIDE_TYPE" || id == "SYNC" || id == "KYBD" || 
        id == "KEYTRACK_13" || id == "KEYTRACK_23" || id == "MTRIG" || 
        id == "INVERT" || id == "LFO_MW_FLT" || id == "LFO_MW_OSC" || 
        id == "LFO_SYNC") {
        maxDiscrete = 1;
    } 
    // 3-position switches (0, 1, 2)
    else if (id == "XMOD_MW" || id == "LFO_MODE" || id == "REL" || id == "GATE_LFO") {
        maxDiscrete = 2;
    }
    // 6-position switches (0 to 5)
    else if (id == "OSC1_RANGE" || id == "OSC2_RANGE" || id == "OSC3_RANGE" || 
             id == "OSC1_WAVE" || id == "OSC2_WAVE" || id == "OSC3_WAVE" ||
             id == "LFO_WAVE") {
        maxDiscrete = 5;
    }
    
    if (maxDiscrete == 5) {
        // 6 positions: mathematically robust centers that evaluate correctly under any common synth division logic
        float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};
        return vals[juce::jlimit(0, 5, (int)syxVal)];
    } else if (maxDiscrete == 2) {
        // 3 positions
        float vals[3] = {0.0f, 64.0f, 127.0f};
        return vals[juce::jlimit(0, 2, (int)syxVal)];
    } else if (maxDiscrete == 1) {
        // 2 positions
        return syxVal > 0.0f ? 127.0f : 0.0f;
    }
    
    if (id == "PWM_LFO_RATE" || id == "PWM_LFO_DEPTH") {
        return syxVal;
    }
    
    // Continuous analog potentiometers (including Range knobs which are analog) use the full 0-255 scale
    return (syxVal / 255.0f) * 127.0f;
}

void SE02_ControllerAudioProcessor::transmitSysExPatch(const juce::MemoryBlock& patchData)
{
    outgoingSysExBuffer = patchData;
    // Set up state machine to send the 4 DT1 packets
    sysExRequestPacket.store(4); // Disable requests
    sysExTransmitPacket.store(0); // Enable transmits
    sysExDelayCounter.store(0); // Trigger the state machine immediately!
}



