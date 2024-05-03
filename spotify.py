import requests,json,pytube,datetime,threading,subprocess
from bs4 import BeautifulSoup as Soup
import urllib.parse
def parse_cookie_string(cookie_string):
    cookies = {}
    for cookie in cookie_string.split('; '):
        key, value = cookie.split('=', 1)
        cookies[key] = value
    return cookies
def getAccessToken(logged_in=False):
    if logged_in:
        with requests.Session() as s:
            cookies=parse_cookie_string('sss=1; sp_t=bf5d50a8-cccc-466d-a663-1f3f231ac373; sp_new=1; sss=1; sp_key=ba4f0348-b8ed-4389-be67-952c32fa296c; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Mar+18+2024+08%3A21%3A19+GMT%2B0200+(South+Africa+Standard+Time)&version=202309.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=s00%3A1%2Cf00%3A1%2Cm00%3A1%2Ct00%3A1%2Ci00%3A1%2Cf11%3A1%2Cm03%3A1&AwaitingReconsent=false')
            for cookie_name, cookie_value in cookies.items():
                s.cookies.set(cookie_name, cookie_value,domain='.spotify.com')
            CURL="""curl 'https://open.spotify.com/track/1ChulFMnwxoD74Me8eX2TU' \
  -H 'authority: open.spotify.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'cookie: sp_t=eb24e891f0c4086fc69b8cbb9452c82e; sp_landing=https%3A%2F%2Fopen.spotify.com%2Ftrack%2F1ChulFMnwxoD74Me8eX2TU%3Fsp_cid%3Deb24e891f0c4086fc69b8cbb9452c82e%26device%3Ddesktop; sp_dc=AQDC-xnqAtfYdrXv4zpgSyYU0KcfRwVj9kbVl1peJVgcmZiT_m-2uzQQcN1aeulUUXUgZDmTc7NaEnq7hFjR1jYsLaFKl01zyrv2GHL4qnTxr-F88usohvcZVHzUxBSrkpEW_pjdtRAYDJnI7kpXfCQ2FqFyyo9L; sp_key=5a3b8340-cbb6-4324-856a-88a00aebdf40; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Mar+18+2024+08%3A56%3A41+GMT%2B0200+(South+Africa+Standard+Time)&version=202309.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=s00%3A1%2Cf00%3A1%2Cm00%3A1%2Ct00%3A1%2Ci00%3A1%2Cf11%3A1%2Cm03%3A1&AwaitingReconsent=false' \
  -H 'pragma: no-cache' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'"""
            process = subprocess.Popen(CURL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            page = stdout.decode('utf-8')
            with open('page.html','w') as f:
                f.write(page)
            html = Soup(page,features='html.parser')
            script = html.select_one('#session').text
            accessToken = json.loads(script)['accessToken']
            print('ACCESS TOKEN')
            return accessToken
    page = requests.get('https://open.spotify.com/track/5A32buYzWvtkJizBkX8OCQ?si=a5de099e65fe4832&nd=1&dlsi=764c7fd25d034edf',timeout=5).text
    html = Soup(page,features='html.parser')
    script = html.select_one('#session').text
    accessToken = json.loads(script)['accessToken']
    print('ACCESS TOKEN')
    return accessToken
ACCESS_TOKEN=None
try:
    ACCESS_TOKEN = getAccessToken()
except:
    print('You are offline')
# def setAccessToken():
#     global ACCESS_TOKEN
#     ACCESS_TOKEN=getAccessToken()
# threading.Thread(target=setAccessToken)

def getIdFromURI(uri):return uri.split(':')[-1]
def toUrl(type,id):return f'https://open.spotify.com/{type}/{id}'
def getHighestQualityPFP(pfps):return sorted(pfps,key=lambda x:x['width'],reverse=True)[0]
def getPFP(artist):
    try:
        return getHighestQualityPFP(artist['data']['visuals']['avatarImage']['sources'])
    except:
        try:
            return getHighestQualityPFP(artist['visuals']['avatarImage']['sources'])
        except:
            pass
    return {'url':None,'width':0,'height':0}
def getBG(artist):
    try:
        return artist['extractedColors']['colorDark']['hex']
    except:
        return '#000'
def getAlbumPreviewCover(album):
    try:
        # print('---------------')
        # print(json.dumps(album,indent=4))
        # print(getHighestQualityPFP(album['coverArt']['sources']))
        # print('---------------')
        return getHighestQualityPFP(album['coverArt']['sources'])
    except:
        return {"url":None,"width":0,"height":0}
class ProfilePicture:
    def __init__(self,url,bg) -> None:
        self.url=url
        self.background=bg
class Artist:
    def __init__(self) -> None:
        pass
class ArtistPreview:
    def __init__(self,name:str,uri:str,verified:bool,pfp:ProfilePicture):
        self.uri=uri
        self.id=getIdFromURI(uri)
        self.name=name
        self.verified=verified
        self.pfp=pfp
        self.url=toUrl('artist',self.id)
class Album:
    def __init__(self) -> None:
        pass
class AlbumPreview:
    def __init__(self,artists:list[ArtistPreview|Artist],name,uri,cover:ProfilePicture,date={"year":0}):
        self.uri=uri
        self.id=getIdFromURI(uri)
        self.url=toUrl('album',self.id)
        self.artists=artists
        self.date=date
        self.name=name
        self.cover=cover
class Track:
    def __init__(self,uri,name,artists,cover,plays,duration,rating,playable,date,album):
        self.uri=uri
        self.name=name
        self.artists=artists
        self.cover=cover
        self.plays=plays
        self.duration=duration
        self.rating=rating
        self.playable=playable
        self.date=date
        self.album=album
    def download(self,filepath,filename):
        # search song on youtube
        yt:pytube.YouTube = pytube.Search(self.name+', by'+self.artists[0]).results[0]
        print(yt.title)
        print(yt.channel_url)
        yt.streams.get_audio_only().download(filepath,filename)    
class TrackPreview:
    def __init__(self,uri,name,artists,pfp,duration,rating,playable,album) -> None:
        self.uri=uri
        self.id=getIdFromURI(uri)
        self.url=toUrl('track',self.id)
        self.name=name
        self.artists:list[ArtistPreview]=artists
        self.pfp:ProfilePicture=pfp
        self.duration=duration
        self.rating=rating
        self.playable=playable
        self.album:AlbumPreview=album
class Search:
    def __init__(self,query:str):
        self._initial_data = self.__request__(query)
        # print(self._initial_data)
        self.initial_data=self._initial_data['data']['searchV2']
        self._albums = self.initial_data['albumsV2']['items']
        self._tracks=self.initial_data['tracksV2']['items']
        self._artists=self.initial_data['artists']['items']
        self._top=self.initial_data['topResultsV2']['itemsV2']
        self._playlists=self.initial_data['playlists']['items']
        self.artists:list[ArtistPreview]=[]
        self.albums:list[AlbumPreview]=[]
        self.tracks:list[TrackPreview]=[]
        self.top:list[TrackPreview]=[]
        self.playlists=list[list[list]]
        self.__parse__()
    def __parse__(self):
        # for artist in self._artists:
        #     print(artist['data']['visuals']['avatarImage']['sources'])
        self.artists=[ArtistPreview(
            artist['data']['profile']['name'],
            artist['data']['uri'],
            artist['data']['profile']['verified'],
            ProfilePicture(
                getPFP(artist)['url'],
                getBG(artist['data']['visuals']['avatarImage'])
            )
            ) for artist in self._artists]
        # for album in self._albums:
        #     print('\n\n\n\n\n\n\n')
        #     try:
        #         print('name',album['data']['name'])
        #     except:
        #         print('album',album['data'])
        # _artists = []
        # try:_artists = album['data']['artists']['items']
        # except:
        #     try:_artists=album['data']['preReleaseContent']['artists']['items']
        #     except:pass
        # def getArtists(album):
        #     try:
        #         return album['data']['preReleaseContent']['artists']['items'] if album['data']['__typename']=='PreRelease' else album['data']['artists']['items']
        #     except:
        #         # print('JGFKHFJKAHFKDJHSDFKJAHSJKFHASJKFHSKJFHKSA',album)
        #         try:
        #             return albq
        # album['data']['preReleaseContent']['artists']['items'] if album['data']['__typename']=='PreRelease' else album['data']['artists']['items']
        self.albums=[AlbumPreview(
            [
                ArtistPreview(
                    artist.get('profile').get('name') if artist.get('profile') else artist.get('name'),
                    artist.get('uri') if artist.get('uri') else artist.get('data').get('uri'),
                    None,
                    ProfilePicture(None,'#000')
                    ) for artist in self._artists
            ],
            album['data']['preReleaseContent']['name'] if album['data']['__typename']=='PreRelease' else album['data']['name'],
            album['data']['preReleaseContent']['name'] if album['data']['__typename']=='PreRelease' else album['data']['uri'],
            ProfilePicture(
                getAlbumPreviewCover(album['data']['preReleaseContent'] if album['data']['__typename']=='PreRelease' else album['data'])['url'],
                getBG(album['data']['preReleaseContent'] if album['data']['__typename']=='PreRelease' else album)
            ),
            album['data'].get('date')
        ) for album in self._albums]
        # print(self._tracks)
        self.tracks = [TrackPreview(
            track['item']['data']['uri'],
            track['item']['data']['name'],
            [ArtistPreview(artist['profile']['name'],artist['uri'],None,ProfilePicture(None,'#000')) for artist in track['item']['data']['artists']['items']],
            ProfilePicture(
                getAlbumPreviewCover(track['item']['data']['albumOfTrack'])['url'],
                getBG(track['item']['data']['albumOfTrack']['coverArt'])
                ),
            track['item']['data']['duration']['totalMilliseconds'],
            track['item']['data']['contentRating']['label'],
            track['item']['data']['playability']['playable'],
            AlbumPreview([],track['item']['data']['albumOfTrack']['name'],track['item']['data']['albumOfTrack']['uri'],ProfilePicture(
                getAlbumPreviewCover(track['item']['data']['albumOfTrack'])['url'],
                getBG(track['item']['data']['albumOfTrack']['coverArt'])
                ),'')
            ) for track in self._tracks]
        """
        TODO: PLAYLISTS, TOP RESULTS
        """

    def __request__(self,q,o=0,t=5,l=10,a=True): # q:quey | o:offset | t:number of top results | l:limit | a:include audio books
        global ACCESS_TOKEN
        url = 'https://api-partner.spotify.com/pathfinder/v1/query'
        headers = {
            'authority': 'api-partner.spotify.com',
            'accept': 'application/json',
            'accept-language': 'en',
            'app-platform': 'WebPlayer',
            'authorization': 'Bearer '+ACCESS_TOKEN,
            'cache-control': 'no-cache',
            # 'client-token': 'AADVtXIw6tJLkkHOUUri9p8zmZ1sOpDgTLeANSxvutYPqpQiOwa58wPIs6GRntXv/CyepYKRURpkJaUDfPvBoz+lReL2k93ODJBGdATOzya/FAUPtsWSGTeuI3xElq5YnDUVo0Ejdo16d5W+l5JwrR7Lr+8LyMWicsmnQhLuA3VtXi5+Xny5bhKpqBZlcCOcc+o8OATXHxrTMB23UWUb/U5x7MOOyv5BNx7sTFXVGSTI4tF8RPSWsuIQFxLDBY4spXeokqt4en5zLNj+qFhlnQSWXmA+BA5gdkY=',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://open.spotify.com',
            'pragma': 'no-cache',
            'referer': 'https://open.spotify.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'spotify-app-version': '1.2.33.0-unknown',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        }

        params = {
            'operationName': 'searchDesktop',
            'variables': '{"searchTerm":"'+q+'","offset":'+str(o)+',"limit":'+str(l)+',"numberOfTopResults":'+str(t)+',"includeAudiobooks":'+str(a).lower()+'}',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"5e360fd8ecc91d7a2aa8ab520bad903cc67f864a9df86b579cf51a53c9589b7f"}}'
        }
        try:
            return requests.get(url, headers=headers, params=params).json()
        except Exception as e:
            print(e)
            "GET ACCESS TOKEN"
            ACCESS_TOKEN = getAccessToken()
            return self.__request__(q,o,t,l,a)
