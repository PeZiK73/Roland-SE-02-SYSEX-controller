# 1. Clean up wrong paths
# Remove the bad file inside the bundle if it exists
if (Test-Path "C:\VST\ANTIGRAVITY_PLUGINS\SE-02 Controller.vst3\SE-02 Controller.vst3") {
    Remove-Item -Force "C:\VST\ANTIGRAVITY_PLUGINS\SE-02 Controller.vst3\SE-02 Controller.vst3"
}

# Remove the one in Program Files (requires admin)
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command "if (Test-Path 'C:\Program Files\Common Files\VST3\SE-02 Controller.vst3') { Remove-Item -Recurse -Force 'C:\Program Files\Common Files\VST3\SE-02 Controller.vst3' }"" -Verb RunAs -Wait

# 2. Deploy the correct bundle format to the correct location
$sourceBundle = "C:\TEMP\ANTIGRAVITIY_ROLANDS_SCRIPTS\SE02_Controller\build\SE02_Controller_artefacts\Release\VST3\SE-02 Controller.vst3"
$destDir = "C:\VST\ANTIGRAVITY_PLUGINS\"

# Copy the entire bundle directory
Copy-Item -Path $sourceBundle -Destination $destDir -Force -Recurse
