import sys
with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

import re
content = re.sub(r'enum class FetchState.*?FetchState fetchState = FetchState::Idle;', 
    'int fetchPhase = 0;\n    bool isFetching = false;', 
    content, flags=re.DOTALL)

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)
