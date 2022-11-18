#import configparser
import requests
import json
from urllib.parse import quote_plus

'''config = configparser.ConfigParser()
config.read('settings.conf')
api_key = config['api']['api_key']'''

# parameters to pass
initial_entry_on_channel = True
new_date = 'should pass date one month from now'



class YouTubeAPI:

    def get_channels_by_name(search_name):
        channels_result = []
        print(search_name)
        url = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={search_name}&type=channel&key={api_key}'
        response = requests.get(url)
        print(response.__dict__)
        response_channels = json.loads(response.text)['items']
        for channel in response_channels:
            channel = channel['snippet']
            channels_result.append(
                {
                    'external_id': channel['channelId'],
                    'name': channel['title'],
                    'thumbnail_url': channel['thumbnails']['high']['url']
                }
            )
        return channels_result

    # extract all video information of the channel
    def get_channel_video_data(self):
        self._get_channel_content(self.limit)

    # extract all videos per channel
    def _get_channel_content(self, limit, check_all_pages=True):
        if initial_entry_on_channel:
            url = f'https://www.googleapis.com/youtube/v3/search \
                ?key={self.api_key} \
                &channelId={self.channel_id} \
                &part=snippet,id \
                &order=date \
                &publishedAfter={new_date}'

        # url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"


        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

        npt = self._get_channel_content_per_page(url)
        idx = 0
        while (check_all_pages and npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            npt = self._get_channel_content_per_page(nexturl)
            idx += 1

    # extracts all videos per page
    # returns nextPageToken
    def _get_channel_content_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)

        if 'items' not in data:
            print('Error! Could not get correct channel data!\n', data)
            return None

        nextPageToken = data.get("nextPageToken", None)

        item_data = data['items']
        for item in item_data:
            try:
                kind = item['id']['kind']
                published_at = item['snippet']['publishedAt']
                title = item['snippet']['title']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
                    url = "https://www.youtube.com/watch?v=" + video_id
                    v = video(video_id, url, thumbnail, published_at, title)
                    self.videos.append(v)
            except KeyError as e:
                print('Error! Could not extract data from item:\n', item)

        return nextPageToken
