# YouTube Data Scraper 🎥

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pejman-ebrahimi-4a60151a7/)
[![HuggingFace](https://img.shields.io/badge/🤗_Hugging_Face-FFD21E?style=for-the-badge)](https://huggingface.co/arad1367)

![YouTube Scraper](youtube.png)

A Python-based YouTube data collection tool for academic research, enabling systematic collection of video metadata, engagement metrics, and comments through the official YouTube Data API v3.

## 📋 Overview

This scraper was developed for research on organizational communication during geopolitical crises, specifically to analyze:
- How organizational statements spread across platforms
- Engagement patterns during crisis events
- Audience responses through comment analysis
- Comparative amplification between different organization types

**Test Collection Results:**
- ✅ 125 videos collected
- ✅ 2,183 comments analyzed
- ✅ Topic: "Capital organisations during geopolitical crises"

## 🎯 Features

- **Video Search**: Query-based video discovery with customizable filters
- **Engagement Metrics**: Automatic collection of views, likes, and comment counts
- **Comment Extraction**: Retrieve top-level comments with metadata
- **Batch Processing**: Efficient handling of multiple videos
- **Date Filtering**: Target specific time periods for crisis analysis
- **CSV Export**: Structured output for easy data analysis
- **Error Handling**: Graceful handling of API limits and disabled comments

## 📊 Data Categories

### Category 1: Posts & Engagement (Fully Supported)
- ✅ Video posts (title, description, channel, publish date)
- ✅ Engagement metrics (views, likes, comment counts)
- ✅ Comments with author information and timestamps
- ✅ Duration and content details

### Categories 2-4: Advanced Signals (Not Available via Free API)
- ❌ Algorithmic rankings/amplification signals
- ❌ Platform-applied misinformation labels
- ❌ Bot activity indicators

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip install google-api-python-client
```

### API Key Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**:
   - Navigate to [API Library](https://console.cloud.google.com/apis/library)
   - Search "YouTube Data API v3"
   - Click Enable
4. Create API credentials:
   - Go to [Credentials](https://console.cloud.google.com/apis/credentials)
   - Click "CREATE CREDENTIALS" → "API key"
   - Copy your API key
5. Configure restrictions (optional):
   - For local scripts: Set "Application restrictions" to "None"
   - For production: Add IP restrictions

### Installation

```bash
git clone https://github.com/arad1367/YouTube-Scraper.git
cd YouTube-Scraper
pip install -r requirements.txt
```

### Usage

1. Add your API key to the script:

```python
API_KEY = "your_api_key_here"
```

2. Customize search parameters:

```python
if __name__ == "__main__":
    search_query = "your search topic"
    max_videos = 500
    max_comments_per_video = 100
    published_after = "2024-01-01T00:00:00Z"
```

3. Run the scraper:

```bash
python youtube_data_collector.py
```

## 📈 API Quota & Limits

### Free Tier Quotas
- **Daily Limit**: 10,000 units per day (resets at midnight Pacific Time)
- **Search Query**: 100 units
- **Video Details**: 1 unit per video
- **Comments**: 1 unit per 100 comments

### Collection Capacity

| Configuration | Videos | Comments | Units Used | % of Daily Quota |
|---------------|--------|----------|------------|------------------|
| Small Test | 25 | 500 | ~130 | 1.3% |
| Balanced | 500 | 50,000 | ~1,100 | 11% |
| Large Scale | 1,000 | 50,000 | ~1,600 | 16% |
| Maximum Daily | 2,000 | 100,000 | ~2,700 | 27% |

### Scaling Strategies

**Daily Collection (Single Run):**
- 500 videos with 100 comments each = 50,000 comments
- Uses: 1,100 units (11% of quota)

**Weekly Collection:**
- 3,500 videos with 100 comments = 350,000 comments

**Monthly Collection:**
- 15,000 videos with 100 comments = 1,500,000 comments

**Multiple Searches per Day:**
Run 5-8 times with different queries to maximize coverage while staying under quota.

## 📁 Output Files

### youtube_videos.csv
Contains one row per video with:
- `video_id`: Unique YouTube video identifier
- `title`: Video title
- `channel_id`: Channel identifier
- `channel_title`: Channel name
- `published_at`: Publication timestamp
- `description`: Video description
- `view_count`: Total views
- `like_count`: Total likes
- `comment_count`: Total comments
- `duration`: Video duration (ISO 8601 format)

### youtube_comments.csv
Contains one row per comment with:
- `comment_id`: Unique comment identifier
- `video_id`: Associated video ID
- `video_title`: Video title for reference
- `author`: Comment author username
- `text`: Comment content
- `like_count`: Comment likes
- `published_at`: Comment timestamp

## 🔧 Configuration Options

### Search Parameters

```python
def search_videos(query, max_results=50, order='relevance', published_after=None)
```

- **query**: Search keywords
- **max_results**: Number of videos to retrieve
- **order**: Sorting method (`relevance`, `date`, `viewCount`, `rating`)
- **published_after**: ISO 8601 timestamp for date filtering

### Comment Collection

```python
def get_video_comments(video_id, max_comments=100)
```

- **video_id**: Target video
- **max_comments**: Maximum comments per video
- Automatically handles videos with disabled comments

## 📚 Research Applications

### Supported Research Questions

1. **Organizational Communication Analysis**
   - How do different organizations frame crisis events?
   - Engagement comparison between high vs. low Strategic Influence Capital organizations

2. **Temporal Analysis**
   - Communication patterns before/during/after geopolitical events
   - Crisis response timing and audience engagement

3. **Audience Response**
   - Sentiment analysis through comment text
   - Engagement velocity and virality indicators

4. **Cross-Platform Comparison** (when combined with other scrapers)
   - YouTube vs. Reddit vs. Telegram engagement patterns
   - Platform-specific amplification differences

## ⚠️ Limitations

### Technical Constraints
- Daily API quota limits large-scale collection to ~2,000 videos
- Comments are top-level only (no nested replies)
- Real-time algorithmic ranking data not accessible
- Video recommendations not exposed via API

### Data Availability
- ❌ Algorithmic amplification signals
- ❌ Shadow-banning or suppression indicators
- ❌ Platform-applied content labels
- ❌ Internal engagement/reach metrics beyond public counts

## 🌐 Platform Comparison

| Platform | API Access | Cost | Data Richness | Ease of Use |
|----------|-----------|------|---------------|-------------|
| **YouTube** | ✅ Free (10K units/day) | Free | High | ⭐⭐⭐⭐⭐ |
| **Reddit** | ✅ Free (100 req/min) | Free | High | ⭐⭐⭐⭐⭐ |
| **Telegram** | ✅ Free (unlimited) | Free | Medium | ⭐⭐⭐⭐ |
| **X/Twitter** | ⚠️ Extremely limited | $200+/month | High | ⭐ |
| **LinkedIn** | ❌ No content API | N/A | N/A | ❌ |
| **TikTok** | ⚠️ Institutional only | Partnership | High | ⭐⭐ |

## 🛠️ Troubleshooting

### "Requests from referer <empty> are blocked"
**Solution**: Change API key restrictions to "None" in Google Cloud Console

### "Quota exceeded"
**Solution**: Wait until midnight Pacific Time for quota reset, or create additional projects

### "Comments disabled" errors
**Solution**: Script automatically skips videos with disabled comments (normal behavior)

### Low comment counts
**Solution**: Some videos naturally have fewer comments; increase `max_videos` to compensate

## 📖 Code Structure

```
youtube_data_collector.py
├── search_videos()           # Query YouTube for videos
├── get_video_statistics()    # Retrieve engagement metrics
├── get_video_comments()      # Extract comments
└── collect_youtube_data()    # Main orchestration function
```

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Multi-threaded collection for speed optimization
- Automatic quota monitoring and management
- Reply thread extraction (nested comments)
- Sentiment analysis integration
- Database storage instead of CSV

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Ethical Considerations

- **Privacy**: Only collects publicly available data
- **Terms of Service**: Uses official YouTube API (compliant with ToS)
- **Rate Limiting**: Respects API quotas to avoid service disruption
- **Data Storage**: Ensure GDPR compliance if analyzing EU user data
- **Research Ethics**: Obtain institutional review board approval when analyzing user behavior

## 📞 Contact

**Pejman Ebrahimi**
- Email: [pejman.ebrahimi77@gmail.com](mailto:pejman.ebrahimi77@gmail.com)
- LinkedIn: [Pejman Ebrahimi](https://www.linkedin.com/in/pejman-ebrahimi-4a60151a7/)
- HuggingFace: [@arad1367](https://huggingface.co/arad1367)
- GitHub: [@arad1367](https://github.com/arad1367)

## 🙏 Acknowledgments

- Google YouTube Data API v3
- Academic research community studying digital communication
- Open-source Python community

---

**Note**: This tool is designed for academic research purposes. Ensure compliance with institutional ethics guidelines and applicable data protection regulations when collecting and analyzing social media data.

**Last Updated**: February 2026
