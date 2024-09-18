from datetime import datetime, timedelta
from typing import Optional

from googleapiclient.discovery import HttpError, Resource, build

from .base import Crawler


class YouTubeCrawler(Crawler):
    MAX_SEARCH_RESULTS: int = 50
    DEFAULT_VIDEOS_FETCH_PERIOD: int = 90
    MAX_COMMENTS_RESULTS: int = 20
    _client: Resource

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key
        self._client = None

    @property
    def client(self) -> Resource:
        if self._client:
            return self._client
        self._client = build('youtube', 'v3', developerKey=self.api_key)
        return self._client

    def _get_top_video_ids(self, query: str, days_period: Optional[int] = None, order_by: Optional[str] = None) -> list[str]:
        if not query:
            return []
        order_by = order_by or 'viewCount'
        days_period = days_period or self.DEFAULT_VIDEOS_FETCH_PERIOD
        n_days_ago = (datetime.now() - timedelta(days=days_period)).strftime('%Y-%m-%dT%H:%M:%SZ')
        try:
            search_response = self.client.search().list(
                q=query,
                type='video',
                order=order_by,
                publishedAfter=n_days_ago,
                part='id,snippet',
                maxResults=self.MAX_SEARCH_RESULTS
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            return video_ids
        except HttpError as e:
            print(str(e))
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
            return []

    def _is_valid_comment(self, comment: dict) -> bool:
        return True


    def _get_video_comments(self, video_id: str):
        try:
            comments = []
            results = self.client.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=self.MAX_COMMENTS_RESULTS,
                textFormat="plainText",
            ).execute()

            while results:
                for item in results['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    if not self._is_valid_comment(comment):
                        continue
                    comments.append({
                        'text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'likes': comment['likeCount'],
                    })
                if len(comments) >= self.MAX_COMMENTS_RESULTS:
                    break

                if 'nextPageToken' not in results:
                    break
                results = self.client.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=self.MAX_COMMENTS_RESULTS,
                    pageToken=results['nextPageToken']
                ).execute()

            return comments
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
            return []

    def get_video_transcript(self, video_id: str):
        pass

    def crawl(self, **kwargs) -> dict:
        video_ids = self._get_top_video_ids(**kwargs)
        comments = [
            comment
            for video_id in video_ids
            for comment in self._get_video_comments(video_id)
        ]
        return {'data': comments}
