# YouTube Channel Analysis README

## Overview
This script analyzes a YouTube channel by retrieving and analyzing data from the YouTube API. It collects video details such as views, likes, and comments, and saves the analysis in a CSV file. The script is written in Python and uses the `googleapiclient` and `pandas` libraries.

## Prerequisites
Before you run this script, ensure you have the following installed:

- Python 3.x
- `googleapiclient` library
- `pandas` library

You can install the required libraries using pip:
```bash
pip install google-api-python-client pandas
```

## Setup
1. **API Key**: Obtain a YouTube Data API v3 key from the Google Developer Console. Replace `'YOUR-API'` with your API key in the script.

2. **Channel ID**: Identify the YouTube channel ID you wish to analyze. Replace `'THE-CHANNEL-ID'` in the script with the channel ID.

## Script Explanation
### 1. Import Libraries
```python
import os
import pandas as pd
from googleapiclient.discovery import build
```
- `os`: For interacting with the operating system.
- `pandas`: For data manipulation and analysis.
- `googleapiclient.discovery`: For interacting with the YouTube Data API.

### 2. Configure the YouTube API
```python
API_KEY = 'YOUR-API'
youtube = build('youtube', 'v3', developerKey=API_KEY)
```
- Replace `'YOUR-API'` with your actual YouTube Data API v3 key.

### 3. Retrieve Channel Videos
```python
def get_channel_videos(channel_id):
    videos = []
    request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=50, order='date')
    response = request.execute()
    
    while response:
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                videos.append(video_id)
        
        if 'nextPageToken' in response:
            request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=50, order='date', pageToken=response['nextPageToken'])
            response = request.execute()
        else:
            break

    return videos
```
- This function retrieves video IDs from a given channel using the YouTube Data API.

### 4. Retrieve Video Details
```python
def get_video_details(video_ids):
    video_details = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(part='snippet,statistics', id=','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for item in response['items']:
            video_data = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'views': int(item['statistics'].get('viewCount', 0)),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'comments': int(item['statistics'].get('commentCount', 0))
            }
            video_details.append(video_data)
    
    return video_details
```
- This function retrieves details such as views, likes, and comments for each video.

### 5. Analyze Channel Data
```python
def analyze_channel(channel_id):
    video_ids = get_channel_videos(channel_id)
    video_details = get_video_details(video_ids)
    
    df = pd.DataFrame(video_details)
    print(f"Total Videos: {len(df)}")
    print(f"Average Views: {df['views'].mean()}")
    print(f"Average Likes: {df['likes'].mean()}")
    print(f"Average Comments: {df['comments'].mean()}")

    return df
```
- This function analyzes the collected video data and prints out the total number of videos, average views, likes, and comments.

### 6. Main Function
```python
if __name__ == "__main__":
    channel_id = 'THE-CHANNEL-ID'
    df = analyze_channel(channel_id)
    df.to_csv('youtube_channel_analysis.csv', index=False)
    print("Data saved to 'youtube_channel_analysis.csv'")
```
- The main function executes the analysis for a specified channel ID and saves the results to a CSV file.

## Running the Script
1. Ensure you have replaced `'YOUR-API'` and `'THE-CHANNEL-ID'` with your API key and the channel ID you wish to analyze.
2. Run the script:
```bash
python your_script_name.py
```
3. The script will print the analysis results and save them to a file named `youtube_channel_analysis.csv`.

## Output
- The output CSV file will contain columns for `video_id`, `title`, `views`, `likes`, and `comments` for each video in the analyzed channel.

By following these steps, you can successfully analyze a YouTube channel's video performance using this script.
