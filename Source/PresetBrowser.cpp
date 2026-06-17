#include "PresetBrowser.h"

// --- PresetGrid ---

PresetGrid::PresetGrid(SE02_ControllerAudioProcessor& p, std::function<void(juce::String)> onSelect)
    : processor(p), onSelectCallback(onSelect)
{
    refreshData();
    startTimerHz(15); // Repaint often to show fetching status
}

void PresetGrid::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colour(0xff121212));
    
    for (auto& layout : bankLayouts)
    {
        // Draw the large dark grey rounded panel for the bank
        juce::Rectangle<int> panelBounds(10, layout.titleBounds.getY() - 10, getWidth() - 20, (16 * 28) + 50);
        g.setColour(juce::Colour(0xff181818));
        g.fillRoundedRectangle(panelBounds.toFloat(), 8.0f);
        
        g.setFont(juce::Font(18.0f, juce::Font::bold));
        g.setColour(juce::Colour(0xffFF8C00)); // Bright Orange
        g.drawText(layout.title, layout.titleBounds, juce::Justification::centred, true);
        
        for (auto& cell : layout.cells)
        {
            bool fileExists = cell.path.isNotEmpty();
            bool isSelected = (fileExists && cell.path == selectedPath);
            bool isMorphTarget = (fileExists && cell.path == selectedMorphTarget);
            juce::Rectangle<int> innerBounds = cell.bounds.reduced(2);
            
            // Cell Background
            g.setColour(juce::Colour(0xff1a1a1a));
            g.fillRoundedRectangle(innerBounds.toFloat(), 4.0f);
            
            // Left square for number
            juce::Rectangle<int> numberBox(innerBounds.getX(), innerBounds.getY(), 30, innerBounds.getHeight());
            g.setColour(juce::Colour(0xff101010));
            g.fillRoundedRectangle(numberBox.toFloat(), 4.0f);
            
            // Draw Number
            g.setFont(juce::Font(11.0f, juce::Font::bold));
            g.setColour(juce::Colour(0xff555555));
            g.drawText(juce::String(cell.index), numberBox, juce::Justification::centred, true);

            // Text Setup
            g.setFont(juce::Font(11.0f, juce::Font::bold));
            juce::Rectangle<int> textBox = innerBounds.withTrimmedLeft(38);
            
            if (cell.isCurrentlyFetching) {
                g.setColour(juce::Colour(0xffFFD700)); // Yellow fetching border
                g.drawRoundedRectangle(innerBounds.toFloat(), 4.0f, 2.0f);
                g.setColour(juce::Colours::white);
                g.drawText(cell.name, textBox, juce::Justification::centredLeft, true);
            } else if (isMorphTarget) {
                g.setColour(juce::Colour(0xff00FF00)); // Green morph target border
                g.drawRoundedRectangle(innerBounds.toFloat(), 4.0f, 2.0f);
                g.setColour(juce::Colours::white);
                g.drawText(cell.name, textBox, juce::Justification::centredLeft, true);
            } else if (isSelected) {
                g.setColour(juce::Colour(0xff00E5FF)); // Cyan selection border
                g.drawRoundedRectangle(innerBounds.toFloat(), 4.0f, 2.0f);
                g.setColour(juce::Colours::white);
                g.drawText(cell.name, textBox, juce::Justification::centredLeft, true);
            } else if (!fileExists) {
                g.setColour(juce::Colour(0xff444444)); // Dim text if missing
                g.drawText(cell.name, textBox, juce::Justification::centredLeft, true);
            } else {
                g.setColour(juce::Colour(0xff333333)); // Border
                g.drawRoundedRectangle(innerBounds.toFloat(), 4.0f, 1.0f);
                
                if (cell.isPrm) {
                    g.setColour(juce::Colour(0xffe5b73b).withAlpha(0.5f)); // Mustard yellow 50% transparent
                } else {
                    g.setColour(juce::Colour(0xffaaaaaa)); // Normal text
                }
                
                g.drawText(cell.name, textBox, juce::Justification::centredLeft, true);
            }
        }
    }
}

void PresetGrid::resized()
{
    refreshData();
}

