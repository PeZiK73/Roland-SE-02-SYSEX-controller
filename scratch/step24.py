import sys

with open('Source/PresetBrowser.cpp', 'r') as f:
    content = f.read()

# Replace refreshData
old_refresh = content[content.find('void PresetGrid::refreshData()'):content.find('void PresetGrid::paint(juce::Graphics& g)')]
new_refresh = """void PresetGrid::refreshData()
{
    bankLayouts.clear();
    flatCells.clear();
    
    juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
    juce::File presetsDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES");
    
    int currentY = 0;
    int gridWidth = getWidth() > 0 ? getWidth() : 1000;
    int colWidth = gridWidth / 8;
    int rowHeight = 35; // Taller for button aesthetic
    int headerHeight = 50;
    
    auto addBank = [&](const juce::String& bankName, const juce::StringArray& hardcodedNames, int fetchBankIndex) {
        BankLayout layout;
        layout.title = bankName;
        layout.titleBounds = juce::Rectangle<int>(0, currentY, gridWidth, headerHeight);
        currentY += headerHeight;
        
        juce::File bankDir = presetsDir.getChildFile(bankName);
        
        for (int i = 0; i < 128; ++i)
        {
            if (i >= hardcodedNames.size()) break;
            
            juce::String name = hardcodedNames[i];
            juce::String cleanName = name.replaceCharacter('/', '_').replaceCharacter('\\\\', '_').replaceCharacter(':', '_').replaceCharacter('?', '_').replaceCharacter('\\"', '_').replaceCharacter('<', '_').replaceCharacter('>', '_').replaceCharacter('|', '_');
            juce::File prmFile = bankDir.getChildFile(cleanName + ".prm");
            
            int col = i / 16;
            int row = i % 16;
            
            PatchCell cell;
            cell.bounds = juce::Rectangle<int>(col * colWidth, currentY + row * rowHeight, colWidth, rowHeight);
            cell.text = name;
            
            bool fetchingThis = processor.isFetchingBank() && processor.getFetchBankName() == bankName && processor.getFetchProgress() == i;
            cell.isCurrentlyFetching = fetchingThis;
            
            if (prmFile.existsAsFile()) {
                cell.isFetched = true;
                cell.relativePath = bankName + "/" + cleanName + ".prm";
            } else {
                cell.isFetched = false;
                cell.relativePath = "";
            }
            
            layout.cells.push_back(cell);
            flatCells.push_back(cell);
        }
        
        currentY += 16 * rowHeight + 30; // padding below bank
        bankLayouts.push_back(layout);
    };
    
    addBank("BANK_A", PresetNames::getBankA(), 0);
    addBank("BANK_B", PresetNames::getBankB(), 1);
    addBank("BANK_C", PresetNames::getBankC(), 2);
    addBank("BANK_D", PresetNames::getBankD(), 3);
    addBank("USER", PresetNames::getUserBank(), 4);
    
    // CUSTOM folder
    BankLayout customLayout;
    customLayout.title = "CUSTOM PRESETS";
    customLayout.titleBounds = juce::Rectangle<int>(0, currentY, gridWidth, headerHeight);
    currentY += headerHeight;
    
    juce::File customDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("CUSTOM_PRESETS");
    if (customDir.isDirectory()) {
        juce::Array<juce::File> files;
        customDir.findChildFiles(files, juce::File::findFiles, false, "*.prm");
        for (int i = 0; i < files.size(); ++i) {
            int col = i / 16;
            int row = i % 16;
            PatchCell cell;
            cell.bounds = juce::Rectangle<int>(col * colWidth, currentY + row * rowHeight, colWidth, rowHeight);
            cell.text = files[i].getFileNameWithoutExtension();
            cell.relativePath = "../CUSTOM_PRESETS/" + files[i].getFileName();
            cell.isFetched = true;
            cell.isCurrentlyFetching = false;
            customLayout.cells.push_back(cell);
            flatCells.push_back(cell);
        }
        int maxRow = (files.size() > 0) ? 16 : 0;
        currentY += maxRow * rowHeight + 20;
    }
    bankLayouts.push_back(customLayout);
    
    setBounds(0, 0, gridWidth, currentY);
}

"""
content = content.replace(old_refresh, new_refresh)

