import responses

def add_youtube_video_response():
    yt_url = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyC-nrN3dQG2myUiOVRW7uOeCMib-YnJ344&channelId=test_external_id&type=video&part=snippet,id&order=date&maxResults=20'
    yt_response = {
        'items': [{
            'id': {
                'videoId': 'test_video_id'
            },
            'snippet': {
                'title': 'test_title',
                'publishedAt': 'random_date',
                'thumbnails': {
                    'high': {
                        'url': 'test_thumbnail_url'
                    }
                }
            }
    }]
    }
    responses.add(
        responses.GET, yt_url,
        json=yt_response, status=200
    )