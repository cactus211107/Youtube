from pytube import *
import time,requests
import youtube_transcript_api

def get_captions_by_country_code(video:YouTube,country_code = 'en'):
    captions = video.captions
    for key in captions:
        print(key)
        if key.code[:2] == country_code:
            return key.json_captions['events']
def play_in_console(url,lang,keep_previous_lines = False):
    captions = get_captions_by_country_code(url,lang) # dont worry about this line, i already have a function for it
    last_start_ms = 0
    for caption in captions:
        ms_start_time = caption['tStartMs']
        wait_for = (ms_start_time-last_start_ms)/1000 # ÷1000 converts it to seconds
        time.sleep(wait_for) # wait till lyric prints
        print_text = ''
        for segment in caption['segs']: # makes a list of dicts into text (only does UTF-8 format)
            print_text+=segment['utf8']+' '
        print(print_text)
        if not keep_previous_lines:
            time.sleep(caption['dDurationMs']/1000)
            print("\033[F\033[K", end="") # this code clears the last printed line
        last_start_ms = ms_start_time # making it so it waits the correct amount of time
def get_transcript(id):
    try:
        return [{"start":caption['start'],"end":caption['start']+caption['duration'],"blocks":[{"offset":0,"text":caption['text']}]} for caption in youtube_transcript_api.YouTubeTranscriptApi.get_transcript(id,('en','fr','it','es'))]
    except:
        return[]
def get_word_timed_captions(video:YouTube):
    try:
        return video.captions.all()[0].json_captions['events'][1:]
    except:
        return []
def getCaptions(video:YouTube):return[{"start":caption['tStartMs']/1000,"end":(caption['tStartMs']+caption.get('dDurationMs',0))/1000,"blocks":[{'text':block['utf8'],'offset':block.get('tOffsetMs',0)/1000}for block in caption['segs']]}for caption in get_word_timed_captions(video)]
if __name__ == '__main__':
    print(get_transcript(YouTube('https://www.youtube.com/watch?v=uh29lzvpBAs')))

    # print(get_transcript('PGNiXGX2nLU'))
    # pprint.pprint(get_captions_by_country_code('en'))
    # print(get_captions_by_country_code('en')['events'])
            #'https://www.youtube.com/watch?v=PGNiXGX2nLU'
    # play_in_console('https://www.youtube.com/watch?v=PGNiXGX2nLU','en',True)