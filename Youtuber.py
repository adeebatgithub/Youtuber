from pytube import YouTube as yt
#from pytube.cli import on_progress
import sys


class YTD:
   
   
    def __init__(self,url,res,aud):
       
        self.video = yt(
            url,
            on_progress_callback = self.on_progress
               )
        self.stream = self.video.streams
        self.res = res
        self.aud = aud
        self.file = 'video'
        
    def check_res(self):
        
        self.tags = {}
        if self.aud == True:
            self.pro = False
        else:
            self.pro = True
        filtered_stream = self.stream.filter(
            file_extension = 'mp4',
            only_audio = self.aud,
            progressive = self.pro
            )
        
        for stream in filtered_stream:
            if self.aud == False:
                self.tags[stream.resolution] = stream.itag
            elif self.aud == True:
                self.tags[stream.abr] = stream.itag
            
        if self.res in self.tags.keys():
            
            return self.tags[self.res]
            
        
        if self.aud == True:
            self.file = 'audio'
            return(
                self.tags[max(self.tags)])
            
    def display_progress_bar(self,
        bytes_received,filesize,
        ch: str = "█", scale: float = 0.55):
        
        columns = 35
        max_width = int(columns * scale)
        
        filled = int(round(max_width * bytes_received / float(filesize)))
        remaining = max_width - filled
        progress_bar = ch * filled + " " * remaining
        percent = round(100.0 * bytes_received / float(filesize), 1)
        text = f" downloading: |{progress_bar}| {percent}% | {round((bytes_received/1024)/1024,2)} MiB\t\r"
        sys.stdout.write(text)
        sys.stdout.flush()
        #print(text)
        
            
    def on_progress(
        self,stream,chunk,bytes_remaining
        ):
        
        self.file_size = self.set_res.filesize
        
        bytes_received = self.file_size - bytes_remaining
        self.display_progress_bar(
            bytes_received, self.file_size)
        
    def download(self):
        
        tag = self.check_res()
        self.set_res = self.stream.get_by_itag(tag)
        
        print(" ")
        print("-"*56)
        print(f" [+] {self.file} :  {self.video.title}")
        print("-"*56)
        print("")
        
        self.set_res.download(
            '/storage/emulated/0/Youtuber'
            )
        
        print("\n")
        print(" [*] download to : Youtuber")

    
if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        
        url = sys.argv[1]
        res = sys.argv[2]
        aud = False
        if "-aud" in sys.argv:
            aud = True
        
        obj = YTD(url,res,aud)
        obj.download()