class Spotify:
    def __init__(self,url):
        self.url = url
        self.uri = self.__parse_uri__(self.url)
        self.id=getIdFromURI(self.uri)
        self._initial_data=self.__request__(self.uri)
        self.initial_data=self._initial_data
        self.name=None
        self.first_artist=None
        self.other_artists:list[ArtistPreview]=None
        self.cover=None
        self.playable=None
        self.plays=None
        self.duration=None
        self.date=None
        self.rating=None
        self.album=None
        self._lyrics=None
        self.track = self.__parse__()
    def __parse_uri__(self,url):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        return "spotify"+parsed_url.path.replace('/',':')
    def __request__(self,uri):
        global ACCESS_TOKEN
        url = 'https://api-partner.spotify.com/pathfinder/v1/query?operationName=getTrack&variables={"uri":"'+uri+'"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"ae85b52abb74d20a4c331d4143d4772c95f34757bfa8c625474b912b9055b5c0"}}'
        headers = {
            'authority': 'api-partner.spotify.com',
            'accept': 'application/json',
            'accept-language': 'en',
            'app-platform': 'WebPlayer',
            'authorization': 'Bearer '+ACCESS_TOKEN,
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://open.spotify.com',
            'pragma': 'no-cache',
            'referer': 'https://open.spotify.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'spotify-app-version': '1.2.33.0-unknown',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        }
        try:
            return requests.get(url,headers=headers).json()
        except Exception as e:
            print(e)
            ACCESS_TOKEN=getAccessToken()
            return self.__request__(uri)
    def __parse__(self):
        "TODO: finish class"
        data = self.initial_data['data']['trackUnion']
        self.name=data['name']
        _first_artist=data['firstArtist']['items'][0]
        self.first_artist=ArtistPreview(_first_artist['profile']['name'],_first_artist['uri'],None,ProfilePicture(getPFP(_first_artist)['url'],'#000'))
        self.other_artists=[]
        self.cover=ProfilePicture(getAlbumPreviewCover(data['albumOfTrack'])['url'],getBG(data['albumOfTrack']['coverArt']))
        self.playable=data['playability']['playable']
        self.plays=int(data['playcount'])
        self.duration=data['duration']['totalMilliseconds']
        self.date=data['albumOfTrack']['date']['isoString']
        self.rating=data['contentRating']['label']
        self.album=''
        self._lyrics=None
        return Track(self.uri,self.name,self.other_artists,self.cover,self.plays,self.duration,self.rating,self.playable,self.date,self.album)
    def __get_lyrics__(self):
        global ACCESS_TOKEN
        logged_in_ACCESS_TOKEN=getAccessToken(True)
        url = f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{self.id}/image/{urllib.parse.quote_plus(self.cover.url)}?format=json&vocalRemoval=false&market=from_token'
        headers = {
    'authority': 'spclient.wg.spotify.com',
    'accept': 'application/json',
    'accept-language': 'en',
    'app-platform': 'WebPlayer',
    'authorization': 'Bearer '+logged_in_ACCESS_TOKEN,
    'cache-control': 'no-cache',
    'origin': 'https://open.spotify.com',
    'pragma': 'no-cache',
    'referer': 'https://open.spotify.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'spotify-app-version': '1.2.34.412.geaac6107',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}
        results = requests.get(url, headers=headers)
        try:
            return results.json()
        except Exception as e:
            "GET ACCESS TOKEN"
            return self.__get_lyrics__()
    @property
    def lyrics(self):
        if not self._lyrics:
            self._lyrics=self.__get_lyrics__()
        return self._lyrics
    def download(self,*,filepath:str|None=None,filename:str|None=None):
        # search song on youtube
        # TODO: Get closest duration then sort by views. get the one with the highest views
        name=self.name+', by '+self.first_artist.name
        results:list[pytube.YouTube] = pytube.Search(name).results
        def isInRange(n,target_number,padding):
            return n >= target_number-padding and n<=target_number+padding
        # get songs in range of 5% of spotify song length.
        # if there are none, sort by 3 closest to spotift song length
        sorted_by_length = list(filter(lambda result: result is not None and isInRange(result.length * 1000, self.track.duration, self.track.duration * 0.05), results))
        # print('\n\n\n',sorted_by_length,'\n\n\n')
        if not sorted_by_length:
            sorted_by_length=sorted(results,key=lambda x:abs(x.length*1000 - self.track.duration))
        # print([f'{s.video_id}:{s.views},{s.length}/{self.track.duration/1000}' for s in sorted_by_length])
        yt:pytube.YouTube = sorted(sorted_by_length[:3],key=lambda x:x.views)[::-1][0]
        yt.streams.get_audio_only().download(filepath or '',filename or name+'.mp3')  
        return yt.watch_url
if __name__ == '__main__':
    song_url = Search('30000 pounds of bananas live 1975').tracks[0].url
    print(song_url)
    print(Spotify(song_url).download())
    # data = Spotify(song_url).initial_data
    # print(data)
    # with open('spotify.json','w') as f:
    #     f.write(json.dumps(data,indent=4))