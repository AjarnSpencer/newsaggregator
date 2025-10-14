#!/bin/bash
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --onefile --windowed --icon=assets/icon.icns src/news_app.py

# Create app bundle structure
mkdir -p dist/GlobalNewsAggregator.app/Contents/MacOS
mkdir -p dist/GlobalNewsAggregator.app/Contents/Resources

# Copy executable
cp dist/news_app dist/GlobalNewsAggregator.app/Contents/MacOS/GlobalNewsAggregator

# Create Info.plist
cat > dist/GlobalNewsAggregator.app/Contents/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>GlobalNewsAggregator</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.globalnewsaggregator.app</string>
    <key>CFBundleName</key>
    <string>Global News Aggregator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>
EOF

# Copy icon
cp assets/icon.icns dist/GlobalNewsAggregator.app/Contents/Resources/

# Create DMG
create-dmg \
  --volname "Global News Aggregator" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "GlobalNewsAggregator.app" 200 190 \
  --hide-extension "GlobalNewsAggregator.app" \
  --app-drop-link 600 185 \
  "dist/GlobalNewsAggregator.dmg" \
  "dist/GlobalNewsAggregator.app"

echo "Build complete. DMG located at dist/GlobalNewsAggregator.dmg"
