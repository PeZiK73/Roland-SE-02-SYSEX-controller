import sys

with open('Source/PresetBrowser.cpp', 'r') as f:
    content = f.read()

old_focus = "setWantsKeyboardFocus(true);"
new_focus = """setWantsKeyboardFocus(true);
    fetchBankSelector.setWantsKeyboardFocus(false);
    fetchBankBtn.setWantsKeyboardFocus(false);
    closeBtn.setWantsKeyboardFocus(false);
    grabKeyboardFocus();"""

content = content.replace(old_focus, new_focus)

# In mouseDown, let's also grab focus
old_mouse = "selectedIndex = index;"
new_mouse = """selectedIndex = index;
                if (auto* pb = findParentComponentOfClass<PresetBrowser>())
                    pb->grabKeyboardFocus();"""

content = content.replace(old_mouse, new_mouse)

with open('Source/PresetBrowser.cpp', 'w') as f:
    f.write(content)
