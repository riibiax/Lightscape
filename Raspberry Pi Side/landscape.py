#!/usr/bin/python          
import time, socket, flickrapi, opc, io, os, random, sys, dpyinfo
#import easydriver as ed
import urllib2 as urllib
from traceback import format_exception
from PIL import Image
from xml.dom import minidom
from threading import Thread
from importer import ImportPlugins
from opc.matrix import OPCMatrix
from opc.error import TtyTooSmall
try:
    import json
except ImportError:
    import simplejson as json

FLIPTIME = 30

matrix = None

import logging; logging.basicConfig(filename='errors.log', level=logging.DEBUG)

#yahoo api
WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w='

#flickr api
api_key ="7cf1a32b029967579424cdf6afc6b104"

#arrays to stock cities' data
woeidCities= []
cities = []
meteo=[]
meteoText=[]
windSpeed=[]
windDirection=[]

address=0


class mainThread(Thread):
	def __init__(self):
		Thread.__init__(self)
 
	def run(self):
		global address
		#socket
		#s = socket.socket()         # Create a socket object
		#host = socket.gethostname() # Get local machine name
		#port = 12345                # Reserve a port for your service.
		#s.bind((host, port))        # Bind to the port
		#socket listening to
		#s.listen(5)                 # Now wait for client connection.
		#while True:
			#c, addr = s.accept()     # Establish connection with client.
			#print 'Got connection from', addr
			#if addr != address:
			#	resetValues()
			#	addr=address
			#string=s.recv(1024)
			#confirm
			#c.send('1\n')
		#string= "37.37,-122.04,2502265\n"
		string= "718345,754542,1118370,724196,783058,2487956,468739,784201,782538\n"
		#delete end character
		string.rstrip('\n')
		#split received data
		#lat, lon, woeid= string.split(",")
		woeidCities= string.split(",")
		#if this woeid hasn't already been added..
		#if woeid not in woeidCities:
		while True:
			for idx, woeid in enumerate(woeidCities):
				#woeidCities.append(woeid)
				#loc=lat+","+lon
				try:
					setValues(woeid)
				except:
					pass
				pictureUrl=findPictures(idx)
				pixels= render(pictureUrl)
				stepperMotor(idx)
				sendPixels(pixels)
				#c.close()                # Close the connection


