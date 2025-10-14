@echo off
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --onefile --windowed --icon=assets/icon.ico src/news_app.py
ren dist\news_app.exe GlobalNewsAggregator.exe
echo Build complete. Executable located in dist/GlobalNewsAggregator.exe
