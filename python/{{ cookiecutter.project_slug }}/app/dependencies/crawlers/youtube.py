from googleapiclient.discovery import HttpError, Resource, build

from .base import Crawler


class YouTubeCrawler(Crawler):
    MAX_SEARCH_RESULTS: int = 50
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


    def crawl(self, depth: int = 1, **kwargs) -> dict:
        query = kwargs.get('query')
        if not query:
            return {}
        try:
            search_response = self.client.search().list(
                q=query,
                type='video',
                part='id,snippet',
                maxResults=self.MAX_SEARCH_RESULTS
            ).execute()

            videos = []
            for search_result in search_response.get('items', []):
                video = {
                    'title': search_result['snippet']['title'],
                    'description': search_result['snippet']['description'],
                    'video_id': search_result['id']['videoId'],
                    'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
                    'channel_title': search_result['snippet']['channelTitle'],
                    'published_at': search_result['snippet']['publishedAt']
                }
                videos.append(video)
            return {'data': videos}
        except HttpError as e:
            print(str(e))
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
            return {}
