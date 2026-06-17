import os

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

if '#include "PresetNames.h"' not in content:
    content = content.replace('#include "PluginProcessor.h"', '#include "PluginProcessor.h"\n#include "PresetNames.h"')

timer_old = '''void SE02_ControllerAudioProcessor::timerCallback()
{
    if (sysExDelayCounter.load() > 0)
    {
        int newCount = sysExDelayCounter.load() - 1;
        sysExDelayCounter.store(newCount);
        if (newCount == 0)
        {
            requestSysExPreset();
        }
    }'''

timer_new = '''void SE02_ControllerAudioProcessor::timerCallback()
{
    if (fetchState != FetchState::Idle)
    {
        processFetchStateMachine();
    }
    else if (sysExDelayCounter.load() > 0)
    {
        int newCount = sysExDelayCounter.load() - 1;
        sysExDelayCounter.store(newCount);
        if (newCount == 0)
        {
            requestSysExPreset();
        }
    }'''

if 'processFetchStateMachine()' not in content:
    content = content.replace(timer_old, timer_new)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

