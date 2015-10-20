# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import ntplib, datetime

hold = False

# Time
xx=ntplib.NTPClient()
t= datetime.datetime.utcfromtimestamp(xx.request('ntp.grnet.gr').tx_time)
d=datetime.datetime.now()-t

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="C:\Users\u\Downloads")
ap.add_argument("-a", "--min-area", type=int, default=1, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
#	camera = cv2.VideoCapture("video2.avi")	
	time.sleep(0.25)
# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
oldgray = None
gray = None

#cam 192.168.1.30 , 192.168.1.184

# Video Selection
ts=0.0001
vs=0
# Full Court=0, half court=1
if vs==0:
	#hsv boundaries
	hmn = 0
	hmx = 170
	smn = 0 #107
	smx = 170
	vmn = 50 #214
	vmx = 165
	# Gaussian mask dimensions
	gw=11
	gh=3
	# Threshold applied to differential image (frameDelta->thresh)
	fDt=8
	#v thresholds and dilate iterations for line exclusion
	vtmn,vtmx,dil=0, 146,5
	#dilate iterations, maximum width and height for player exclusion
	dip, mw, mh=25, 70, 60
	
elif vs==1:
	#hsv boundaries
	hmn = 0
	hmx = 70
	smn = 0 
	smx = 170
	vmn = 70 
	vmx = 200
	# Gaussian mask dimensions
	gw=3
	gh=11
	# Threshold applied to differential image (frameDelta->thresh)
	fDt=10
	#v thresholds and dilate iterations for line exclusion
	vtmn,vtmx,dil=0, 170,7
	#dilate iterations, maximum width and height for player exclusion
	dip, mw, mh=15, 70, 100

cv2.namedWindow('hue')
cv2.namedWindow('sat')
cv2.namedWindow('val')

def nothing(x):
    pass

# Creating track bar for min and max for hue, saturation and value
# You can adjust the defaults as you like
cv2.createTrackbar('hmin', 'hue',hmn,180,nothing)
cv2.createTrackbar('hmax', 'hue',hmx,180,nothing)
cv2.createTrackbar('smin', 'sat',smn,255,nothing)
cv2.createTrackbar('smax', 'sat',smx,255,nothing)
cv2.createTrackbar('vmin', 'val',vmn,255,nothing)
cv2.createTrackbar('vmax', 'val',vmx,255,nothing)

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied"
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		print grabbed
		break
	if gray != None:
		oldgray = gray
	# resize the frame, convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (gw, gh), 0)
	cv2.imshow("gray",gray)
	# image to hue	
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	hue,sat,val = cv2.split(hsv)
	# get info from track bar and appy to result
	hmn = cv2.getTrackbarPos('hmin','hue')
	hmx = cv2.getTrackbarPos('hmax','hue')
	smn = cv2.getTrackbarPos('smin','sat')
	smx = cv2.getTrackbarPos('smax','sat')
	vmn = cv2.getTrackbarPos('vmin','val')
	vmx = cv2.getTrackbarPos('vmax','val')
	
	hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
	sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
	vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))
	vthreshneg = cv2.inRange(np.array(val),vtmn,vtmx)
	vthreshneg = 255-vthreshneg
	vthreshneg  = cv2.dilate(vthreshneg , None, iterations=dil)
	vthreshneg = 255-vthreshneg
	#cv2.imshow("vthreshneg ",vthreshneg)
	# loop over the boundaries
	#cv2.imshow("hue", hthresh)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		oldgray = gray
		frameDelta = gray	
		#continue

	# Calculate ONLY positive differences to detect movement
	frameDelta[gray>oldgray]=1
	frameDelta[gray<=oldgray]=0
	frameDelta=frameDelta*(gray-oldgray)
	
	thresh = cv2.threshold(frameDelta, fDt, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image

	#yperthesi 
	tracking = cv2.bitwise_and(hthresh,thresh)
	tracking2 = cv2.bitwise_and(vthresh,vthreshneg)
	tracking = cv2.bitwise_and(tracking2 ,tracking)

	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("sat", sthresh)
	#cv2.imshow("val", vthresh)
	#cv2.imshow("Frame Delta", frameDelta)
	tracking=cv2.dilate(tracking , None, iterations=dip)
	
	(_, cnts, _) = cv2.findContours(tracking.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		if w<mw and h<mh:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			#print w,h
		text = "Occupied"
	# draw the text and timestamp on the frame
	'''cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, (datetime.datetime.now()+d-datetime.timedelta(0,0,0,0,0,3)).strftime("%H:%M:%S:%f %p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)'''
	cv2.imshow("Security Feed", frame)	
	#cv2.imshow("Last Frame",tracking)
	ct=(datetime.datetime.now()+d-datetime.timedelta(0,0,0,0,0,3))
	
	frame[6,0,0]=ct.microsecond/1000/256
	frame[7,0,0]=(ct.microsecond/1000)%256
	
	frame[0,0,0]=ct.year-2000
	frame[1,0,0]=ct.month
	frame[2,0,0]=ct.day
	frame[3,0,0]=ct.hour
	frame[4,0,0]=ct.minute
	frame[5,0,0]=ct.second
	
	#for xxx in range(0,8):
	#	print frame[xxx,0,0]
	#print ct.microsecond
	
	while hold:
		key = cv2.waitKey(1) & 0xFF
		if key == ord("n"):
			break
		elif key == ord("r"):
			hmn = cv2.getTrackbarPos('hmin','hue')
			hmx = cv2.getTrackbarPos('hmax','hue')
			smn = cv2.getTrackbarPos('smin','sat')
			smx = cv2.getTrackbarPos('smax','sat')
			vmn = cv2.getTrackbarPos('vmin','val')
			vmx = cv2.getTrackbarPos('vmax','val')
			hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
			sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
			vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))
			vthreshneg = cv2.inRange(np.array(val),vtmn,vtmx)
			vthreshneg = 255-vthreshneg
			vthreshneg  = cv2.dilate(vthreshneg , None, iterations=dil)
			vthreshneg = 255-vthreshneg
			cv2.imshow("vthreshneg ",vthreshneg)
			# loop over the boundaries
			cv2.imshow("hue", hthresh)
			# Calculate ONLY positive differences to detect movement
			frameDelta[gray>oldgray]=1
			frameDelta[gray<=oldgray]=0
			frameDelta=frameDelta*(gray-oldgray)
			thresh = cv2.threshold(frameDelta, fDt, 255, cv2.THRESH_BINARY)[1]
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			#yperthesi 
			tracking = cv2.bitwise_and(hthresh,thresh)
			tracking2 = cv2.bitwise_and(vthresh,vthreshneg)
			tracking = cv2.bitwise_and(tracking2 ,tracking)
			cv2.imshow("Thresh", thresh)
			cv2.imshow("sat", sthresh)
			cv2.imshow("val", vthresh)
			cv2.imshow("Frame Delta", frameDelta)
			tracking=cv2.dilate(tracking , None, iterations=dip)
			(_, cnts, _) = cv2.findContours(tracking.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			# loop over the contours
			for c in cnts:
				# if the contour is too small, ignore it
				# compute the bounding box for the contour, draw it on the frame,
				# and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				if w<mw and h<mh:
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					print w,h
				text = "Occupied"
			# draw the text and timestamp on the frame
			cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			cv2.putText(frame, (datetime.datetime.now()+d-datetime.timedelta(0,0,0,0,0,3)).strftime("%H:%M:%S:%f %p"),
				(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
			cv2.imshow("Security Feed", frame)	
			cv2.imshow("Last Frame",tracking)

		elif key == ord("t"):
			ts=0.05
	time.sleep(ts)		
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
	#print ts 
	#print datetime.datetime.now()+d-datetime.timedelta(0,0,0,0,0,3)
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()