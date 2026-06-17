import sys

with open('Source/PresetBrowser.cpp', 'r') as f:
    content = f.read()

old_destructor = """PresetBrowser::~PresetBrowser()
{
    stopTimer();
}"""

new_destructor = """PresetBrowser::~PresetBrowser()
{
    stopTimer();
    viewport.setViewedComponent(nullptr, false);
}"""

if new_destructor not in content:
    content = content.replace(old_destructor, new_destructor)
    with open('Source/PresetBrowser.cpp', 'w') as f:
        f.write(content)
        print("Fixed PresetBrowser destructor")
else:
    print("Already fixed")
