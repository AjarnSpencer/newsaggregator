#!/bin/bash
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --onefile --windowed src/news_app.py

# Create DEB package structure
mkdir -p dist/deb/global-news-aggregator/usr/bin
mkdir -p dist/deb/global-news-aggregator/usr/share/applications
mkdir -p dist/deb/global-news-aggregator/DEBIAN

# Copy executable
cp dist/news_app dist/deb/global-news-aggregator/usr/bin/global-news-aggregator

# Create desktop entry
cat > dist/deb/global-news-aggregator/usr/share/applications/global-news-aggregator.desktop << EOF
[Desktop Entry]
Name=Global News Aggregator
Exec=/usr/bin/global-news-aggregator
Icon=global-news-aggregator
Type=Application
Categories=Network;News;
EOF

# Create control file
cat > dist/deb/global-news-aggregator/DEBIAN/control << EOF
Package: global-news-aggregator
Version: 1.0
Section: base
Priority: optional
Architecture: amd64
Depends: python3
Maintainer: Your Name <your.email@example.com>
Description: Global News Aggregator
 A cross-platform application that scrapes breaking news from top global sources across multiple categories
EOF

# Build DEB package
dpkg-deb --build dist/deb/global-news-aggregator

# Create RPM package structure
mkdir -p dist/rpm/global-news-aggregator/usr/bin
mkdir -p dist/rpm/global-news-aggregator/usr/share/applications

# Copy executable
cp dist/news_app dist/rpm/global-news-aggregator/usr/bin/global-news-aggregator

# Create desktop entry
cat > dist/rpm/global-news-aggregator/usr/share/applications/global-news-aggregator.desktop << EOF
[Desktop Entry]
Name=Global News Aggregator
Exec=/usr/bin/global-news-aggregator
Icon=global-news-aggregator
Type=Application
Categories=Network;News;
EOF

# Create spec file
cat > dist/rpm/global-news-aggregator.spec << EOF
Name: global-news-aggregator
Version: 1.0
Release: 1
Summary: Global News Aggregator

License: MIT
BuildArch: x86_64

%description
A cross-platform application that scrapes breaking news from top global sources across multiple categories

%files
/usr/bin/global-news-aggregator
/usr/share/applications/global-news-aggregator.desktop

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
cp dist/rpm/global-news-aggregator/usr/bin/global-news-aggregator %{buildroot}/usr/bin/
cp dist/rpm/global-news-aggregator/usr/share/applications/global-news-aggregator.desktop %{buildroot}/usr/share/applications/

%changelog
* $(date +"%a %b %d %Y") Your Name <your.email@example.com> - 1.0-1
- Initial build
EOF

# Build RPM package
rpmbuild -bb dist/rpm/global-news-aggregator.spec

echo "Build complete. Packages located in dist/"
