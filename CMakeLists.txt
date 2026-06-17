cmake_minimum_required(VERSION 3.20)

project(SE02_Controller VERSION 1.0.0)

# Add JUCE using FetchContent
include(FetchContent)
FetchContent_Declare(
    juce
    URL https://github.com/juce-framework/JUCE/archive/refs/tags/8.0.0.zip
)
FetchContent_MakeAvailable(juce)

# Define the plugin
juce_add_plugin(SE02_Controller
    NEEDS_MIDI_INPUT TRUE
    NEEDS_MIDI_OUTPUT TRUE
    IS_MIDI_EFFECT FALSE
    IS_SYNTH TRUE
    FORMATS VST3 Standalone
    PRODUCT_NAME "SE-02 Controller"
    VERSION 1.0.0
    COMPANY_NAME "Antigravity"
    PLUGIN_MANUFACTURER_CODE "Antg"
    PLUGIN_CODE "Se02"
)

# Generate JuceHeader.h
juce_generate_juce_header(SE02_Controller)

# Source files
target_sources(SE02_Controller PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginProcessor.h
    Source/PluginEditor.cpp
    Source/PluginEditor.h
    Source/PresetBrowser.cpp
    Source/PresetBrowser.h
        )

# Add binary data
juce_add_binary_data(SE02_Controller_BinaryData
    HEADER_NAME "BinaryData.h"
    NAMESPACE BinaryData
    SOURCES
    Source/Resources/bg.png
    Source/Resources/grid_bg.png
)

# Compiler flags
target_compile_definitions(SE02_Controller
    PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
)

# Link JUCE modules
target_link_libraries(SE02_Controller
    PRIVATE
    SE02_Controller_BinaryData
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_gui_extra
    juce::juce_gui_basics
    juce::juce_graphics
    juce::juce_events
    juce::juce_core
    juce::juce_data_structures
    PUBLIC
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags
)

# Automatically copy the built VST3 plugin to the VST folder
set_target_properties(SE02_Controller_VST3 PROPERTIES VST3_COPY_DIR "C:/VST/ANTIGRAVITY_PLUGINS")
