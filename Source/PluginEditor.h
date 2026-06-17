#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"
#include "PresetBrowser.h"
#include <map>

class SE02LookAndFeel : public juce::LookAndFeel_V4
{
public:
    bool showValues = false;

    SE02LookAndFeel()
    {
        setColour(juce::Slider::textBoxTextColourId, juce::Colours::white);
        setColour(juce::Slider::textBoxOutlineColourId, juce::Colours::transparentBlack);
    }

    void drawRotarySlider (juce::Graphics& g, int x, int y, int width, int height, float sliderPos,
                           const float rotaryStartAngle, const float rotaryEndAngle, juce::Slider& slider) override
    {
        auto radius = (float) juce::jmin (width / 2, height / 2) - 4.0f;
        auto centreX = (float) x + (float) width  * 0.5f;
        auto centreY = (float) y + (float) height * 0.5f;
        auto rx = centreX - radius;
        auto ry = centreY - radius;
        auto rw = radius * 2.0f;
        auto angle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle);

        juce::ColourGradient silver (juce::Colour(0xffe0e0e0), centreX, ry, juce::Colour(0xff808080), centreX, ry + rw, false);
        g.setGradientFill (silver);
        g.fillEllipse (rx, ry, rw, rw);
        
        g.setColour(juce::Colour(0xff505050));
        g.drawEllipse(rx, ry, rw, rw, 1.0f);

        auto innerRadius = radius * 0.65f;
        g.setColour (juce::Colour(0xff111111));
        g.fillEllipse (centreX - innerRadius, centreY - innerRadius, innerRadius * 2.0f, innerRadius * 2.0f);

        juce::Path p;
        auto pointerLength = radius * 0.8f;
        auto pointerThickness = 2.5f;
        p.addRoundedRectangle (-pointerThickness * 0.5f, -radius * 0.9f, pointerThickness, pointerLength, 1.0f);
        p.applyTransform (juce::AffineTransform::rotation (angle).translated (centreX, centreY));
        g.setColour (juce::Colours::white);
        g.fillPath (p);

        if (showValues) {
            g.setColour(juce::Colours::yellow.withAlpha(0.5f));
            g.setFont(12.0f);
            juce::String text = juce::String(slider.getValue(), 0);
            g.drawText(text, x, y + height - 20, width, 20, juce::Justification::centred, false);
        }
    }
};

class SE02SwitchLookAndFeel : public juce::LookAndFeel_V4
{
public:
    bool showValues = false;

    void drawLinearSlider (juce::Graphics& g, int x, int y, int width, int height,
                           float sliderPos, float minSliderPos, float maxSliderPos,
                           const juce::Slider::SliderStyle style, juce::Slider& slider) override
    {
        g.setColour(juce::Colours::black);
        g.fillRect(x + width/2 - 5, y + 5, 10, height - 10);
        
        g.setColour(juce::Colours::white);
        g.fillRect(x + width/2 - 8, (int)sliderPos - 4, 16, 8);

        if (showValues) {
            g.setColour(juce::Colours::yellow.withAlpha(0.5f));
            g.setFont(12.0f);
            juce::String text = juce::String(slider.getValue(), 0);
            g.drawText(text, x, y + height - 16, width, 16, juce::Justification::centred, false);
        }
    }
};

class MainPanel;
class SE02_ControllerAudioProcessorEditor  : public juce::AudioProcessorEditor
{
public:
    SE02_ControllerAudioProcessorEditor (SE02_ControllerAudioProcessor&);
    ~SE02_ControllerAudioProcessorEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;
    void savePresetToFile(const juce::File& file);
    void loadPresetFromFile(const juce::File& file);
    
    std::map<juce::String, float> getPresetState(const juce::File& file, juce::String& outName);
    std::map<juce::String, float> stateA;
    std::map<juce::String, float> stateB;
    juce::String nameA;
    juce::String nameB;
    juce::String lastPathA;
    juce::String lastPathB;

private:
    std::unique_ptr<MainPanel> mainPanel;
    SE02_ControllerAudioProcessor& audioProcessor;
    
    SE02LookAndFeel customLookAndFeel;
    SE02SwitchLookAndFeel switchLookAndFeel;

    juce::ComponentBoundsConstrainer constrainer;
    juce::ResizableCornerComponent resizer;
    
    
    
    struct AttachedSlider {
        juce::Slider slider;
        juce::Label label; // Name label
                std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> attachment;
    };
    
    
    
    
    std::map<juce::String, std::unique_ptr<AttachedSlider>> sliders;

    void addKnob(const juce::String& id, const juce::String& name, int x, int y, int size);
    void addSwitch(const juce::String& id, const juce::String& name, int x, int y, int width, int height);
    void addBottomKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size);

    juce::ComboBox midiInSelector;
    juce::ComboBox midiOutSelector;
    juce::TextButton loadPresetBtn{"LOAD PRESET"};
    juce::ComboBox bankSelectorMain;

    juce::TextButton presetPrevBtn{"<"};
    juce::TextButton presetNextBtn{">"};
    juce::Label presetLabel;

    juce::TextButton browseBtn{"BROWSE"};
    juce::TextButton savePresetBtn{"SAVE PRESET"};

    std::unique_ptr<juce::FileChooser> fileChooser;
    
    std::unique_ptr<PresetBrowser> presetBrowser;
    
    
    


    juce::ToggleButton showValuesBtn{"SHOW PARAMETERS"};
    
    juce::StringArray getMidiInputNames() {
        juce::StringArray names;
        names.add("[ DAW Passthrough ]");
        for (auto info : juce::MidiInput::getAvailableDevices()) names.add(info.name);
        return names;
    }
    juce::StringArray getMidiOutputNames() {
        juce::StringArray names;
        names.add("[ DAW Passthrough ]");
        for (auto info : juce::MidiOutput::getAvailableDevices()) names.add(info.name);
        return names;
    }

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (SE02_ControllerAudioProcessorEditor)

};