void PresetGrid::refreshData()
{
    bankLayouts.clear();
    
    juce::File docsDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory);
    juce::File presetsDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("HARDWARE_PATCHES");
    juce::File customDir = docsDir.getChildFile("SE-02_ANTIGRAVITIY_EDITOR").getChildFile("CUSTOM_PRESETS");
    
    int gridWidth = getWidth() > 0 ? getWidth() : 2000;
    int colWidth = (gridWidth - 40) / 8; // 8 columns with 20px padding on each side
    int rowHeight = 28;
    int currentY = 10;
    
    auto addBank = [&](const juce::String& bankId, const juce::String& displayName, int bankIndex) {
        BankLayout layout;
        layout.title = displayName;
        layout.titleBounds = juce::Rectangle<int>(20, currentY, gridWidth - 40, 30);
        currentY += 35;
        
        if (bankId == "CUSTOM") {
            customDir.createDirectory();
            juce::Array<juce::File> files;
            files.addArray(customDir.findChildFiles(juce::File::findFiles, false, "*.syx"));
            files.addArray(customDir.findChildFiles(juce::File::findFiles, false, "*.prm"));
            
            std::sort(files.begin(), files.end(), [](const juce::File& a, const juce::File& b) {
                return a.getFileName().compareIgnoreCase(b.getFileName()) < 0;
            });
            
            for (int i = 0; i < files.size(); ++i) {
                juce::File f = files[i];
                int col = i % 8;
                int row = i / 8;
                
                PatchCell cell;
                cell.bounds = juce::Rectangle<int>(20 + col * colWidth, currentY + row * rowHeight, colWidth, rowHeight);
                cell.index = i + 1;
                juce::String ext = f.getFileExtension().toUpperCase();
                if (ext == ".PRM") ext = " PRM";
                else if (ext == ".SYX") ext = " SYX";
                else ext = "";
                cell.name = f.getFileNameWithoutExtension().replaceCharacter('_', ' ') + ext;
                cell.path = f.getFullPathName();
                cell.isPrm = f.getFileExtension().toLowerCase() == ".prm";
                
                layout.cells.push_back(cell);
            }
            int numRows = (files.size() + 7) / 8;
            if (numRows == 0) numRows = 1;
            currentY += (numRows * rowHeight) + 20;
        }
        else {
            juce::File bankDir = presetsDir.getChildFile(bankId);
            for (int i = 0; i < 128; ++i)
            {
                juce::String prefix = juce::String(i + 1).paddedLeft('0', 3) + "_";
                juce::Array<juce::File> files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.syx");
                if (files.isEmpty()) files = bankDir.findChildFiles(juce::File::findFiles, false, prefix + "*.prm");
                
                juce::String name = "Empty";
                juce::String path = "";
                bool exists = false;
                bool isPrm = false;
                
                if (files.size() > 0) {
                    exists = true;
                    path = files[0].getFullPathName();
                    name = files[0].getFileNameWithoutExtension().substring(4);
                    name = name.replaceCharacter('_', ' ');
                    juce::String ext = files[0].getFileExtension().toUpperCase();
                    if (ext == ".PRM") ext = " PRM";
                    else if (ext == ".SYX") ext = " SYX";
                    else ext = "";
                    name = name + ext;
                    isPrm = files[0].getFileExtension().toLowerCase() == ".prm";
                } else {
                    name = "Not fetched";
                }
                
                int col = i / 16;
                int row = i % 16;
                
                PatchCell cell;
                cell.bounds = juce::Rectangle<int>(20 + col * colWidth, currentY + row * rowHeight, colWidth, rowHeight);
                cell.index = i + 1;
                cell.name = name;
                cell.isCurrentlyFetching = processor.isFetchingBank() && processor.getFetchBankName() == bankId && processor.getFetchProgress() == i;
                cell.isPrm = isPrm;
                if (exists) cell.path = path;
                
                layout.cells.push_back(cell);
            }
            currentY += (16 * rowHeight) + 20;
        }
        bankLayouts.push_back(layout);
    };
    
    addBank("BANK_A", "BANK A", 0);
    addBank("BANK_B", "BANK B", 1);
    addBank("BANK_C", "BANK C", 2);
    addBank("BANK_D", "BANK D", 3);
    addBank("USER", "USER", 4);
    addBank("CUSTOM", "CUSTOM", 5);
    
    setSize(gridWidth, currentY);
}

