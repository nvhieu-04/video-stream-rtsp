import cv2
import threading
import time
import logging
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

logger = logging.getLogger(__name__)

thread = None

class Camera:
	def __init__(self,fps=30,video_source=0):
		self.fps = fps
		self.video_source = video_source
		# for ip camera use -
        # rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
		# rtsp://demo:demo@ipvmdemo.dyndns.org:5541/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast
		# rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4
        #localcamera
		# 0
		self.camera = cv2.VideoCapture('rtsp://bambi1:bambi12022@happyhouse2.ddns.net:8002/user=bambi1_password=bambi12022_channel=channel_number_stream=0.sdp')
		self.max_frames = 5*self.fps
		self.frames = []
		self.isrunning = False
	def run(self):
		global thread
		if thread is None:
			thread = threading.Thread(target=self._capture_loop,daemon=True)
			self.isrunning = True
			thread.start()
	
	def _capture_loop(self):
		dt = 1/self.fps
		while self.isrunning:
			v,im = self.camera.read()
			if v:
				if len(self.frames)==self.max_frames:
					self.frames = self.frames[1:]
				self.frames.append(im)
			time.sleep(dt)
	
	def stop(self):
		self.isrunning = False
	def get_frame(self, _bytes=True):
		if len(self.frames)>0:
			if _bytes:
				img = cv2.imencode('.png',self.frames[-1])[1].tobytes()
			else:
				img = self.frames[-1]
		else:
			with open("images/not_found.jpg","rb") as f:
				img = f.read()
		return img
		