import os
import pandas as pd
from googleapiclient.discovery import build

# Configurar a API do YouTube
API_KEY = 'YOUR-API'  # Substitua pela sua chave de API
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(channel_id):
    # Obter todos os vídeos do canal
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

def get_video_details(video_ids):
    # Obter detalhes dos vídeos
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

def analyze_channel(channel_id):
    video_ids = get_channel_videos(channel_id)
    video_details = get_video_details(video_ids)
    
    df = pd.DataFrame(video_details)
    print(f"Total Videos: {len(df)}")
    print(f"Average Views: {df['views'].mean()}")
    print(f"Average Likes: {df['likes'].mean()}")
    print(f"Average Comments: {df['comments'].mean()}")

    return df

if __name__ == "__main__":
    channel_id = 'THE-CHANNEL-ID'  # Substitua pelo ID do canal que você deseja analisar
    df = analyze_channel(channel_id)
    df.to_csv('youtube_channel_analysis.csv', index=False)
    print("Dados salvos em 'youtube_channel_analysis.csv'")