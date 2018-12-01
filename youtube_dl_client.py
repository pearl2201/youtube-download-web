from __future__ import unicode_literals
import youtube_dl
import json

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'ext': 'mp4',
    'format':'bestvideo'
 
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ret = ydl.extract_info('https://www.youtube.com/watch?v=BaW_jenozKc',download=False,process=True)
    print (ret)
    with open('result.txt','w') as f:
        f.write(json.dumps(ret,indent=4, sort_keys=True))
        f.close()