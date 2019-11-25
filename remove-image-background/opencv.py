import os
import platform
import cv2 as cv
import numpy as np
import urllib.request
import hashlib

import services

class OpenCV:

    def __init__(self):
        self.profile = cv.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_alt2.xml'))



    def findFaces(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = self.profile.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 1 or len(faces) == 0:
            print('more than one or zero found')
            return
        else:
            return faces



    def checkForFaces(self, href):
        resp = urllib.request.urlopen(href)
        img = np.asarray(bytearray(resp.read()), dtype='uint8')
        if img.shape[0] == 0:
            print('could not load image; may be blocked')
            return
        img = cv.imdecode(img, cv.IMREAD_COLOR)

        if img is None:
            return

        return self.findFaces(img)



    def saveCropped(self, filename, cropped):
        cv.imwrite('./remove-image-background/downloads/' + filename, cropped)
        return



    def createHash(self, name):
        file = name + ' profile'
#create hash from the file
        filename = hashlib.md5(file.encode()).hexdigest()
        filename = str(filename) + '.png'
        return filename



    def processDownloadedImage(self, name):
#remove.bg uses last part of pathname to name the images

        imgName = services.getLastImage()

        img = None
        img = cv.imread(imgName, cv.IMREAD_UNCHANGED)
        if img is None:
            print('image not found')
            return

        faces = self.findFaces(img)

#check again for amount of profice faces found...after removing BG, sometimes OpenCV doesn't find face again
        if faces is None:
            return

        for (x, y, w, h) in faces:
            y1 = int(y - h/2)
            if y1 < 0:
                y1 = 0
            y2 = int(y + h + h/2)
            x1 = int(x - w/2)
            if x1 < 0:
                x1 = 0
            x2 = int(x + w + w/2)

        try:
            cropped = img[y1:y2, x1:x2]

            filename = self.createHash(name)

            self.saveCropped(filename, cropped)
            return filename

        except Exception as e:
            print(e)
            return

