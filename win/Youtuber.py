from pytube import YouTube as yt
import sys


class YTD:
   
   
    def __init__(self,url):
       
        self.video = yt(
            url,
               )
        self.stream = self.video.streams
        
    def available_res_video(self):
        
        dic_tags = {}
        filtered_stream = self.stream.filter(
            file_extension = 'mp4',
            )
        
        for stream in filtered_stream:
            dic_tags[stream.resolution] = stream.itag
        return dic_tags

    def available_res_audio(self):

        dic_tags = {}
        filtered_stream = self.stream.filter(
            file_extension='mp4',
            only_audio = True,
            progressive = False
        )

        for stream in filtered_stream:
            dic_tags[stream.resolution] = stream.itag
        return dic_tags
        
    def check_res_video(self, resolution):

        dic_tags = self.available_res_video()
        tags = dic_tags.keys()
        if resolution in tags:
            return dic_tags[resolution]

    def check_res_audio(self):

        dic_tags = self.available_res_audio()
        tags = dic_tags.values()
        return max(tags)

    def file_size(self):
        return self.set_res.filesize

    def video_download(self, resolution, *args):

        tag = self.check_res_video(resolution)

        self.set_res = self.stream.get_by_itag(tag)
        self.set_res.download()

    def audio_download(self, *args):

        tag = self.check_res_audio()

        self.set_res = self.stream.get_by_itag(tag)

        self.set_res.download()

    def get_title(self):
        return self.video.title

    def get_thumb(self):
        return self.video.thumbnail_url
