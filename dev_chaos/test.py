import logging
import sys

from base.ColorFormatter import ColorFormatter
from base.Browser import Browser

# Enable logging for base code
logger  = logging.getLogger( "base" )
console = logging.StreamHandler( sys.stderr )
logger.setLevel( logging.DEBUG )
console.setLevel( logging.DEBUG )
console.setFormatter( ColorFormatter( True ) )
logger.addHandler( console )

# Test browser
pages = [ "http://www.mirage-team.com/public/images/news/op545.jpg", 
		  "http://www.planet-libre.org/themes/planetlibre_repo/images/logo.png",
		  "http://www.jeuxvideo.com/pc.htm", 
		  "http://www.jeuxvideo.com/pc.htm", 
		  "http://www.jeuxvideo.com/pc.htm", 
		  "http://www.jeuxvideo.com/pc.htm", 
		  "http://www.jeuxvideo.com/ps3-playstation-3.htm",
		  "http://www.jeuxvideo.com/wii-nintendo-wii.htm" ]

browser = Browser()
browser.getFiles( pages )
browser.getFiles( pages )

# import logging
# import sys
# 
# from ColorFormatter import ColorFormatter
# from Navigateur import Navigateur
# 
# logger  = logging.getLogger( "pluzzdl" )
# console = logging.StreamHandler( sys.stdout )
# logger.setLevel( logging.DEBUG )
# console.setLevel( logging.DEBUG )
# console.setFormatter( ColorFormatter( True ) )
# logger.addHandler( console )
# 
# n = Navigateur()
# 
# pages = [ "http://www.mirage-team.com/public/images/news/op545.jpg", 
		  # "http://www.planet-libre.org/themes/planetlibre_repo/images/logo.png",
		  # "http://www.jeuxvideo.com/pc.htm", 
		  # "http://www.jeuxvideo.com/pc.htm", 
		  # "http://www.jeuxvideo.com/pc.htm", 
		  # "http://www.jeuxvideo.com/pc.htm", 
		  # "http://www.jeuxvideo.com/ps3-playstation-3.htm",
		  # "http://www.jeuxvideo.com/wii-nintendo-wii.htm" ]
# 
# print n.getFiles( pages )
# n.getFiles( pages )
# n.getFiles( pages )
# n.getFiles( [] )
# n.getFile( "http://www.publicsenat.fr/zp/templates/emission/JX_video.php", { "idP" : 108, "page" : 1 } )

# from base.Browser import Browser
# from base.ColorFormatter import ColorFormatter
# from base.Config import Config
# from base.Patterns import *

# b = Browser()
# c = Config()
# c2 = Config()
# print c == c2
