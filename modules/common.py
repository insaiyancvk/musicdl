import os, urllib.request, re, subprocess, sys, pafy
from rich.console import Console
from youtube_title_parse import get_artist_title 
from urllib.parse import quote

class common():
    
    def __init__(self, ffmpeg, spo=False):
        self.ffmpeg = ffmpeg
        self.spo = spo

    def get_url(self,s):
        """
        Give a video ID as an argument to this function. It returns top n (7 by default) video URLs.
        """

        query = "https://www.youtube.com/results?search_query="+quote(s)
        baseurl = "https://www.youtube.com/watch?v="
        response = urllib.request.urlopen(query)
        html = response.read()
        video_ids = re.findall(r"watch\?v=(\S{11})", html.decode())
        urls = []
        if self.spo:
            for i in video_ids:
                try:
                    pafy.new(baseurl+i)
                    urls.append(baseurl+i)
                    return urls
                except:
                    continue
        else:
            j = 0
            for i in video_ids:
                try:
                    pafy.new(baseurl+i)
                    urls.append(baseurl+i)
                    j+=1
                    if j==7:
                        break
                except:
                    continue
            return urls

    def convert(self, old, new, alburl, flac=False):
        """ converts any file format to .mp3 or flac with the help of ffmpeg """
        
        if self.spo:
            if not flac:
                subprocess.call(['ffmpeg','-hide_banner','-loglevel', 'quiet','-i',old,'-b:a', '320k','w'+new])
                os.remove(old)
                urllib.request.urlretrieve(alburl, "thumb.png")
                print("Adding album art")
                subprocess.call(['ffmpeg','-hide_banner','-loglevel','quiet','-i','w'+new,'-i','thumb.png','-map','0:0','-map','1:0','-codec','copy','-id3v2_version','3','-metadata:s:v','title="Album cover"','-metadata:s:v','comment="Cover (front)"',new])
                os.remove("w"+new)
                os.remove("thumb.png")
            elif flac:
                subprocess.call(['ffmpeg','-hide_banner','-loglevel', 'quiet','-i',old,'-c:a', 'flac','w'+new])
                os.remove(old)
                urllib.request.urlretrieve(alburl, "thumb.png")
                print("Adding album art")
                subprocess.call(['ffmpeg','-hide_banner','-loglevel','quiet','-i','w'+new, '-i','thumb.png','-sample_fmt', 's32', '-ar', '48000', '-disposition:v', 'attached_pic', '-vsync', '0', new])
                os.remove("w"+new)
                os.remove("thumb.png")
            
        else:
            if not flac:
                subprocess.call(["ffmpeg",'-hide_banner','-loglevel','quiet','-i',old,'-b:a', '320k',new])
            elif flac:
                subprocess.call(["ffmpeg",'-hide_banner','-loglevel','quiet','-i',old,'-c:a', 'flac',new])
            os.remove(old)

    # Download the song
    def download_song(self,url, albart, sponame, z): 
        """
        Download the song by passing the video URL as a parameter
        """

        try:
            v = pafy.new(url)
        except Exception as e:
            print(f"\nSome error occurred while fetching the details of the song : {e}\n")
            return
        name = v.title
        audio = v.getbestaudio()
        Console().print(f"\n[bold green]Downloading {name}[/bold green]")
        audio.download()
        dirs = os.listdir()
        try:

            if self.spo:
                artist, title = get_artist_title(sponame)   
            else:
                artist, title = get_artist_title(name)

            for i in dirs:
                if sys.platform=='win32' or os.name=='nt':
                    if name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_") in i:                    
                        
                        if z == "1" or z == "flac" or z == "f":
                            track_name = title+" - "+artist+".flac"
                            track_name = track_name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_")
                            print(f"Converting the audio format to flac")
                            self.convert(i, track_name, albart, flac=True)

                        else:
                            track_name = title+" - "+artist+".mp3"
                            track_name = track_name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_")
                            print(f"Converting the audio format to mp3")
                            self.convert(i, track_name, albart)

            for i in os.listdir():
                if "_" in i:
                    try:
                        os.rename(i,i.replace("_"," "))
                    except FileExistsError:
                        try:
                            os.rename(i,i.replace("_","  "))
                        except FileExistsError:
                            pass
        except TypeError:
            for i in dirs:
                if name in i:
                    ind1 = len(i) - 1 - i[::-1].index('.')
                    ext = i[ind1:]
                    if ext in i:

                        if z == "1" or z == "flac" or z == "f":
                            track_name = name[:ind1]+".flac"
                            print(f"Converting the audio format to flac")
                            self.convert(i, track_name, albart, flac=True)

                        else:
                            track_name = name[:ind1]+".mp3"
                            print(f"Converting the audio format to mp3")
                            self.convert(i, track_name, albart)

            for i in os.listdir():
                if "_" in i:
                    os.rename(i,i.replace("_"," "))