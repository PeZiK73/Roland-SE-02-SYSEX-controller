import sys

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

old_close = """                  [this]() {
                      presetBrowser = nullptr; // Close button
                  }"""

new_close = """                  [this]() {
                      juce::MessageManager::callAsync([this]() {
                          presetBrowser = nullptr; // Safe close
                      });
                  }"""

if new_close not in content:
    content = content.replace(old_close, new_close)
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(content)
        print("Fixed close button async callback")
else:
    print("Already fixed")
