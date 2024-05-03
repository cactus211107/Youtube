import random,os
from pytube import *



from moviepy.editor import VideoFileClip, AudioFileClip, clips_array
import moviepy.video.io.ffmpeg_tools as ffmepg


def combine_video_audio(video_path, audio_path, output_path):
    ffmepg.ffmpeg_merge_video_audio(video_path,audio_path,output_path)
    # video_clip = VideoFileClip(video_path)
    # audio_clip = AudioFileClip(audio_path)

    # video_with_audio = video_clip.set_audio(audio_clip)
    # video_with_audio.write_videofile(output_path, codec=vc, audio_codec="libx264",threads=8,preset='ultrafast')




def download_video(video:YouTube,path:str,stream_id:int,filename:str|None=None):video.streams.get_by_itag(stream_id).download(path,filename)
def get_resolutions(video:YouTube):return video.streams.filter().order_by('resolution')
def get_progressive_resolutions(video:YouTube): # full video
    return video.streams.filter(progressive=True).order_by('resolution')
def get_adaptive_resolutions(video:YouTube): # no audio. audio seperate
    return get_resolutions(video).filter(progressive=False,only_audio=False)
def download_adaptive_video(video:YouTube,path:str,stream_id:int,filename:str|None=None):
    if video.age_restricted:
        video.bypass_age_gate()
    audio = video.streams.filter(only_audio=True, adaptive=True).last()
    video_at_res = video.streams.get_by_itag(stream_id)
    # video_codec=video_at_res.video_codec
    title = video.title
    if filename:
        title=filename
    if not video_at_res:return
    if not audio:return
    temp_id = str(random.randint(0,10934))
    video_name = temp_id+'__video.webm'
    audio_name = temp_id+'__audio.webm'
    vid_folder = 'temp'
    audio_folder = 'temp'
    vid_path = os.path.join(vid_folder,video_name)
    audio_path = os.path.join(audio_folder,audio_name)
    print('DOWNLOADING VIDEO',video_at_res)
    video_at_res.download(vid_folder,video_name)
    print('DOWNLOADING AUDIO',audio)
    audio.download(audio_folder,audio_name)
    print('SAVED VIDEO AT',vid_folder,'AND AUDIO AT',audio_folder)
    # combine audio and video
    os.makedirs(path,exist_ok=True)
    combine_video_audio(vid_path,audio_path,os.path.join(path,title+'.mp4'))
    print('remoing',vid_path)
    os.remove(vid_path)
    os.remove(audio_path)
def getResolutionsAsDict(resolutions):return [{"id":res.itag,"display":res.resolution+str(res.fps)+('' if res.is_progressive else " (Adaptive)"),"resolution":res.resolution,"fps":res.fps,"progressive":bool(res.is_progressive)} for res in resolutions]
def get_highest_res(video:YouTube):return video.streams.get_highest_resolution()
def get_id_from_url(url:str):return YouTube(url).video_id
if __name__ == '__main__':
    URL = 'https://www.youtube.com/watch?v=WTOm65IZneg'
    URL = 'https://www.youtube.com/watch?v=grQtbKJHNhc'
    video = YouTube(URL)
    RES = getResolutionsAsDict(get_adaptive_resolutions(video))
    print(RES)
    # download_adaptive_video(YouTube(URL),'ok',RES.itag)
    # print(RES.resolution)
    # download_adaptive_video(URL,RES,'/Desktop')
    YouTube('url').comments