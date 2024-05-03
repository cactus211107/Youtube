import captions,downloader,random,os,db,datetime,requests,subprocess,spotify,re
from flask import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PYTUBE LETS GOOOOO'
db.initDB('database.db')
db.executeFile('.sql')
def getDate():return datetime.date.today().strftime('%Y-%m-%d')
def dateToTextDate(date):
    date = date.split('-')
    year = date[0]
    m={
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}
    month = m[int(date[1])]
    day = date[2].split(' ')[0]
def generateId():return random.randint(0,99999999)
def getUsersVideos(id):return db.parseResponseAsJSON(db.execute(f'SELECT VIDEOS FROM USERS WHERE ID={id} LIMIT 1').fetchone()[0])
def addVideoToUser(user_id,video_id):
    current_videos = getUsersVideos(user_id)
    if video_id in current_videos:return
    current_videos.append(video_id)
    db.execute(f'''UPDATE USERS SET VIDEOS="{str(current_videos)}" WHERE ID={user_id}''')
def getVideo(id):
    return db.execute(f'SELECT * FROM VIDEOS WHERE ID="{id}" LIMIT 1').fetchone()
def getVideoChapters(id):
    return jsonify(getVideo(id)[9])
def getChapters(initial_data):
    try:
        chapters=initial_data["playerOverlays"]["playerOverlayRenderer"]["decoratedPlayerBarRenderer"]["decoratedPlayerBarRenderer"]["playerBar"]["multiMarkersPlayerBarRenderer"]["markersMap"][0]["value"]["chapters"]
        chapters=[{
            "chapter":chapter['chapterRenderer']['title']['simpleText'],
            "start":chapter['chapterRenderer']['timeRangeStartMillis']/1000,
            "thumbnail_url":chapter['chapterRenderer']['thumbnail']['thumbnails'][-1],
            "id":generateId()
            } for chapter in chapters]
        return chapters
    except Exception as e:
        print(e)
    return []
def saveImageContent(content,path):
    with open(path,'wb') as f:
        f.write(content)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            id=downloader.get_id_from_url(request.form.get('url'))
            save_entire_video(id)
            # addVideoToUser(session.get('id'),id)
            return redirect('/watch?v='+id)
        except Exception as e:
            print(e)
            return redirect('/')
    # videos = getUsersVideos(session.get('id'))
    videos = db.execute('SELECT ID FROM VIDEOS ORDER BY UPLOAD_DATE ASC').fetchall()
    print(videos)
    
    return render_template('index.html',videos=videos)
@app.route('/spotify',methods=['GET','POST'])
def index_spotify():
    if request.method == 'POST':
        url=request.form.get('url')
        id = save_entire_song(url)
        return redirect('/spotify/track/'+id )
    return render_template('index_spotify.html')

@app.route('/watch')
def watch_video():
    id = request.args.get('v')
    video =  db.execute(f'SELECT * FROM VIDEOS WHERE ID="{id}" LIMIT 1').fetchone()
    return render_template('watch.html',id=id,title=video[1],description=video[2],channel_name=video[3],channel_id=video[4])
@app.route('/results')
def results():
    query = request.args.get('search_query')
    if not query:
        return redirect('/')
    return render_template('search.html',query=query)
@app.route('/spotify/track/<id>')
def spotifyTrack(id):
    song=db.execute(f'SELECT * FROM SONGS WHERE ID="{id}" LIMIT 1').fetchone()
    return render_template('listen.html',id=id,name=song[1],artists=json.loads(song[2]))

def format_captions(captions):
    formatted = []
    print('formatting captions',captions)
    for caption in captions:
        print(caption)
        print(type(caption))
        segs=caption['segs']
        print(1,segs)
        text = segs[0]['utf8']
        print(2,text)
        for seg in segs[1:]:
            text+=' ('+seg['utf8']+')'
        print('--------',text)
        formatted.append({"text":text,"start":caption['tStartMs']/1000,'duration':caption['dDurationMs']/1000})
    return formatted
    # return [{"text": ' '.join([f"{seg['utf8']} ({seg['utf8']})" for seg in caption['segs']]).strip(), "start": caption['tStartMs'] / 1000, 'duration': caption['dDurationMs'] / 1000} for caption in captions]
def getImageContent(url):
    return requests.get(url).content
def save_entire_video(id):
    if os.path.exists('downloaded/'+id):return
    video = downloader.YouTube('https://youtube.com/watch?v='+id)
    itag = downloader.get_adaptive_resolutions(video).filter(res='1080p').last() or downloader.get_adaptive_resolutions(video).last() # NOW MAX IS SET TO 1080p (9:52 tue feb 6 2024)
    itag=itag.itag
    downloader.download_adaptive_video(video,'downloaded/videos/'+id,itag,'video')

    caption_track = captions.getCaptions(video)
    with open(f'downloaded/videos/{id}/captions.json','w') as f:
        try:
            f.write(json.dumps(caption_track))
        except Exception as e:
            print('caption error:',e)
            f.write('[]')
    duration = video.length
    yt_date = video.publish_date
    date = getDate()
    title = video.title
    description = video.description
    thumb_url=f'https://i.ytimg.com/vi/{id}/hq720.jpg'
    channel_id = video.channel_id
    keywords = str(video.vid_info['videoDetails'].get('keywords') or '[]')
    channel_name = video.author
    directory = f'downloaded/videos/{id}/'
    os.makedirs(directory, exist_ok=True)
    os.makedirs(directory+'previews', exist_ok=True)
    saveImageContent(getImageContent(thumb_url),directory+'thumbnail.jpg')
    # get transcript in case there are no captions
    transcript=captions.get_transcript(id)
    with open(directory+'transcript.json','w') as f:
        f.write(json.dumps(transcript))
    if len(str(caption_track)) > 15:
        vtt=caption_track
        print('Chose captions')
    else:
        vtt=transcript
        print('Chose transcript')
    # make preview images
    preview_interval=5 # every `n` frames to take a preview image
    ffmpeg_command = [
        'ffmpeg',
        '-i', directory + 'video.mp4',
        '-vf', f'select=not(mod(t\,{preview_interval})),scale=120:-1',
        '-q:v', '2',
        '-vsync', 'vfr',
        directory + 'previews/preview%d.jpg'
    ]
    subprocess.run(ffmpeg_command)
    try:
        chapters = getChapters(video.initial_data)
        for chapter in chapters:
            saveImageContent(getImageContent(chapter['thumbnail_url']),directory+"chapters_thumbs/"+chapter['id']+'.jpg')
    except Exception as e:
        chapters=[]
        print(e)

    db.execute(F'INSERT INTO VIDEOS VALUES ({"?,"*9}?)',(id,title,description,channel_name,channel_id,yt_date,date,duration,keywords,json.dumps(chapters)))

