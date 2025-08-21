# Rotten Tomatoes Reviews Scraper

A comprehensive Python web scraper that collects movie reviews from Rotten Tomatoes using Selenium WebDriver. I built this tool to gather large datasets of critic reviews for sentiment analysis and movie review research projects. Currently targeting 1100+ reviews across multiple high-profile movies.

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Movies Currently Tracked](#movies-currently-tracked)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Output Format](#output-format)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Architecture & Design](#architecture--design)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [Legal Notice](#legal-notice)

## Features

### Core Functionality
- **Automated Review Collection**: Scrapes critic reviews, ratings, and metadata from Rotten Tomatoes
- **Dynamic Content Loading**: Automatically clicks "Load More" buttons to fetch all available reviews
- **Smart Element Detection**: Uses multiple CSS selectors and XPath expressions to handle RT's changing layouts
- **Cookie Consent Handling**: Automatically accepts cookie policies and privacy notices
- **Robust Error Handling**: Continues processing even if individual pages fail
- **Data Export**: Outputs clean CSV files for easy analysis

### Advanced Features
- **Browser Stealth Mode**: Uses realistic user agents and disables automation detection
- **Intelligent Waiting**: WebDriverWait ensures elements load before interaction
- **Debug Mode**: Saves page source HTML when scraping fails for troubleshooting
- **Progress Tracking**: Real-time console output shows scraping progress
- **Rate Limiting**: Built-in delays to be respectful to RT's servers
- **Comprehensive Logging**: Detailed console output for monitoring and debugging

## How It Works

The scraper follows this workflow for each movie:

1. **Page Loading**: Navigates to the movie's reviews page with custom headers
2. **Cookie Handling**: Automatically detects and accepts various cookie consent forms
3. **Review Loading**: Continuously clicks "Load More" buttons until all reviews are visible
4. **Data Extraction**: Parses each review card to extract:
   - Critic name and publication
   - Review date and numerical score
   - Fresh/Rotten classification
   - Review text/quotes
5. **Data Validation**: Filters out empty or malformed review data
6. **CSV Export**: Saves both individual movie files and a combined dataset

## Movies Currently Tracked

The scraper is configured to collect reviews from these movies:

| Movie | Release Year | Rotten Tomatoes URL |
|-------|--------------|-------------------|
| **Sinners** | 2025 | `/m/sinners_2025/reviews` |
| **The Life of Chuck** | - | `/m/the_life_of_chuck/reviews` |
| **Superman** | 2025 | `/m/superman_2025/reviews` |
| **Jurassic World: Rebirth** | - | `/m/jurassic_world_rebirth/reviews` |
| **Weapons** | - | `/m/weapons/reviews` |
| **Avatar: The Way of Water** | 2022 | `/m/avatar_the_way_of_water/reviews` |

Adding new movies is straightforward - just update the `movie_urls` dictionary in the script with the movie key and RT URL.

## Installation & Setup

### Prerequisites
- **Python 3.7+** (tested on 3.8-3.11)
- **Google Chrome browser** (latest stable version recommended)
- **ChromeDriver** (auto-detected or manual installation)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/rotten-tomatoes-scraper.git
cd rotten-tomatoes-scraper
```

### Step 2: Install Dependencies
```bash
pip install selenium
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 3: ChromeDriver Setup

**Option A: Automatic Detection (Recommended)**
The script will try to find ChromeDriver automatically if it's in your PATH.

**Option B: Manual Installation**
1. Download ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
2. Extract to a folder (e.g., `C:\chromedriver\` on Windows)
3. Update the path in the script or add to your system PATH

**Option C: Using WebDriver Manager (Alternative)**
```bash
pip install webdriver-manager
```
Then modify the script to use WebDriverManager for automatic ChromeDriver management.

## Usage

### Basic Usage
Run the scraper with default settings:
```bash
python scraper.py
```

### What Happens During Execution
1. **Browser Launch**: Chrome opens in automated mode
2. **Movie Processing**: Each movie is processed sequentially
3. **Progress Updates**: Console shows real-time progress:
   ```
   🎬 Processing: sinners_2025
   📄 URL: https://www.rottentomatoes.com/m/sinners_2025/reviews
   ✅ Page loaded
   🍪 Checking for cookie consent...
   📚 Loading all reviews...
   📊 Loaded more reviews (attempt 1)
   📊 Loaded more reviews (attempt 2)
   🎯 Found 45 review cards using selector: review-speech-balloon
   ✍️ Parsed review 1: John Smith from The Movie Times
   ```
4. **Data Export**: CSV files are created in the project directory
5. **Summary**: Final statistics and file locations are displayed

### Expected Runtime
- **Per movie**: 30-60 seconds depending on review count
- **Full run**: 5-10 minutes for all 6 movies
- **Large datasets**: Up to 15 minutes for movies with 200+ reviews

## Output Format

### Individual Movie Files
Each movie generates a separate CSV file: `{movie_key}_reviews.csv`

### Combined Dataset
All reviews are merged into: `all_reviews_{timestamp}.csv`

### CSV Structure
| Column | Description | Example |
|--------|-------------|---------|
| `movie_key` | Internal movie identifier | `sinners_2025` |
| `movie_url` | Full Rotten Tomatoes URL | `https://www.rottentomatoes.com/m/sinners_2025/reviews` |
| `critic` | Critic/reviewer name | `Peter Travers` |
| `outlet` | Publication/media outlet | `Rolling Stone` |
| `date` | Review publication date | `January 15, 2025` |
| `score` | Numerical score if available | `3.5/4` or `7/10` |
| `freshness` | Fresh or Rotten classification | `fresh`, `rotten`, or empty |
| `quote` | Review excerpt/quote | `"A masterful blend of action and emotion..."` |

### Sample CSV Output
```csv
movie_key,movie_url,critic,outlet,date,score,freshness,quote
sinners_2025,https://www.rottentomatoes.com/m/sinners_2025/reviews,Peter Travers,Rolling Stone,Jan 15 2025,3.5/4,fresh,"A masterful blend of action and emotion that delivers on every level."
sinners_2025,https://www.rottentomatoes.com/m/sinners_2025/reviews,Owen Gleiberman,Variety,Jan 14 2025,,rotten,"Despite strong performances the film never quite finds its footing."
```

## Configuration

### Customizing the Movie List
Edit the `movie_urls` dictionary in the script:

```python
movie_urls = {
    "your_movie_key": "https://www.rottentomatoes.com/m/your_movie/reviews",
    "another_movie": "https://www.rottentomatoes.com/m/another_movie/reviews",
}
```

### Adjusting Scraping Behavior
Key parameters you can modify:

```python
# Maximum "Load More" clicks per movie
max_attempts = 20  

# Delay between page loads (seconds)
time.sleep(5)

# WebDriver timeout (seconds)  
WebDriverWait(driver, 15)

# Review card timeout
timeout=3
```

### Browser Options
The script includes stealth options to avoid detection:
- Custom user agent strings
- Disabled automation flags
- Realistic window sizing
- No sandbox mode for server environments

## Troubleshooting

### Common Issues and Solutions

**ChromeDriver Not Found**
```
Error: ChromeDriver setup failed
```
**Solution**: Download ChromeDriver and update the path in `setup_driver()` function, or add it to your system PATH.

**No Reviews Found**
```
⚠️ No review cards found with any selector
```
**Solution**: RT may have changed their HTML structure. Check the debug HTML file that gets saved automatically, or update the CSS selectors in `parse_review_card()`.

**Timeout Errors**
```
TimeoutException: Page load timeout
```
**Solutions**:
- Check your internet connection
- Increase timeout values in the script
- Some movies might have restricted access

**Cookie Consent Issues**
```
Could not click cookie consent button
```
**Solution**: The script tries multiple cookie consent patterns, but RT occasionally changes theirs. Add new selectors to the `accept_cookies_if_needed()` function.

### Debug Mode
When reviews aren't found, the script automatically:
1. Saves the page HTML to `debug_{movie_key}.html`
2. Prints page analysis to console
3. Shows which selectors were tried

Inspect these files to understand what's happening on the page.

### Verbose Logging
For more detailed debugging, you can add:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Architecture & Design

### File Structure
```
scraper.py              # Main scraping script
├── setup_driver()      # Chrome/ChromeDriver configuration
├── accept_cookies_if_needed()  # Cookie consent handling
├── load_all_reviews()  # Dynamic content loading
├── parse_review_card() # Data extraction logic
├── write_csv()         # File output handling
└── debug_page_content() # Troubleshooting utilities
```

### Key Design Decisions

**Multiple Selector Strategy**: Instead of relying on single CSS selectors, the script tries multiple patterns to handle RT's frequent layout changes.

**Graceful Degradation**: If one movie fails, the script continues with others rather than crashing entirely.

**Memory Efficient**: Processes one movie at a time rather than loading everything into memory.

**Extensible**: Easy to add new movies, modify selectors, or change output formats.

### Error Handling Philosophy
The scraper uses a "fail gracefully" approach:
- Individual review parsing errors don't stop the movie
- Movie-level errors don't stop the entire run  
- Detailed error reporting helps with debugging
- Automatic retry logic for transient failures

## Known Issues

### Rotten Tomatoes Rate Limiting
RT may temporarily block requests if too many are made quickly. The script includes delays, but you may need to increase them for very large datasets.

### Dynamic Content Changes
RT occasionally updates their review page layout. When this happens:
1. Check the debug HTML output
2. Update CSS selectors in `parse_review_card()`
3. Test with a single movie first

### Browser Compatibility
Currently only supports Chrome/Chromium. Firefox support could be added by modifying the `setup_driver()` function.

### Review Completeness
Some reviews may not have all fields (date, score, etc.). The script handles missing data gracefully but your analysis may need to account for this.

## Contributing

Contributions are welcome! Areas where help is particularly appreciated:

- **New Movie URLs**: Add more movies to track
- **Selector Updates**: When RT changes their layout
- **Browser Support**: Firefox, Safari, Edge compatibility  
- **Performance**: Parallel processing, async requests
- **Data Quality**: Better parsing logic, validation rules
- **Documentation**: Usage examples, tutorials

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Test thoroughly with multiple movies
4. Submit a pull request with clear description

### Reporting Issues
When reporting bugs, please include:
- Python version and OS
- Full error traceback
- Movie URLs that failed
- Debug HTML files if available

## Legal Notice

**Important**: This tool is designed for educational and research purposes only. 

### Terms of Use
- Respect Rotten Tomatoes' robots.txt and terms of service
- Don't overload their servers - the built-in delays are intentional
- Use collected data responsibly and ethically
- Consider reaching out to RT for permission if doing commercial research

### Rate Limiting
The script includes polite delays and rate limiting. Please don't modify these to be more aggressive without good reason.

### Data Usage
The data you collect belongs to the original critics and publications. If publishing research or analysis:
- Cite sources appropriately  
- Consider fair use guidelines
- Respect copyright and attribution requirements

### Disclaimer  
I'm not responsible for how this tool is used. Web scraping exists in a legal gray area - make sure you understand the implications for your specific use case.

---

**Happy scraping!** 🎬🍅

If you find this useful, consider starring the repo or contributing improvements back to the community.
