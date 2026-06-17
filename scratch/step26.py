import sys

with open('Source/PresetBrowser.h', 'r') as f:
    content = f.read()

content = content.replace("void refreshData();", "void refreshData();\n    void updateFetchState();")

with open('Source/PresetBrowser.h', 'w') as f:
    f.write(content)

with open('Source/PresetBrowser.cpp', 'r') as f:
    content = f.read()

new_update = """
void PresetGrid::updateFetchState()
{
    // Only update the fetching booleans without rebuilding layouts or resizing
    juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
    juce::File presetsDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES");
    
    bool needsRepaint = false;
    int flatIndex = 0;
    
    for (auto& layout : bankLayouts)
    {
        if (layout.title == "CUSTOM PRESETS") {
            for (auto& cell : layout.cells) {
                flatCells[flatIndex] = cell;
                flatIndex++;
            }
            continue;
        }
        
        juce::File bankDir = presetsDir.getChildFile(layout.title);
        
        for (auto& cell : layout.cells)
        {
            bool fetchingThis = processor.isFetchingBank() && processor.getFetchBankName() == layout.title && processor.getFetchProgress() == (flatIndex % 128);
            
            if (cell.isCurrentlyFetching != fetchingThis) {
                cell.isCurrentlyFetching = fetchingThis;
                needsRepaint = true;
            }
            
            if (!cell.isFetched) {
                juce::String cleanName = cell.text.replaceCharacter('/', '_').replaceCharacter('\\\\', '_').replaceCharacter(':', '_').replaceCharacter('?', '_').replaceCharacter('\\"', '_').replaceCharacter('<', '_').replaceCharacter('>', '_').replaceCharacter('|', '_');
                juce::File prmFile = bankDir.getChildFile(cleanName + ".prm");
                
                if (prmFile.existsAsFile()) {
                    cell.isFetched = true;
                    cell.relativePath = layout.title + "/" + cleanName + ".prm";
                    needsRepaint = true;
                }
            }
            
            flatCells[flatIndex] = cell;
            flatIndex++;
        }
    }
}
"""

content = content.replace("void PresetGrid::paint(juce::Graphics& g)", new_update + "\nvoid PresetGrid::paint(juce::Graphics& g)")

content = content.replace("grid.refreshData();\n    grid.repaint();", "grid.updateFetchState();\n    grid.repaint();")

with open('Source/PresetBrowser.cpp', 'w') as f:
    f.write(content)
