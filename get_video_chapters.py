from pytube import YouTube
import requests,json
def getImageContent(url):
    return requests.get(url).content
def saveImageContent(content,path):
    with open(path,'wb') as f:
        f.write(content)
def getChapters(initial_data):
    try:
        chapters=initial_data["playerOverlays"]["playerOverlayRenderer"]["decoratedPlayerBarRenderer"]["decoratedPlayerBarRenderer"]["playerBar"]["multiMarkersPlayerBarRenderer"]["markersMap"][0]["value"]["chapters"]
        chapters=[{
            "chapter":chapter['chapterRenderer']['title']['simpleText'],
            "start":chapter['chapterRenderer']['timeRangeStartMillis']/1000,
            "thumbnail":chapter['chapterRenderer']['thumbnail']['thumbnails'][-1]
            } for chapter in chapters]
        return chapters
    except Exception as e:
        print(e)
    return []
with open('test.json','w') as f:
    f.write(json.dumps(YouTube('watch?v=N3cYojoqeNA').initial_data))
# print(getChapters(YouTube('watch?v=N3cYojoqeNA')))