void PresetGrid::mouseDown(const juce::MouseEvent& e)
{
    for (auto& layout : bankLayouts)
    {
        for (auto& cell : layout.cells)
        {
            if (cell.bounds.contains(e.getPosition()))
            {
                if (cell.path.isNotEmpty() && onSelectCallback != nullptr) {
                    if (e.mods.isShiftDown() && selectedPath.isNotEmpty() && cell.path != selectedPath) {
                        selectedMorphTarget = cell.path;
                    } else {
                        selectedPath = cell.path;
                        selectedMorphTarget = juce::String();
                        onSelectCallback(cell.path);
                    }
                    repaint();
                    if (onMorphSelectionChanged) onMorphSelectionChanged();
                }
                return;
            }
        }
    }
}

void PresetGrid::mouseDoubleClick(const juce::MouseEvent& e)
{
    for (auto& layout : bankLayouts)
    {
        for (auto& cell : layout.cells)
        {
            if (cell.bounds.contains(e.getPosition()))
            {
                if (cell.path.isNotEmpty()) {
                    auto* aw = new juce::AlertWindow("Rename Patch", "Enter a new name for this patch (max 16 characters):", juce::MessageBoxIconType::NoIcon);
                    aw->addTextEditor("newName", cell.name, "New Name:");
                    aw->addButton("Rename", 1, juce::KeyPress(juce::KeyPress::returnKey, 0, 0));
                    aw->addButton("Cancel", 0, juce::KeyPress(juce::KeyPress::escapeKey, 0, 0));

                    juce::String currentPath = cell.path;

                    aw->enterModalState(true, juce::ModalCallbackFunction::create([this, aw, currentPath](int result) {
                        if (result == 1) {
                            juce::String newName = aw->getTextEditorContents("newName").substring(0, 16);
                            juce::String cleanName = newName.replaceCharacter('/', '_').replaceCharacter('\\', '_').replaceCharacter(':', '_').replaceCharacter('?', '_').replaceCharacter('"', '_').replaceCharacter('<', '_').replaceCharacter('>', '_').replaceCharacter('|', '_');
                            
                            juce::File oldFile(currentPath);
                            juce::File newFile = oldFile.getSiblingFile(oldFile.getFileNameWithoutExtension().substring(0, 4) + cleanName + oldFile.getFileExtension());
                            
                            if (oldFile.existsAsFile()) {
                                juce::MemoryBlock data;
                                oldFile.loadFileAsData(data);
                                if (data.getSize() == 240) {
                                    juce::String paddedName = newName.paddedRight(' ', 16);
                                    for (int i=0; i<16; ++i) {
                                        data[208 + i] = (juce::uint8)paddedName[i];
                                    }
                                    oldFile.replaceWithData(data.getData(), data.getSize());
                                }
                                oldFile.moveFileTo(newFile);
                                this->refreshData();
                                this->repaint();
                            }
                        }
                        delete aw;
                    }));
                }
                return;
            }
        }
    }
}

void PresetGrid::timerCallback()
{
    if (processor.isFetchingBank()) {
        refreshData();
        repaint();
    }
}

// --- PresetBrowser ---

