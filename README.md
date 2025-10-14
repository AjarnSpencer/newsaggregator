# newsaggregator
Global News Aggregator
A sophisticated cross-platform desktop application that aggregates news from sources around the world across multiple categories.

News Aggregator Screenshot

🌍 Overview
News Aggregator is a comprehensive desktop application built with Python that in its initial commit was designed to bring together breaking news and categorized content from over 30 major news sources across 6 continents and 10+ languages. The application provides a unified interface to access global news with enhanced deep-dive research on each article. The Aggregator has now been updated to a more sophisticated app with expanded sources

🚀 Features

📰 Multi-Source News Aggregation

### New additions

---

🌐 Expanded Sources: 30+ news sources from 6 continents and 10+ languages
Categorized Content: 8 distinct categories (breaking, sports, tech, politics, culture, entertainment, music, weather)
Improved UI: Category tabs, country/language metadata, color-coded category badges
Enhanced Scraping: Better error handling, user agent headers, increased article limits
Category-Specific Research: Different research templates for each category
Responsive Design: 4-column grid layout for better content presentation
Visual Improvements: Better styling, shadows, rounded corners, improved typography
Metadata Display: Shows source, country, and language for each article.

---

📂 Categorized Content
Breaking News: Latest global developments and breaking stories
Sports: Athletic events, competitions, and sports industry news
Technology: Tech innovations, product launches, and industry trends
Politics: Government affairs, policy changes, and political developments
Culture: Arts, architecture, and cultural movements
Entertainment: Movies, TV shows, celebrity news, and entertainment industry
Music: Musical releases, concerts, and industry news
Weather: Meteorological updates and climate news

🔍 Enhanced Content Experience
Deep-dive research on each article with AI-simulated analysis
Key facts highlighting, related articles suggestions
Data point visualization (impact, trend, region)
Category-specific content enhancement

🖥️ Cross-Platform Interface
Responsive PyQt5 GUI with modern card-based layout
4-column grid design for optimal content presentation
Category filtering and source metadata display
Color-coded category badges for quick identification
Thumbnail images for visual engagement
"Read Full Analysis" functionality for detailed content

📦 Native Packaging
Windows: .exe executable
macOS: .dmg disk image
Ubuntu: .deb Debian package
Fedora: .rpm Red Hat package
Universal Linux: .run installer script

🌐 News Sources
Breaking News
BBC (UK) - Global news coverage
Reuters (US) - International news agency
CNN (US) - World news reporting
Al Jazeera (Qatar) - Middle Eastern perspective
The Guardian (UK) - International news
Le Monde (France) - European news
Der Spiegel (Germany) - German perspective
Xinhua (China) - Asian news coverage
Kyodo News (Japan) - Japanese news
El Pais (Spain) - Spanish news
Yomiuri (Japan) - Japanese language news

Sports
ESPN (US) - Sports news and events
Sky Sports (UK) - European sports coverage
Marca (Spain) - Football and sports news
Technology
TechCrunch (US) - Startup and tech news
The Verge (US) - Technology reviews
Wired (US) - Tech culture and innovation
Politics

Politico (US) - Political news and analysis
The Hill (US) - US political coverage
Culture
Artnet (US) - Art world news
Architectural Digest (US) - Design and architecture
Entertainment
Variety (US) - Entertainment industry news
The Hollywood Reporter (US) - Film and TV industry
Music
Rolling Stone (US) - Music and culture
NME (UK) - Music news and reviews
Weather
Weather.com (US) - Meteorological news
AccuWeather (US) - Weather forecasting updates

🛠️ Technical Architecture
Core Technologies
Python 3.8+: Main programming language
PyQt5/PyQtWebEngine: GUI framework
BeautifulSoup4: Web scraping and parsing
Requests: HTTP handling
Threading: Non-blocking operations
LXML: Fast XML/HTML processing

Main Components
NewsScraper Class: Handles multi-source scraping with source-specific CSS selectors
DeepDiveResearcher Class: Simulates enhanced content generation with category-specific templates
NewsArticle Class: Manages article data, enhancement, and thumbnail generation
NewsApp GUI Class: PyQt5 QMainWindow with responsive card layout and category filtering

Key Features
Multi-threaded scraping to prevent UI blocking
Graceful HTTP error handling
Responsive 4-column card layout
Placeholder image generation with Picsum
Article caching with timestamps
Category-based content organization

📋 Requirements
Python 3.8 or higher
PyQt5 >= 5.15.0
PyQtWebEngine >= 5.15.0
Requests >= 2.25.0
BeautifulSoup4 >= 4.9.0
LXML >= 4.6.0

🚀 **Installation From Source**

```
# Clone the repository
git clone https://github.com/yourusername/news-aggregator.git
cd news-aggregator

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/news_app.py
```
From Pre-built Packages
Download the appropriate package for your platform:

Windows: .exe file from releases
macOS: .dmg file from releases
Ubuntu: .deb package from releases
Fedora: .rpm package from releases
Universal Linux: .run installer from releases

🏗️ Building from Source
Windows
```
cd build
build.bat
```

macOS
```
cd build
chmod +x build_mac.sh
./build_mac.sh
```

Linux
```
cd build
chmod +x build.sh
./build.sh
```

🤝 Contributing
We welcome contributions from the community! Here's how you can help:

Report Issues: Found a bug? Have a feature request? Open an issue!
Submit Pull Requests: Fix bugs, add features, improve documentation
Add News Sources: Contribute configurations for new news sources
Improve Scraping: Enhance CSS selectors for better content extraction
UI/UX Improvements: Make the interface more intuitive and visually appealing

## Development Setup
```

# Fork and clone the repository
git clone https://github.com/yourusername/news-aggregator.git
cd news-aggregator

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest tests/

# Make your changes and submit a pull request
```
- **License**;
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 **Acknowledgments**
Thanks to all news sources for providing public content
PyQt5 community for the excellent GUI framework
BeautifulSoup developers for web scraping tools
All contributors who help improve this project

📞 **Support**
For general questions, please use Discussions
For bug reports and feature requests, please use Issues
For security concerns, please contact the maintainers directly
Stay informed with the world's news in one powerful, cross-platform application! 🌍📰
