import sys

with open('Source/PresetBrowser.cpp', 'r') as f:
    content = f.read()

old_code = """
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
"""

new_code = """
            // Determine text color based on state
            juce::Colour textCol;
            if (cell.isCurrentlyFetching) textCol = juce::Colour(0xffffff00);
            else if (isSelected) textCol = juce::Colours::white;
            else if (cell.isFetched) textCol = juce::Colour(0xffeeeeee);
            else textCol = juce::Colour(0xff666666);

            // Draw index/number
            juce::Rectangle<int> textRect = cellRect.toNearestInt();
            juce::String indexStr = juce::String(globalIndex + 1);
            g.setColour(textCol.withMultipliedAlpha(0.5f));
            g.setFont(juce::Font(10.0f));
            g.drawText(indexStr, textRect.withWidth(25).withX(textRect.getX() + 5), juce::Justification::centredLeft);
            
            // Draw patch name
            g.setColour(textCol);
            g.setFont(isSelected ? juce::Font(13.0f, juce::Font::bold) : juce::Font(13.0f, juce::Font::plain));
            g.drawText(cell.text, textRect.withTrimmedLeft(28).withTrimmedRight(5), juce::Justification::centredLeft);
"""

content = content.replace(old_code, new_code)

with open('Source/PresetBrowser.cpp', 'w') as f:
    f.write(content)