PresetBrowser::PresetBrowser(SE02_ControllerAudioProcessor& p, std::function<void(juce::String)> onSelect, std::function<void()> onClose)
    : processor(p), onSelectCallback(onSelect), onCloseCallback(onClose)
{
    grid = std::make_unique<PresetGrid>(processor, onSelect);
    
    gridViewport.setLookAndFeel(&customLookAndFeel);
    gridViewport.setViewedComponent(grid.get(), false);
    gridViewport.setScrollBarsShown(true, false);
    addAndMakeVisible(gridViewport);
    
    // Intercept keys before the viewport uses them to scroll
    grid->addKeyListener(this);
    gridViewport.addKeyListener(this);
    
    setWantsKeyboardFocus(true);
    
    addAndMakeVisible(bankSelector);
    bankSelector.addItem("BANK A", 1);
    bankSelector.addItem("BANK B", 2);
    bankSelector.addItem("BANK C", 3);
    bankSelector.addItem("BANK D", 4);
    bankSelector.addItem("USER", 5);
    bankSelector.addItem("CUSTOM", 6);
    bankSelector.setSelectedId(1, juce::dontSendNotification);
    bankSelector.setColour(juce::ComboBox::backgroundColourId, juce::Colour(0xff222222));
    bankSelector.setColour(juce::ComboBox::outlineColourId, juce::Colour(0xff555555));

    addAndMakeVisible(fetchBankBtn);
    fetchBankBtn.setButtonText("FETCH BANK");
    fetchBankBtn.setColour(juce::TextButton::buttonColourId, juce::Colour(0xff333333));
    fetchBankBtn.onClick = [this] {
        juce::PopupMenu menu;
        menu.addItem(1, "Fetch ALL Patches in Bank (Overwrite)");
        menu.addItem(2, "Fetch MISSING Patches Only (Resume)");
        
        menu.showMenuAsync(juce::PopupMenu::Options().withTargetComponent(&fetchBankBtn),
            [this](int result) {
                if (result == 1) {
                    processor.startFetchingBank(bankSelector.getSelectedId() - 1, false);
                } else if (result == 2) {
                    processor.startFetchingBank(bankSelector.getSelectedId() - 1, true);
                }
            });
    };

    addAndMakeVisible(cancelBankBtn);
    cancelBankBtn.setButtonText("CANCEL");
    cancelBankBtn.setColour(juce::TextButton::buttonColourId, juce::Colour(0xff553333));
    cancelBankBtn.onClick = [this] {
        processor.cancelFetchingBank();
    };
    
    addAndMakeVisible(closeBtn);
    closeBtn.setButtonText("X");
    closeBtn.setColour(juce::TextButton::buttonColourId, juce::Colour(0xffdd4444));
    closeBtn.onClick = [this] {
        if (onCloseCallback) onCloseCallback();
    };

    addAndMakeVisible(rndPatchBtn);
    rndPatchBtn.setButtonText("RND PATCH");
    rndPatchBtn.setColour(juce::TextButton::buttonColourId, juce::Colour(0xff235E36));
    rndPatchBtn.setColour(juce::TextButton::textColourOffId, juce::Colour(0xffFFD700));
    rndPatchBtn.onClick = [this] {
        if (onRndPatchCallback) onRndPatchCallback(rndCategorySelector.getSelectedId());
    };
    
    addAndMakeVisible(rndCategorySelector);
    rndCategorySelector.addItem("ANY", 1);
    rndCategorySelector.addItem("BASS", 2);
    rndCategorySelector.addItem("LEAD", 3);
    rndCategorySelector.addItem("PLUCK", 4);
    rndCategorySelector.addItem("PAD", 5);
    rndCategorySelector.setSelectedId(1, juce::dontSendNotification);
    rndCategorySelector.setColour(juce::ComboBox::backgroundColourId, juce::Colour(0xff222222));
    rndCategorySelector.setColour(juce::ComboBox::outlineColourId, juce::Colour(0xff235E36));
    
    addAndMakeVisible(morphTooltip);
    morphTooltip.setText("Select second patch with [SHIFT] to enable MORPH feature", juce::dontSendNotification);
    morphTooltip.setColour(juce::Label::textColourId, juce::Colour(0xff235E36));
    morphTooltip.setFont(juce::Font(12.0f, juce::Font::bold));

    addChildComponent(morphSlider);
    morphSlider.setSliderStyle(juce::Slider::LinearHorizontal);
    morphSlider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    morphSlider.setRange(0.0, 1.0, 0.01);
    morphSlider.onValueChange = [this] {
        if (onMorphChangeCallback && grid->selectedPath.isNotEmpty() && grid->selectedMorphTarget.isNotEmpty()) {
            onMorphChangeCallback(grid->selectedPath, grid->selectedMorphTarget, morphSlider.getValue());
        }
    };
    
    addChildComponent(applyMorphBtn);
    applyMorphBtn.setColour(juce::TextButton::buttonColourId, juce::Colour(0xff44dd44));
    applyMorphBtn.onClick = [this] {
        if (onMorphApplyCallback && grid->selectedPath.isNotEmpty() && grid->selectedMorphTarget.isNotEmpty()) {
            onMorphApplyCallback(grid->selectedPath, grid->selectedMorphTarget);
            grid->selectedMorphTarget = juce::String();
            grid->repaint();
            resized();
        }
    };

    grid->onMorphSelectionChanged = [this] {
        morphSlider.setValue(0.0, juce::dontSendNotification);
        resized();
    };
}

PresetBrowser::~PresetBrowser()
{
    if (grid != nullptr) grid->removeKeyListener(this);
    gridViewport.removeKeyListener(this);
    gridViewport.setLookAndFeel(nullptr);
}

void PresetBrowser::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colour(0xff121212));
    
    // Draw top bar
    g.setColour(juce::Colour(0xff181818));
    g.fillRect(0, 0, getWidth(), 40);
    g.setColour(juce::Colour(0xff333333));
    g.drawLine(0, 40, getWidth(), 40);
    
    g.setFont(juce::Font(16.0f, juce::Font::bold));
    g.setColour(juce::Colours::lightgrey);
    g.drawText("PRESET BROWSER", 15, 0, 200, 40, juce::Justification::centredLeft, true);
}

