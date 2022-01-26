import paho.mqtt.publish as publish
import cv2
from time import sleep
import numpy as np
from datetime import datetime
import os
from array import array

# some comment added #
MissingObj = 0
UnattendedObj = 0

channelID = "572070"

apiKey = "0VSBARDTO364U1BK"

useUnsecuredTCP = False

useUnsecuredWebsockets = False

useSSLWebsockets = True

mqttHost = "mqtt.thingspeak.com"

Original = cv2.imread("Original.png")
Original = cv2.medianBlur(Original, 5)
Original2 = cv2.imread("Original.png")

cap = cv2.VideoCapture(0)

ret,Edited=cap.read()
cap.release()
cv2.imwrite('Edited.png',Edited)

Edited= cv2.imread('Edited.png')
Edited = cv2.medianBlur(Edited, 5)
Edited2= cv2.imread('Edited.png')

print Original2.shape, Original2.dtype
print Edited2.shape, Edited2.dtype

diffadd = cv2.subtract(Edited2, Original2)
diffsub = cv2.subtract(Original2, Edited2)
cv2.imwrite('diffsub.png', diffsub)
cv2.imwrite('diffadd.png', diffadd)

## grayscale images
imgraysub = cv2.cvtColor(diffsub,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgraysub,39,255,0)
cv2.imwrite("threshsub.png",thresh)
imgrayadd = cv2.cvtColor(diffadd,cv2.COLOR_BGR2GRAY)
ret,thresha = cv2.threshold(imgrayadd,39,255,0)
cv2.imwrite("threshadd.png",thresha)
cv2.imwrite('diffsubgray.png', diffsub)
cv2.imwrite('diffaddgray.png', diffadd)

#contours for missing objects
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(c) for c in contours]

try:
        max_index = np.argmax(areas)
except ValueError:
        pass

cnt=contours[max_index]
len(contours)
len(cnt)
cv2.imwrite('321.png', thresh)
moments = cv2.moments(cnt)
M = moments
centroid_x = int(M['m10']/M['m00'])
centroid_y = int(M['m01']/M['m00'])
x,y,w,h = cv2.boundingRect(cnt)
orig2=cv2.rectangle(Original2,(x,y),(x+w,y+h),(0,0,255),0)
print cv2.contourArea(cnt)
font = cv2.FONT_HERSHEY_SIMPLEX
area = cv2.contourArea(cnt)

try:
        if area>500:
                import ssl
                tTransport = "websockets"
                tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
                tPort = 443
                topic = "channels/" + channelID + "/publish/" + apiKey
                while(True):
                        MissingObj +=1
                        print MissingObj
                        print ("Missing Object Detected")
                        tPayload = "field1=" + str(MissingObj)
                        try:
                                publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
                        except (KeyboardInterrupt):
                                break
                        except:
                                print ("There was an error while publishing the data.")
                        if MissingObj == 10:
                                break
except ValueError:
        pass

#contours for new object
contours,hierarchy = cv2.findContours(thresha,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
areas1 = [cv2.contourArea(c1) for c1 in contours]

try:
        max_index1 = np.argmax(areas1)
except ValueError:
        pass


cnt2=contours[max_index1]
len(contours)
len(cnt2)
cv2.imwrite('123.png', thresha)
moments = cv2.moments(cnt2)
M2 = moments
centroid_x2 = int(M2['m10']/M2['m00'])
centroid_y2 = int(M2['m01']/M2['m00'])
x2,y2,w2,h2 = cv2.boundingRect(cnt2)
orig3=cv2.rectangle(Edited2,(x2,y2),(x2+w2,y2+h2),(0,0,255),1)
print cv2.contourArea(cnt2)
font = cv2.FONT_HERSHEY_SIMPLEX
area1 = cv2.contourArea(cnt2)
try:
        if area1>500:
                import ssl
                tTransport = "websockets"
                tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
                tPort = 443
                topic = "channels/" + channelID + "/publish/" + apiKey
                while(True):
                        UnattendedObj +=1
                        print UnattendedObj
                        print ("Unattended Object Detected")
                        tPayload = "field2=" + str(MissingObj)
                        try:
                                publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
                        except (KeyboardInterrupt):
                                break
                        except:
                                print ("There was an error while publishing the data.")
                        if UnattendedObj == 10:
                                break
except ValueError:
        pass
