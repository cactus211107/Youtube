def convert_json_to_vtt(json:list):
    content = 'WEBVTT'
    print(enumerate(json))
    for i,caption in enumerate(json):
        print(i,caption)
        start = caption['start']
        print(1)
        end=caption['start']+caption['duration']
        print(2)
        text=caption['text']
        print(3)
        content+=f"\n\n{i}\n{int_to_time(start)} --> {int_to_time(end)}\n{text}"
        print(4)
    print('CONTENT',content)
    return content
def pad_zeros(n):
    return str(n).rjust(2,'0')
def int_to_time(n):
    hours = int(n/3600)
    n-=hours*3600
    minutes=int(n/60)
    n-=minutes*60
    int_n=int(n)
    return f"{pad_zeros(hours)}:{pad_zeros(minutes)}:{pad_zeros(int_n)}.{str(round(n-int_n,3))[2:].ljust(3,'0')}"