void PresetBrowser::resized()
{
    int topBarY = 8;
    int controlHeight = 24;
    int rightMargin = 10;
    
    closeBtn.setBounds(getWidth() - rightMargin - 30, topBarY, 30, controlHeight);
    cancelBankBtn.setBounds(closeBtn.getX() - 10 - 70, topBarY, 70, controlHeight);
    fetchBankBtn.setBounds(cancelBankBtn.getX() - 10 - 100, topBarY, 100, controlHeight);
    bankSelector.setBounds(fetchBankBtn.getX() - 10 - 100, topBarY, 100, controlHeight);
    
    rndPatchBtn.setBounds(160, topBarY, 90, controlHeight);
    rndCategorySelector.setBounds(rndPatchBtn.getRight() + 10, topBarY, 80, controlHeight);
    morphTooltip.setBounds(rndCategorySelector.getRight() + 10, topBarY, 400, controlHeight);
    
    bool isMorphing = grid->selectedMorphTarget.isNotEmpty() && grid->selectedPath.isNotEmpty();
    int morphAreaHeight = isMorphing ? 50 : 0;
    
    gridViewport.setBounds(10, 50, getWidth() - 20, getHeight() - 60 - morphAreaHeight);
    
    if (isMorphing) {
        morphSlider.setVisible(true);
        applyMorphBtn.setVisible(true);
        morphSlider.setBounds(10, getHeight() - 50, getWidth() - 120, 40);
        applyMorphBtn.setBounds(getWidth() - 100, getHeight() - 45, 90, 30);
    } else {
        morphSlider.setVisible(false);
        applyMorphBtn.setVisible(false);
    }
}

bool PresetBrowser::keyPressed(const juce::KeyPress& key, juce::Component* originatingComponent)
{
    juce::ignoreUnused(originatingComponent);
    
    if (grid == nullptr || grid->bankLayouts.empty()) return false;
    
    // Flatten all cells into a single list to make navigation easier
    std::vector<PresetGrid::PatchCell*> allCells;
    int currentIndex = -1;
    
    for (auto& layout : grid->bankLayouts) {
        for (auto& cell : layout.cells) {
            allCells.push_back(&cell);
            if (cell.path == grid->selectedPath && grid->selectedPath.isNotEmpty()) {
                currentIndex = (int)allCells.size() - 1;
            }
        }
    }
    
    if (allCells.empty()) return false;
    if (currentIndex == -1) currentIndex = 0; // Default to first cell if nothing selected
    
    int cols = 8;
    int nextIndex = currentIndex;
    
    if (key.isKeyCode(juce::KeyPress::upKey)) {
        nextIndex = currentIndex - 1;
    } else if (key.isKeyCode(juce::KeyPress::downKey)) {
        nextIndex = currentIndex + 1;
    } else if (key.isKeyCode(juce::KeyPress::leftKey)) {
        nextIndex = currentIndex - 16;
    } else if (key.isKeyCode(juce::KeyPress::rightKey)) {
        nextIndex = currentIndex + 16;
    } else if (key.isKeyCode(juce::KeyPress::returnKey)) {
        if (allCells[currentIndex]->path.isNotEmpty() && onSelectCallback) {
            onSelectCallback(allCells[currentIndex]->path);
        }
        return true;
    } else {
        return false;
    }
    
    nextIndex = juce::jlimit(0, (int)allCells.size() - 1, nextIndex);
    
    auto* targetCell = allCells[nextIndex];
    if (targetCell->path.isNotEmpty()) {
        grid->selectedPath = targetCell->path;
        grid->repaint();
        if (onSelectCallback) onSelectCallback(targetCell->path);
        
        // Auto-scroll the viewport so the selected item is visible
        int cellTop = targetCell->bounds.getY();
        int cellBottom = targetCell->bounds.getBottom();
        int viewTop = gridViewport.getViewPositionY();
        int viewBottom = viewTop + gridViewport.getHeight();
        
        if (cellTop < viewTop) {
            gridViewport.setViewPosition(gridViewport.getViewPositionX(), cellTop - 20);
        } else if (cellBottom > viewBottom) {
            gridViewport.setViewPosition(gridViewport.getViewPositionX(), cellBottom - gridViewport.getHeight() + 20);
        }
    }
    
    return true;
}
