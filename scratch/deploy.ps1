$sourceBundle = "C:\TEMP\ANTIGRAVITIY_ROLANDS_SCRIPTS\SE02_Controller\build\SE02_Controller_artefacts\Release\VST3\SE-02 Controller.vst3"
$destDir = "C:\VST\ANTIGRAVITY_PLUGINS\"
if (Test-Path "$destDir\SE-02 Controller.vst3") {
    Remove-Item "$destDir\SE-02 Controller.vst3" -Force -Recurse
}
Copy-Item -Path $sourceBundle -Destination $destDir -Force -Recurse
