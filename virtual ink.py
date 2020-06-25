import cv2
import numpy as np
from caliberation import Caliberation
if __name__ == "__main__":
	c=input("Press Enter to Caliberate marker: ")	
	Lower,Upper=Caliberation()
	c=input("\n\nPress Enter to start................... ")	
	vc = cv2.VideoCapture(0)
	x0,y0=-1,-1
	#color=(0,132,255)#Default - Orange
	color=(204,51,255)#Pink
	temp=np.full(shape=(480,640,3),fill_value=(0,0,0),dtype=np.uint8)
	while cv2.waitKey(1)==-1:
		return_value,frame = vc.read()
		frame=cv2.flip(frame,1)
		hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		mask=cv2.inRange(hsv,np.array(Lower),np.array(Upper))
		kernel=np.ones((5,5),np.uint8)
		erosion=cv2.erode(mask,kernel,iterations=1)
		frame=np.array(frame)
		contours,hierarchy=cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		if contours:	
			c = max(contours, key = cv2.contourArea)
			x,y,W,H = cv2.boundingRect(c)
			if x0==-1:
				x0,y0=x+W//2,y+H//2
			else:
				cv2.line(temp,(x0,y0),(x+W//2,y+H//2),color,5)
				x0,y0=x+W//2,y+H//2
		else:
			x0,y0=-1,-1	
		mask=cv2.cvtColor(temp,cv2.COLOR_BGR2HSV)
		mask=cv2.inRange(mask,np.array([1,1,1]),np.array([255,255,255]))
		temp=cv2.bitwise_and(temp,temp,mask=mask)
		mask=cv2.bitwise_not(mask)
		frame=cv2.bitwise_and(frame,frame,mask=mask)
		frame=cv2.add(frame,temp)
		cv2.imshow('Frame',cv2.resize(frame,(1280,720)))		
	vc.release()
	cv2.destroyAllWindows()

	