class updateThread(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		while True:
			mins=0
			while mins!=30:
				time.sleep(30)
				mins+=1
			#update meteo value
			updateValues()

###exceptionHandler##################################################
def exceptionHandler(etype, evalue, etraceback):
    global matrix
    if matrix is not None:
        matrix.terminate()

    for line in format_exception(etype, evalue, etraceback):
        logging.error('Exception: '+line.rstrip('\n'))

###setValues##################################################
def setValues(woeid):
	url=WEATHER_URL + woeid
	dom=minidom.parse(urllib.urlopen(url))
	location = dom.getElementsByTagName('yweather:location')
	cities.append(location[0].getAttribute('city'))
	condition=dom.getElementsByTagName('yweather:condition')
	meteo.append(condition[0].getAttribute('code'))
	meteoText.append(condition[0].getAttribute('text'))
	wind=dom.getElementsByTagName('yweather:wind')
	windSpeed.append(wind[0].getAttribute('speed'))
	windDirection.append(wind[0].getAttribute('direction'))

###resetValues##################################################
def resetValues():
	woeidCities= []
	cities = []
	meteo=[]
	meteoText=[]
	windSpeed=[]
	windDirection=[]

###updateValues##################################################
def updateValues():
	for idx, city in enumerate(woeidCities):
		url=WEATHER_URL + city
		dom=minidom.parse(urllib.urlopen(url))
		condition=dom.getElementsByTagName('yweather:condition')
		meteo[idx]=condition[0].getAttribute('code')
		meteoText[idx]=condition[0].getAttribute('text')
		wind=dom.getElementsByTagName('yweather:wind')
		windSpeed[idx]=wind[0].getAttribute('speed')
		windDirection[idx]=wind[0].getAttribute('direction')

###findpictures##################################################
def findPictures(idx):
	flickr = flickrapi.FlickrAPI(api_key)
	url=""
	try:
		args = gen_arguments(idx)
		photos = flickr.walk(**args)
		for photo in photos:
			url_test= create_url(photo)
			if url_test!=0 or url_test!="":
				url=url_test
			break
	except:
		pass
	else:
		if url!="":
			return url
	try:
		args = gen_arguments_bis(idx)
		photos = flickr.walk(**args)
		for photo in photos:
			url_test= create_url(photo)
			if url_test!=0 or url_test!="":
				url=url_test
			break
	except:
		pass
	else:
		if url!="":
			return url
	try:
		args = gen_arguments_tris(idx)
		photos = flickr.walk(**args)
		for photo in photos:
			url_test= create_url(photo)
			if url_test!=0 or url_test!="":
				url=url_test
			break
	except:
		pass
	else:
		if url!="":
			return url
	return 0

###create_url#####################################################
def create_url(photo):
	owner = photo.get('owner')
	photo_id = photo.get('id')
	farm= photo.get('farm')
	ser= photo.get('server')
	secret = photo.get('secret')
	if owner !="" and photo_id !="" and farm!="" and ser!="" and secret!="":
		picture_url = "https://farm"+farm+".staticflickr.com/"+ser+"/"+photo_id+"_"+secret+".jpg"
		return picture_url
	return 0

###gen_arguments#####################################################
def gen_arguments(id):
	searchedText= cities[id]+" landscape " + meteoText[id]
	per_page=5
	print searchedText
	arguments = {"tag_mode": "all", "text": searchedText, "per_page": per_page}
	return arguments

###gen_arguments_bis#####################################################
def gen_arguments_bis(id):
	searchedText= cities[id]+" landscape"
	per_page=5
	print searchedText
	arguments = {"tag_mode": "all", "text": searchedText, "per_page": per_page}
	return arguments

###gen_arguments_tris#####################################################
def gen_arguments_tris(id):
	searchedText= cities[id]
	per_page=5
	print searchedText
	arguments = {"tag_mode": "all", "text": searchedText, "per_page": per_page}
	return arguments

###render##################################################
def render(pic):
	print pic
	if pic!=0:
		fd = urllib.urlopen(pic)
		image_file = io.BytesIO(fd.read())
		return imageRender(image_file)
	else:
		return standardRender()

###imageRender#####################################################
def imageRender(fileImage):
	size = (59, 8) 
	im = Image.open(fileImage)
	im = im.resize(size, Image.ANTIALIAS)
	i = 0
	j = 0
	MatrixPix = [[0 for x in xrange(59)] for x in xrange(8)] 
	while j <= 7:
		while i <= 58:
			MatrixPix[j][i]=im.getpixel((i,j))[:3] # Only want RGB, not RGBA
			i+=1
		j+=1
		i = 0
	return MatrixPix

###standardRender#####################################################
def standardRender():
	pix=[255,255,255];
	return pix

###sendPixels#####################################################
def sendPixels(pix):
	#LED PART
	global matrix
	#expections
	sys.excepthook = exceptionHandler
	#setting matrix using dpyinfo file
	matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT, dpyinfo.ADDRESS, dpyinfo.ZIGZAG)
	#load a template. Write sudo python art.py nameTemplate.py
	arts = ImportPlugins("art", ["template2.py"], sys.argv[1:], matrix)
	if len(arts) == 0:
		logging.error("Couldn't find any art to execute")
		exit(1)
	t = time.time()
	while time.time()-t < FLIPTIME:
		random.seed(time.time())
		for art in arts:
			matrix.setFirmwareConfig()
			art.start(matrix, pix)
        	while time.time()-t < FLIPTIME/len(arts):
        		art.refresh(matrix)
        		matrix.show()
        		time.sleep(art.interval()/1000.0)

###stepperMotor##################################################
def stepperMotor(idx):
	cw = True
	ccw = False
	# Create an instance of the easydriver class.
	# Not using sleep, enable or reset in this example.
#	stepper = ed.easydriver(18, 0.004, 23, 24, 17, 25)
	# Set motor direction to clockwise.
	#if windDirection[idx]>180:
	#	stepper.set_direction(cw)
	#else:
	#	stepper.set_direction(ccw)
	# Set the motor to run in 1/8 of a step per pulse.
#	stepper.set_eighth_step()
	# Do some steps.
#	for i in range(0,100):
#		stepper.step()
	# Clean up (just calls GPIO.cleanup() function.)
#	stepper.finish()


if __name__ == '__main__':
	mThread = mainThread()
	#update values thread
 	uThread = updateThread()
	# Start running the threads!
	mThread.start()
	uThread.start()
	# Wait for the threads to finish...
	mThread.join()
	uThread.join()