def save_entire_song(url):
    song = spotify.Spotify(url)
    id=song.id
    path=f'downloaded/audio/{id}/'
    yt_url=song.download(filepath=path,filename='audio.mp3')
    saveImageContent(getImageContent(song.cover.url),path+'cover.jpg')
    lyrics = song.lyrics
    with open(path+'lyrics.json','w') as f:
        f.write(json.dumps(lyrics))
    yt_lyrics = captions.get_transcript(captions.YouTube(yt_url))
    with open(path+'yt_lyrics.json','w') as f:
        f.write(json.dumps(yt_lyrics))
    transcript_lyrics = captions.get_transcript(downloader.YouTube(yt_url).video_id)
    with open(path+'transcript_lyrics.json','w') as f:
        f.write(json.dumps(transcript_lyrics))
    _artists = song.other_artists
    _artists.insert(0,song.first_artist)
    artists = []
    for artist in _artists:
        artists.append(
            {
                "name":artist.name,
                "id":artist.id,
                "pfp":{
                    "bg":artist.pfp.background,
                    "url":artist.pfp.url
                    },
                "url":artist.url,
                "verified":artist.verified,
            }
        )
    db.execute(f'INSERT INTO SONGS VALUES ({"?,"*8}?)',(id,song.name,json.dumps(artists),song.date,song.duration/1000,getDate(),id,captions.YouTube(yt_url).video_id,song.album))
    return id
    
    

@app.route('/captions')
def api_captions():
    _captions = ''
    _=request.args.get
    path=f'downloaded/{_("type","videos")}/{_("id")}/'
    with open(path+'captions.json') as f:
        _captions=f.read()
    if len(_captions) <=6:
        with open(path+'transcript.json') as f:
            print('chose transcript')
            _captions=jsonify(f.read())
    return _captions
@app.route('/spotify_search')
def api_spotify_search():
    q=request.args.get('q')
    songs = spotify.Search(q).tracks
    songs=[{
        "name":song.name,
        "artist":song.artists[0].name,
        "cover":{
            "bg":song.pfp.background,
            "url":song.pfp.url
        },
        "url":song.url,
        "album":song.album.name,
        "duration":song.duration
    } for song in songs]
    return songs
@app.route('/songs')
def api_spotify_songs_all():
    return db.execute('SELECT * FROM SONGS').fetchall()
@app.route('/lyrics')
def api_spotify_lyrics():
    lyrics = []
    id=request.args.get('id')
    base='/downloaded/audio/'+id+'/'
    with open(base+'lyrics.json') as f:
        lyrics = lyrics or f.read()
    with open(base+'yt_lyrics.json') as f:
        lyrics = lyrics or f.read()
    with open(base+'transcript_lyrics.json') as f:
        lyrics = lyrics or f.read()
    return lyrics

@app.route('/downloaded/<path:name>')
def getDownloadedStuff(name):
    return send_file(os.path.join('downloaded',name))
@app.before_request
def load_user():
    if not session.get('id'):
        session['id'] = generateId()
        db.execute('INSERT INTO USERS VALUES (?,?,?)',(session.get('id'),'[]','[]'))
def display_video(id):
    def time_ago(datetime_str):
        current_time = datetime.datetime.now()
        parsed_time = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        
        time_difference = current_time - parsed_time
        
        # Calculate years, months, days, hours, minutes, and seconds
        years = time_difference.days // 365
        months = time_difference.days // 30
        days = time_difference.days
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds % 3600) // 60
        seconds = time_difference.seconds % 60

        if years > 0:
            return f"{years} years ago"
        elif months > 0:
            return f"{months} months ago"
        elif days > 0:
            return f"{days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return f"{seconds} seconds ago"
    video = getVideo(id)
    return f"""
<div class="video">
    <a href="/watch?v={ video[0] }">
        <div class="thumbnail">
            <img src="/downloaded/videos/{ video[0] }/thumbnail.jpg" alt="Thumbnail">
            <div class="duration">{ re.sub(r'^00:','',datetime.datetime.fromtimestamp(video[7],datetime.timezone.utc).strftime('%H:%M:%S')) }</div>
        </div>
        <div class="info">
            <div class="title">{ video[1] }</div>
            <div class="channel">{ video[3] }</div>
            <div class="youtube-date">{ time_ago(video[5]) }</div>
        </div>
    </a>
</div>
"""

@app.context_processor
def more_code():return{'display_video':display_video}


def run(online=True):
    app.run(host = '0.0.0.0' if online else None, port = 6969)


run()