#pragma once
#include <JuceHeader.h>
#include "PluginProcessor.h"
#include "PresetNames.h"

class BrowserLookAndFeel : public juce::LookAndFeel_V4
{
public:
    void drawScrollbar(juce::Graphics& g, juce::ScrollBar& scrollbar, int x, int y, int width, int height,
                       bool isScrollbarVertical, int thumbStartPosition, int thumbSize, bool isMouseOver, bool isMouseDown) override
    {
        juce::ignoreUnused(isMouseOver, isMouseDown);
        
        g.fillAll(juce::Colour(0xff121212)); // Scrollbar track background
        
        juce::Rectangle<float> thumbBounds;
        if (isScrollbarVertical) {
            thumbBounds = juce::Rectangle<float>(x + 2, thumbStartPosition + 2, width - 4, thumbSize - 4);
        } else {
            thumbBounds = juce::Rectangle<float>(thumbStartPosition + 2, y + 2, thumbSize - 4, height - 4);
        }
        
        g.setColour(juce::Colour(0xff00E5FF)); // Neon cyan thumb
        g.fillRoundedRectangle(thumbBounds, 3.0f);
    }
};

class PresetGrid : public juce::Component, private juce::Timer
{
public:
    PresetGrid(SE02_ControllerAudioProcessor& p, std::function<void(juce::String)> onSelect);
    void paint(juce::Graphics& g) override;
    void resized() override;
    void refreshData();
    void timerCallback() override;
    void mouseDown(const juce::MouseEvent& e) override;
    void mouseDoubleClick(const juce::MouseEvent& e) override;

    SE02_ControllerAudioProcessor& processor;
    std::function<void(juce::String)> onSelectCallback;
    std::function<void()> onMorphSelectionChanged;
    juce::String selectedPath;
    juce::String selectedMorphTarget;
    
    struct PatchCell {
        juce::Rectangle<int> bounds;
        juce::String text;
        int index = 0;
        juce::String name;
        juce::String path;
        bool isCurrentlyFetching = false;
        bool isPrm = false;
    };
    struct BankLayout {
        juce::String title;
        juce::Rectangle<int> titleBounds;
        std::vector<PatchCell> cells;
    };
    std::vector<BankLayout> bankLayouts;
};

class PresetBrowser : public juce::Component, public juce::KeyListener
{
public:
    PresetBrowser(SE02_ControllerAudioProcessor& p, std::function<void(juce::String)> onSelect, std::function<void()> onClose);
    ~PresetBrowser() override;
    void paint(juce::Graphics& g) override;
    void resized() override;
    
    // KeyListener overrides
    bool keyPressed(const juce::KeyPress& key, juce::Component* originatingComponent) override;
    
    juce::ComboBox bankSelector;
    juce::TextButton fetchBankBtn;
    juce::TextButton cancelBankBtn;
    juce::TextButton closeBtn;
    juce::TextButton rndPatchBtn;
    juce::ComboBox rndCategorySelector;
    juce::Label morphTooltip;
    
    juce::Slider morphSlider;
    juce::TextButton applyMorphBtn{"OK"};
    
    std::unique_ptr<PresetGrid> grid;
    juce::Viewport gridViewport;
    BrowserLookAndFeel customLookAndFeel;

    std::function<void(juce::String, juce::String, float)> onMorphChangeCallback;
    std::function<void(juce::String, juce::String)> onMorphApplyCallback;
    std::function<void(int)> onRndPatchCallback;

private:
    SE02_ControllerAudioProcessor& processor;
    std::function<void(juce::String)> onSelectCallback;
    std::function<void()> onCloseCallback;
};