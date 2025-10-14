# place this file in location src/news_app.py
import sys
import os
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QStatusBar, QTabWidget, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
import threading
import time
import datetime
import random

# Enhanced global news sources with categories
SOURCE_CONFIGS = {
    # Breaking News
    'BBC': {
        'url': 'https://www.bbc.com/news',
        'selectors': {
            'title': 'h3[data-testid="card-headline"]',
            'url': 'a[data-testid="internal-link"]'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'UK'
    },
    'Reuters': {
        'url': 'https://www.reuters.com/world/',
        'selectors': {
            'title': 'a[data-testid="Heading"]',
            'url': 'a[data-testid="Heading"]'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'US'
    },
    'CNN': {
        'url': 'https://www.cnn.com/world',
        'selectors': {
            'title': 'span[data-editable="headline"]',
            'url': 'a'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'US'
    },
    'Al Jazeera': {
        'url': 'https://www.aljazeera.com/news/',
        'selectors': {
            'title': 'article h3 a',
            'url': 'article h3 a'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'Qatar'
    },
    'The Guardian': {
        'url': 'https://www.theguardian.com/international',
        'selectors': {
            'title': 'a[data-link-name="article"]',
            'url': 'a[data-link-name="article"]'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'UK'
    },
    'Le Monde': {
        'url': 'https://www.lemonde.fr/en/',
        'selectors': {
            'title': 'h2 > a',
            'url': 'h2 > a'
        },
        'category': 'breaking',
        'language': 'fr',
        'country': 'France'
    },
    'Der Spiegel': {
        'url': 'https://www.spiegel.de/international/',
        'selectors': {
            'title': 'a.text-black[data-orbis-link]',
            'url': 'a.text-black[data-orbis-link]'
        },
        'category': 'breaking',
        'language': 'de',
        'country': 'Germany'
    },
    'Xinhua': {
        'url': 'http://www.news.cn/english/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'China'
    },
    'Kyodo News': {
        'url': 'https://english.kyodonews.net/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'Japan'
    },
    'El Pais': {
        'url': 'https://english.elpais.com/',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'breaking',
        'language': 'en',
        'country': 'Spain'
    },
    'Yomiuri': {
        'url': 'https://www.yomiuri.co.jp/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'breaking',
        'language': 'ja',
        'country': 'Japan'
    },
    
    # Sports
    'ESPN': {
        'url': 'https://www.espn.com/',
        'selectors': {
            'title': 'h1 > a',
            'url': 'h1 > a'
        },
        'category': 'sports',
        'language': 'en',
        'country': 'US'
    },
    'Sky Sports': {
        'url': 'https://www.skysports.com/',
        'selectors': {
            'title': 'a.news-list__headline-link',
            'url': 'a.news-list__headline-link'
        },
        'category': 'sports',
        'language': 'en',
        'country': 'UK'
    },
    'Marca': {
        'url': 'https://www.marca.com/en/',
        'selectors': {
            'title': 'h2 > a',
            'url': 'h2 > a'
        },
        'category': 'sports',
        'language': 'en',
        'country': 'Spain'
    },
    
    # Technology
    'TechCrunch': {
        'url': 'https://techcrunch.com/',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'technology',
        'language': 'en',
        'country': 'US'
    },
    'The Verge': {
        'url': 'https://www.theverge.com/',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'technology',
        'language': 'en',
        'country': 'US'
    },
    'Wired': {
        'url': 'https://www.wired.com/',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'technology',
        'language': 'en',
        'country': 'US'
    },
    
    # Politics
    'Politico': {
        'url': 'https://www.politico.com/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'politics',
        'language': 'en',
        'country': 'US'
    },
    'The Hill': {
        'url': 'https://thehill.com/',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'politics',
        'language': 'en',
        'country': 'US'
    },
    
    # Culture
    'Artnet': {
        'url': 'https://www.artnet.com/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'culture',
        'language': 'en',
        'country': 'US'
    },
    'Architectural Digest': {
        'url': 'https://www.architecturaldigest.com/',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'culture',
        'language': 'en',
        'country': 'US'
    },
    
    # Entertainment
    'Variety': {
        'url': 'https://variety.com/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'entertainment',
        'language': 'en',
        'country': 'US'
    },
    'The Hollywood Reporter': {
        'url': 'https://www.hollywoodreporter.com/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'entertainment',
        'language': 'en',
        'country': 'US'
    },
    
    # Music
    'Rolling Stone': {
        'url': 'https://www.rollingstone.com/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'music',
        'language': 'en',
        'country': 'US'
    },
    'NME': {
        'url': 'https://www.nme.com/',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'music',
        'language': 'en',
        'country': 'UK'
    },
    
    # Weather
    'Weather.com': {
        'url': 'https://weather.com/news',
        'selectors': {
            'title': 'h3 a',
            'url': 'h3 a'
        },
        'category': 'weather',
        'language': 'en',
        'country': 'US'
    },
    'AccuWeather': {
        'url': 'https://www.accuweather.com/en/weather-news',
        'selectors': {
            'title': 'h2 a',
            'url': 'h2 a'
        },
        'category': 'weather',
        'language': 'en',
        'country': 'US'
    }
}

CATEGORIES = {
    'all': 'All News',
    'breaking': 'Breaking News',
    'sports': 'Sports',
    'technology': 'Technology',
    'politics': 'Politics',
    'culture': 'Culture',
    'entertainment': 'Entertainment',
    'music': 'Music',
    'weather': 'Weather'
}

class NewsScraper:
    def __init__(self):
        self.sources = SOURCE_CONFIGS

    def scrape_headlines(self, category='all'):
        articles = []
        for source_name, config in self.sources.items():
            # Filter by category if not 'all'
            if category != 'all' and config['category'] != category:
                continue
                
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(config['url'], timeout=15, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Find all title elements
                title_elements = soup.select(config['selectors']['title'])
                
                for elem in title_elements[:8]:  # Increased to 8 articles per source
                    title = elem.get_text(strip=True)
                    url = elem.get('href')
                    
                    # Handle relative URLs
                    if url and url.startswith('/'):
                        if source_name in ['BBC', 'The Guardian']:
                            url = 'https://www.bbc.com' + url if source_name == 'BBC' else 'https://www.theguardian.com' + url
                        elif source_name in ['Reuters', 'CNN', 'Al Jazeera']:
                            base_url = {
                                'Reuters': 'https://www.reuters.com',
                                'CNN': 'https://www.cnn.com',
                                'Al Jazeera': 'https://www.aljazeera.com'
                            }
                            url = base_url[source_name] + url
                        elif source_name == 'Le Monde':
                            url = 'https://www.lemonde.fr' + url
                        elif source_name == 'Der Spiegel':
                            url = 'https://www.spiegel.de' + url
                        elif source_name == 'Xinhua':
                            url = 'http://www.news.cn' + url
                        elif source_name == 'Kyodo News':
                            url = 'https://english.kyodonews.net' + url
                        elif source_name == 'El Pais':
                            url = 'https://english.elpais.com' + url
                        elif source_name == 'Yomiuri':
                            url = 'https://www.yomiuri.co.jp' + url
                    
                    if title and url and len(title) > 15:  # Filter out very short titles
                        articles.append({
                            'title': title,
                            'url': url,
                            'source': source_name,
                            'category': config['category'],
                            'language': config['language'],
                            'country': config['country']
                        })
            except Exception as e:
                print(f"Error scraping {source_name}: {str(e)}")
                continue
        return articles

class DeepDiveResearcher:
    def research_topic(self, query, category):
        # Enhanced research with category-specific content
        category_summaries = {
            'breaking': [
                f"Major developments in '{query}' are reshaping global perspectives.",
                f"New information about '{query}' reveals unexpected international implications.",
                f"Experts analyze the impact of '{query}' on worldwide political dynamics."
            ],
            'sports': [
                f"Latest updates on '{query}' showcase exceptional athletic achievements.",
                f"'{query}' competition results have significant implications for rankings.",
                f"Behind the scenes analysis of '{query}' reveals strategic insights."
            ],
            'technology': [
                f"Breakthrough innovations in '{query}' are transforming industry standards.",
                f"New developments in '{query}' technology promise to revolutionize user experience.",
                f"Technical analysis of '{query}' reveals performance optimization opportunities."
            ],
            'politics': [
                f"Political developments in '{query}' have far-reaching policy implications.",
                f"Government response to '{query}' reflects changing political dynamics.",
                f"Policy analysis of '{query}' reveals complex stakeholder interests."
            ],
            'culture': [
                f"Cultural significance of '{query}' resonates across global communities.",
                f"Artistic interpretation of '{query}' sparks international dialogue.",
                f"Cultural impact assessment of '{query}' reveals diverse perspectives."
            ],
            'entertainment': [
                f"Entertainment industry buzz around '{query}' generates significant media attention.",
                f"'{query}' receives critical acclaim from international reviewers.",
                f"Behind-the-scenes look at '{query}' reveals creative process insights."
            ],
            'music': [
                f"Musical innovation in '{query}' influences contemporary soundscapes.",
                f"'{query}' performance receives standing ovations from global audiences.",
                f"Musical analysis of '{query}' reveals technical and artistic excellence."
            ],
            'weather': [
                f"Weather patterns in '{query}' region show unusual meteorological activity.",
                f"Climate analysis of '{query}' reveals seasonal variation trends.",
                f"Meteorological data for '{query}' indicates potential weather impacts."
            ]
        }
        
        return {
            'summary': random.choice(category_summaries.get(category, category_summaries['breaking'])),
            'related_articles': [
                {'title': f'Related: {query} - Background', 'url': 'https://example.com/related1'},
                {'title': f'Analysis: {query} Impact', 'url': 'https://example.com/related2'}
            ],
            'key_facts': [
                f'Fact 1: {query} has global significance',
                f'Fact 2: Key stakeholders are monitoring developments',
                f'Fact 3: Timeline shows recent acceleration'
            ],
            'data_points': [
                {'label': 'Impact', 'value': random.choice(['High', 'Medium', 'Low'])},
                {'label': 'Trend', 'value': random.choice(['Increasing', 'Stable', 'Decreasing'])},
                {'label': 'Region', 'value': random.choice(['Global', 'Regional', 'Local'])}
            ]
        }

class NewsArticle:
    def __init__(self, title, url, source, category, language, country):
        self.title = title
        self.url = url
        self.source = source
        self.category = category
        self.language = language
        self.country = country
        self.thumbnail = None
        self.description = None
        self.enhanced_content = None
        self.timestamp = datetime.datetime.now()

    def enhance_article(self):
        researcher = DeepDiveResearcher()
        self.enhanced_content = researcher.research_topic(self.title, self.category)
        self.description = self.enhanced_content['summary']
        # Generate placeholder thumbnail with category-specific seed
        seed = hash(self.title + self.category) % 10000
        self.thumbnail = f"https://picsum.photos/seed/{seed}/300/200"

class NewsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.articles = []
        self.current_category = 'all'
        self.init_ui()
        self.load_news()

    def init_ui(self):
        self.setWindowTitle("Global News Aggregator")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("GLOBAL NEWS AGGREGATOR")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            padding: 20px;
            color: #2c3e50;
        """)
        header_layout.addWidget(header)
        main_layout.addLayout(header_layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Category selector
        self.category_combo = QComboBox()
        for key, value in CATEGORIES.items():
            self.category_combo.addItem(value, key)
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        controls_layout.addWidget(QLabel("Category:"))
        controls_layout.addWidget(self.category_combo)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh News")
        refresh_btn.clicked.connect(self.load_news)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(refresh_btn)
        
        # Country filter
        self.country_combo = QComboBox()
        self.country_combo.addItem("All Countries", "all")
        controls_layout.addWidget(QLabel("Country:"))
        controls_layout.addWidget(self.country_combo)
        
        main_layout.addLayout(controls_layout)
        
        # Tab widget for categories
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Scroll area for articles grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.articles_widget = QWidget()
        self.articles_layout = QGridLayout(self.articles_widget)
        self.scroll_area.setWidget(self.articles_widget)
        main_layout.addWidget(self.scroll_area)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Loading news...")

    def on_category_changed(self, index):
        self.current_category = self.category_combo.currentData()
        self.load_news()

    def load_news(self):
        self.status_bar.showMessage("Fetching news...")
        self.articles = []
        
        # Use threading to prevent UI blocking
        thread = threading.Thread(target=self._fetch_news)
        thread.start()

    def _fetch_news(self):
        scraper = NewsScraper()
        raw_articles = scraper.scrape_headlines(self.current_category)
        
        # Convert to NewsArticle objects and enhance
        for data in raw_articles:
            article = NewsArticle(
                data['title'], 
                data['url'], 
                data['source'],
                data['category'],
                data['language'],
                data['country']
            )
            article.enhance_article()
            self.articles.append(article)
        
        # Update UI in main thread
        QApplication.instance().postEvent(self, None)  # Wake up event loop
        self.populate_grid()

    def populate_grid(self):
        # Clear existing articles
        for i in reversed(range(self.articles_layout.count())):
            widget = self.articles_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Add articles to grid
        for i, article in enumerate(self.articles):
            row = i // 4  # Increased to 4 columns
            col = i % 4
            
            # Create article card
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card.setStyleSheet("""
                QWidget {
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 15px;
                    background-color: #ffffff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
            """)
            
            # Category badge
            category_badge = QLabel(article.category.upper())
            category_badge.setStyleSheet(f"""
                background-color: {
                    '#e74c3c' if article.category == 'breaking' else
                    '#3498db' if article.category == 'sports' else
                    '#9b59b6' if article.category == 'technology' else
                    '#f39c12' if article.category == 'politics' else
                    '#1abc9c' if article.category == 'culture' else
                    '#34495e' if article.category == 'entertainment' else
                    '#2ecc71' if article.category == 'music' else
                    '#95a5a6'
                };
                color: white;
                padding: 3px 8px;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
                margin-bottom: 8px;
            """)
            card_layout.addWidget(category_badge)
            
            # Thumbnail
            thumbnail = QLabel()
            try:
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(article.thumbnail).content)
                thumbnail.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except:
                thumbnail.setText("Image Unavailable")
                thumbnail.setAlignment(Qt.AlignCenter)
                thumbnail.setStyleSheet("background-color: #f0f0f0; height: 200px;")
            card_layout.addWidget(thumbnail)
            
            # Title
            title = QLabel(article.title)
            title.setWordWrap(True)
            title.setStyleSheet("""
                font-weight: bold; 
                font-size: 16px;
                margin-top: 10px;
                color: #2c3e50;
            """)
            card_layout.addWidget(title)
            
            # Source and metadata
            metadata = QLabel(f"{article.source} • {article.country} • {article.language.upper()}")
            metadata.setStyleSheet("color: #7f8c8d; font-size: 12px;")
            card_layout.addWidget(metadata)
            
            # Description
            description = QLabel(article.description)
            description.setWordWrap(True)
            description.setStyleSheet("""
                margin: 10px 0;
                color: #34495e;
                font-size: 13px;
            """)
            card_layout.addWidget(description)
            
            # Read Full Analysis button
            read_btn = QPushButton("Read Full Analysis")
            read_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1a252f;
                }
            """)
            read_btn.clicked.connect(lambda checked, a=article: self.show_analysis(a))
            card_layout.addWidget(read_btn)
            
            self.articles_layout.addWidget(card, row, col)
        
        self.status_bar.showMessage(f"Loaded {len(self.articles)} articles in {self.current_category} category")

    def show_analysis(self, article):
        # In a real app, this would open a detailed view
        print(f"Showing analysis for: {article.title}")
        print(f"Category: {article.category}")
        print(f"Source: {article.source}")
        print(f"Summary: {article.enhanced_content['summary']}")
        print("Key Facts:")
        for fact in article.enhanced_content['key_facts']:
            print(f"  - {fact}")

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
        QComboBox {
            padding: 5px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
        }
        QComboBox:hover {
            border: 1px solid #3498db;
        }
    """)
    window = NewsApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
