import sys
import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Add pushOutgoingMidiMessage
if "void SE02_ControllerAudioProcessor::pushOutgoingMidiMessage" not in content:
    func = """
void SE02_ControllerAudioProcessor::pushOutgoingMidiMessage(const juce::MidiMessage& msg)
{
    int start1, size1, start2, size2;
    outgoingMidiFifo.prepareToWrite(1, start1, size1, start2, size2);
    if (size1 > 0) {
        outgoingMidiBuffer[start1] = msg;
        outgoingMidiFifo.finishedWrite(1);
    }
}
"""
    # Insert it right before requestSysExPreset
    content = content.replace("void SE02_ControllerAudioProcessor::requestSysExPreset()", func + "\nvoid SE02_ControllerAudioProcessor::requestSysExPreset()")

# 2. Fix sendProgramChange
send_pc_old = """    if (hardwareMidiOut) {
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));"""
send_pc_new = """    pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 0, msb));
    pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 32, lsb));
    pushOutgoingMidiMessage(juce::MidiMessage::programChange(1, pc));
    if (hardwareMidiOut) {"""
content = content.replace(send_pc_old, send_pc_new)

# 3. Fix requestSysExPreset
rq1_old = """        if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(rq1);
        else midiOutputQueue.addEvent(rq1, 0);"""
rq1_new = """        pushOutgoingMidiMessage(rq1);"""
content = content.replace(rq1_old, rq1_new)

# 4. Fix processFetchStateMachine
fetch_old = """        if (hardwareMidiOut) {
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
            hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
        }"""
fetch_new = """        pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 0, msb));
        pushOutgoingMidiMessage(juce::MidiMessage::controllerEvent(1, 32, lsb));
        pushOutgoingMidiMessage(juce::MidiMessage::programChange(1, pc));"""
content = content.replace(fetch_old, fetch_new)

# 5. Fix processBlock
process_block_old = """    midiMessages.addEvents(midiOutputQueue, 0, buffer.getNumSamples(), 0);
    midiOutputQueue.clear();"""
process_block_new = """    // Process the lock-free FIFO queue containing outgoing messages from the GUI thread
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
    midiOutputQueue.clear();"""

if "processFifoChunk" not in content:
    content = content.replace(process_block_old, process_block_new)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("Updated PluginProcessor.cpp")
