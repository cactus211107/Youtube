import os,requests
videos = os.listdir('downloaded/videos')
for video in videos:
    id = video
    thumb_url = f'https://i.ytimg.com/vi/{id}/hq720.jpg'
    with open(f'downloaded/videos/{id}/thumbnail.jpg','wb') as f:
        f.write(requests.get(thumb_url).content)