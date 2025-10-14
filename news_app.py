import sys
import os
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout,
    QLabel, QPushButton, QScrollArea, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import threading
import time
import datetime

# News source configurations
SOURCE_CONFIGS = {
    'BBC': {
        'url': 'https://www.bbc.com/news',
        'selectors': {
            'title': 'h3[data-testid="card-headline"]',
            'url': 'a[data-testid="internal-link"]'
        }
    },
    'Reuters': {
        'url': 'https://www.reuters.com/world/',
        'selectors': {
            'title': 'a[data-testid="Heading"]',
            'url': 'a[data-testid="Heading"]'
        }
    },
    'CNN': {
        'url': 'https://www.cnn.com/world',
        'selectors': {
            'title': 'span[data-editable="headline"]',
            'url': 'a'
        }
    },
    'Al Jazeera': {
        'url': 'https://www.aljazeera.com/news/',
        'selectors': {
            'title': 'article h3 a',
            'url': 'article h3 a'
        }
    },
    'The Guardian': {
        'url': 'https://www.theguardian.com/international',
        'selectors': {
            'title': 'a[data-link-name="article"]',
            'url': 'a[data-link-name="article"]'
        }
    }
}

class NewsScraper:
    def __init__(self):
        self.sources = SOURCE_CONFIGS

    def scrape_headlines(self):
        articles = []
        for source_name, config in self.sources.items():
            try:
                response = requests.get(config['url'], timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Find all title elements
                title_elements = soup.select(config['selectors']['title'])
                
                for elem in title_elements[:5]:  # Limit to 5 articles per source
                    title = elem.get_text(strip=True)
                    url = elem.get('href')
                    
                    # Handle relative URLs
                    if url and url.startswith('/'):
                        if source_name == 'BBC':
                            url = 'https://www.bbc.com' + url
                        elif source_name == 'Reuters':
                            url = 'https://www.reuters.com' + url
                        elif source_name == 'CNN':
                            url = 'https://www.cnn.com' + url
                        elif source_name == 'Al Jazeera':
                            url = 'https://www.aljazeera.com' + url
                        elif source_name == 'The Guardian':
                            url = 'https://www.theguardian.com' + url
                    
                    if title and url:
                        articles.append({
                            'title': title,
                            'url': url,
                            'source': source_name
                        })
            except Exception as e:
                print(f"Error scraping {source_name}: {str(e)}")
                continue
        return articles

class DeepDiveResearcher:
    def research_topic(self, query):
        # Simulate research with placeholder data
        return {
            'summary': f"Comprehensive analysis of '{query}' showing significant developments in global affairs.",
            'related_articles': [
                {'title': 'Related Article 1', 'url': 'https://example.com/related1'},
                {'title': 'Related Article 2', 'url': 'https://example.com/related2'}
            ],
            'key_facts': [
                'Fact 1: Important development in the story',
                'Fact 2: Key stakeholders involved',
                'Fact 3: Timeline of events'
            ],
            'data_points': [
                {'label': 'Impact', 'value': 'High'},
                {'label': 'Trend', 'value': 'Increasing'},
                {'label': 'Region', 'value': 'Global'}
            ]
        }

class NewsArticle:
    def __init__(self, title, url, source):
        self.title = title
        self.url = url
        self.source = source
        self.thumbnail = None
        self.description = None
        self.enhanced_content = None
        self.timestamp = datetime.datetime.now()

    def enhance_article(self):
        researcher = DeepDiveResearcher()
        self.enhanced_content = researcher.research_topic(self.title)
        self.description = self.enhanced_content['summary']
        # Generate placeholder thumbnail
        self.thumbnail = f"https://picsum.photos/seed/{hash(self.title)%10000}/300/200"

class NewsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.articles = []
        self.init_ui()
        self.load_news()

    def init_ui(self):
        self.setWindowTitle("Global News Aggregator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("BREAKING NEWS WORLDWIDE")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        main_layout.addWidget(header)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh News")
        refresh_btn.clicked.connect(self.load_news)
        main_layout.addWidget(refresh_btn)
        
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

    def load_news(self):
        self.status_bar.showMessage("Fetching news...")
        self.articles = []
        
        # Use threading to prevent UI blocking
        thread = threading.Thread(target=self._fetch_news)
        thread.start()

    def _fetch_news(self):
        scraper = NewsScraper()
        raw_articles = scraper.scrape_headlines()
        
        # Convert to NewsArticle objects and enhance
        for data in raw_articles:
            article = NewsArticle(data['title'], data['url'], data['source'])
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
            row = i // 3
            col = i % 3
            
            # Create article card
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card.setStyleSheet("""
                QWidget {
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #f9f9f9;
                }
            """)
            
            # Thumbnail
            thumbnail = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(article.thumbnail).content)
            thumbnail.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio))
            card_layout.addWidget(thumbnail)
            
            # Title
            title = QLabel(article.title)
            title.setWordWrap(True)
            title.setStyleSheet("font-weight: bold; font-size: 16px;")
            card_layout.addWidget(title)
            
            # Source
            source = QLabel(f"Source: {article.source}")
            source.setStyleSheet("color: #666;")
            card_layout.addWidget(source)
            
            # Description
            description = QLabel(article.description)
            description.setWordWrap(True)
            description.setStyleSheet("margin-bottom: 10px;")
            card_layout.addWidget(description)
            
            # Read Full Analysis button
            read_btn = QPushButton("Read Full Analysis")
            read_btn.clicked.connect(lambda checked, a=article: self.show_analysis(a))
            card_layout.addWidget(read_btn)
            
            self.articles_layout.addWidget(card, row, col)
        
        self.status_bar.showMessage(f"Loaded {len(self.articles)} articles")

    def show_analysis(self, article):
        # In a real app, this would open a detailed view
        print(f"Showing analysis for: {article.title}")
        print(f"Summary: {article.enhanced_content['summary']}")
        print("Key Facts:")
        for fact in article.enhanced_content['key_facts']:
            print(f"  - {fact}")

def main():
    app = QApplication(sys.argv)
    window = NewsApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