# Replace paint and mouseDown
old_paint_mouse = content[content.find('void PresetGrid::paint(juce::Graphics& g)'):content.find('// --- PresetBrowser ---')]
new_paint_mouse = """void PresetGrid::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colour(0xff0a0a0a)); // Sleek dark background
    
    int globalIndex = 0;
    for (auto& layout : bankLayouts)
    {
        // Bank Header Background
        juce::Rectangle<float> headerBg(layout.titleBounds.getX() + 10, layout.titleBounds.getY() + 10, layout.titleBounds.getWidth() - 20, layout.titleBounds.getHeight() - 15);
        g.setGradientFill(juce::ColourGradient(juce::Colour(0xff1f1f1f), headerBg.getTopLeft(), juce::Colour(0xff111111), headerBg.getBottomLeft(), false));
        g.fillRoundedRectangle(headerBg, 5.0f);
        g.setColour(juce::Colour(0xff2a2a2a));
        g.drawRoundedRectangle(headerBg, 5.0f, 1.0f);
        
        // Bank Header Text
        g.setColour(juce::Colour(0xffff8c00)); // Neon orange
        g.setFont(juce::Font(22.0f, juce::Font::bold));
        g.drawText(layout.title, layout.titleBounds, juce::Justification::centred);
        
        g.setFont(juce::Font(13.0f, juce::Font::plain));
        for (auto& cell : layout.cells)
        {
            juce::Rectangle<float> cellRect = cell.bounds.reduced(3, 3).toFloat();
            
            bool isSelected = (globalIndex == selectedIndex);
            
            if (cell.isCurrentlyFetching) {
                // Pulsing yellow fetch outline
                g.setColour(juce::Colour(0xff333300));
                g.fillRoundedRectangle(cellRect, 4.0f);
                g.setColour(juce::Colour(0xffffff00));
                g.drawRoundedRectangle(cellRect, 4.0f, 2.0f);
                g.setColour(juce::Colour(0xffffff00));
            }
            else if (isSelected) {
                // Glowing cyan border for selected
                g.setGradientFill(juce::ColourGradient(juce::Colour(0xff2a3a4a), cellRect.getTopLeft(), juce::Colour(0xff1a2a3a), cellRect.getBottomLeft(), false));
                g.fillRoundedRectangle(cellRect, 4.0f);
                g.setColour(juce::Colour(0xff00ffff));
                g.drawRoundedRectangle(cellRect, 4.0f, 2.0f);
                g.setColour(juce::Colours::white);
                g.setFont(juce::Font(13.0f, juce::Font::bold));
            }
            else if (cell.isFetched) {
                // Active button
                g.setGradientFill(juce::ColourGradient(juce::Colour(0xff282828), cellRect.getTopLeft(), juce::Colour(0xff181818), cellRect.getBottomLeft(), false));
                g.fillRoundedRectangle(cellRect, 4.0f);
                g.setColour(juce::Colour(0xff3a3a3a));
                g.drawRoundedRectangle(cellRect, 4.0f, 1.0f);
                g.setColour(juce::Colour(0xffeeeeee));
                g.setFont(juce::Font(13.0f, juce::Font::plain));
            } else {
                // Dimmed button
                g.setColour(juce::Colour(0xff151515));
                g.fillRoundedRectangle(cellRect, 4.0f);
                g.setColour(juce::Colour(0xff1e1e1e));
                g.drawRoundedRectangle(cellRect, 4.0f, 1.0f);
                g.setColour(juce::Colour(0xff666666));
                g.setFont(juce::Font(13.0f, juce::Font::plain));
            }
            
            // Draw index/number
            juce::Rectangle<int> textRect = cellRect.toNearestInt();
            juce::String indexStr = juce::String(globalIndex + 1);
            g.setColour(g.getCurrentContext().getCurrentColour().withMultipliedAlpha(0.5f));
            g.setFont(juce::Font(10.0f));
            g.drawText(indexStr, textRect.withWidth(25).withX(textRect.getX() + 5), juce::Justification::centredLeft);
            
            // Draw patch name
            g.setColour(g.getCurrentContext().getCurrentColour().withMultipliedAlpha(2.0f)); // restore alpha
            g.setFont(isSelected ? juce::Font(13.0f, juce::Font::bold) : juce::Font(13.0f, juce::Font::plain));
            g.drawText(cell.text, textRect.withTrimmedLeft(28).withTrimmedRight(5), juce::Justification::centredLeft);
            
            globalIndex++;
        }
    }
}

bool PresetGrid::triggerSelect(int index)
{
    if (index >= 0 && index < flatCells.size()) {
        if (flatCells[index].isFetched && flatCells[index].relativePath.isNotEmpty()) {
            if (onSelectCallback) onSelectCallback(flatCells[index].relativePath);
            return true;
        }
    }
    return false;
}

void PresetGrid::mouseDown(const juce::MouseEvent& e)
{
    int index = 0;
    for (auto& layout : bankLayouts)
    {
        for (auto& cell : layout.cells)
        {
            if (cell.bounds.contains(e.getPosition()))
            {
                selectedIndex = index;
                repaint();
                triggerSelect(index);
                return;
            }
            index++;
        }
    }
}

"""
content = content.replace(old_paint_mouse, new_paint_mouse)

