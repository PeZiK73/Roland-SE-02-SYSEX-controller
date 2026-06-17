import sys

with open('Source/PresetBrowser.h', 'r') as f:
    lines = f.readlines()

out = []
for line in lines:
    if "void refreshData();" in line:
        out.append(line)
        out.append("    void setSelectedIndex(int index) { selectedIndex = index; repaint(); }\n")
        out.append("    int getSelectedIndex() const { return selectedIndex; }\n")
        out.append("    int getNumCells() const { return flatCells.size(); }\n")
        out.append("    juce::Rectangle<int> getCellBounds(int index) const { return flatCells[index].bounds; }\n")
        out.append("    juce::String getCellPath(int index) const { return flatCells[index].relativePath; }\n")
        out.append("    bool triggerSelect(int index);\n")
    elif "std::vector<BankLayout> bankLayouts;" in line:
        out.append(line)
        out.append("    std::vector<PatchCell> flatCells;\n")
        out.append("    int selectedIndex = -1;\n")
    elif "void timerCallback() override;" in line:
        out.append(line)
        out.append("    bool keyPressed(const juce::KeyPress& key) override;\n")
    else:
        out.append(line)

with open('Source/PresetBrowser.h', 'w') as f:
    f.writelines(out)
