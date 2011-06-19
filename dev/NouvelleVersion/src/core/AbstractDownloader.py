
class AbstractDownloader (DownloaderInterface) :
	def __init__(self) :
		pass
	def read (self, n) :
		# returns byte[]
		pass
	def canDownload (self, url) :
		# returns bool
		pass