# Hook up Keyboard
old_timer = content[content.find('void PresetBrowser::timerCallback()'):content.find('void PresetBrowser::paint(juce::Graphics& g)')]
new_timer = """void PresetBrowser::timerCallback()
{
    if (processor.isFetchingBank()) {
        fetchBankBtn.setButtonText("FETCHING " + juce::String(processor.getFetchProgress()) + "/128");
    } else {
        fetchBankBtn.setButtonText("FETCH BANK");
    }
    
    // Periodically refresh the grid to show newly fetched files and the fetching cursor!
    grid.refreshData();
    grid.repaint();
}

bool PresetBrowser::keyPressed(const juce::KeyPress& key)
{
    int currentIndex = grid.getSelectedIndex();
    int newIndex = currentIndex;
    int numCells = grid.getNumCells();
    
    if (numCells == 0) return false;
    
    if (key.isKeyCode(juce::KeyPress::upKey)) {
        newIndex = currentIndex - 1; // Actually in an 8x16 grid, down goes +1, up goes -1, right goes +16, left goes -16?
        // Wait, the patches are added as col = i / 16, row = i % 16.
        // So visually:
        // i=0 is (col 0, row 0)
        // i=1 is (col 0, row 1) ... down
        // i=16 is (col 1, row 0) ... right
    } else if (key.isKeyCode(juce::KeyPress::downKey)) {
        newIndex = currentIndex + 1;
    } else if (key.isKeyCode(juce::KeyPress::leftKey)) {
        newIndex = currentIndex - 16;
    } else if (key.isKeyCode(juce::KeyPress::rightKey)) {
        newIndex = currentIndex + 16;
    } else if (key.isKeyCode(juce::KeyPress::returnKey)) {
        grid.triggerSelect(currentIndex);
        return true;
    } else {
        return false;
    }
    
    if (newIndex < 0) newIndex = 0;
    if (newIndex >= numCells) newIndex = numCells - 1;
    
    if (newIndex != currentIndex) {
        grid.setSelectedIndex(newIndex);
        
        juce::Rectangle<int> cellBounds = grid.getCellBounds(newIndex);
        
        // Custom logic to scroll viewport to keep cell in view
        int viewY = viewport.getViewPositionY();
        int viewH = viewport.getViewHeight();
        
        if (cellBounds.getY() < viewY) {
            viewport.setViewPosition(viewport.getViewPositionX(), cellBounds.getY() - 10);
        } else if (cellBounds.getBottom() > viewY + viewH) {
            viewport.setViewPosition(viewport.getViewPositionX(), cellBounds.getBottom() - viewH + 10);
        }
        
        grid.triggerSelect(newIndex);
        return true;
    }
    
    return true;
}

"""
content = content.replace(old_timer, new_timer)

# Ensure setWantsKeyboardFocus in constructor
constructor_sig = "PresetBrowser::PresetBrowser(SE02_ControllerAudioProcessor& p, std::function<void(juce::String)> onSelect, std::function<void()> onClose)"
if constructor_sig in content:
    idx = content.find('{', content.find(constructor_sig)) + 1
    content = content[:idx] + "\n    setWantsKeyboardFocus(true);\n" + content[idx:]

with open('Source/PresetBrowser.cpp', 'w') as f:
    f.write(content)
