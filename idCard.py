import sys
import os
import cv2
import pytesseract
import numpy as np
from wand.image import Image as wi

pytesseract.pytesseract.tesseract_cmd = "tesseract.exe"

widthImg = 1200
heightImg = 920

def getWarp(img, square):
    pt1 = np.float32(square)
    pt2 = np.float32([[0, 0], [590, 0], [0, 100], [590, 100]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgOutput = cv2.warpPerspective(img, matrix, (590, 100))
    return imgOutput

def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5,5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=4)
    imgEraded = cv2.erode(imgDialation, kernel, iterations=1)
    return imgEraded

def reorder(pts):
    pts = pts.reshape((4,2))
    newPts = np.zeros((4,1,2), np.int32)
    adding = pts.sum(1)
    diffPts = np.diff(pts, axis=1)
    newPts[0] = pts[np.argmin(adding)]
    newPts[1] = pts[np.argmin(diffPts)]
    newPts[2] = pts[np.argmax(diffPts)]
    newPts[3] = pts[np.argmax(adding)]
    return newPts

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = np.array([])
    maxPeri = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if (peri > maxPeri):
                biggest = approx
                maxPeri = peri
    for l,i in enumerate(biggest):
        for y in i:
            if (y[0] > 900 or y[1] > 900):
                y[0] = 0
                y[1] = 0
    x,y,w,h = cv2.boundingRect(biggest)
    cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.drawContours(imgContour, [biggest], -1, (255, 0, 0), 6)
    return [x, y, w, h]

def getWarp(img, biggest):
    biggest = reorder(biggest)
    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    return imgOutput

def main(file):
    filename = file
    if file[-4:] == ".pdf":
        PDFfile = wi(filename=file, resolution=400)
        Images = PDFfile.convert('jpg')
        ImageSequence = 1
        for img in PDFfile.sequence:
            Image = wi(image = img)
            Image.save(filename=file[:-3] + "jpg")
            ImageSequence += 1
        filename = file[:-3] + "jpg"

    img = cv2.imread(filename)
    if file[-4:] == ".pdf":
        #only if pdf
        height, width = img.shape[:2]
        height = height // 2
        width = width // 2
        img = cv2.resize(img, (width, height))
        os.remove(file)
        #end here

    #height, width = img.shape[:2]
    #height = height // 2
    #width = width // 2
    #img = cv2.resize(img, (width, height))
    imgContour = img.copy()

    imgThres = preProcess(img)
    biggest = getContours(imgThres, imgContour)
    cv2.imshow("contour", imgContour)

    imgCropped = img[biggest[1]:biggest[1]+biggest[3], biggest[0]:biggest[0]+biggest[2]]
    cv2.imshow("lol", imgCropped)
    height, width = imgCropped.shape[:2]
    imgSize = cv2.resize(imgCropped, (width * 2, height * 2))
    cv2.imshow("size", imgSize)

    #imgWarp = getWarp(img, biggest)

    #cv2.imshow('normal', img)
    #ret, imgCropped = cv2.threshold(imgCropped, 120, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow('black', imgCropped)
    #imgCropped = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('more black', imgCropped)
    #ret, imgCropped = cv2.threshold(imgCropped, 254, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow('white', imgCropped)

    #warp = getWarp(img, [[13, 314], [600, 314], [15, 413], [600, 413]])

    #word = pytesseract.image_to_string(warp)
    #cv2.imshow('warp', warp)

    cv2.waitKey(0)
    allWord = pytesseract.image_to_string(imgSize)
    if not allWord:
        print("Not a word")
        sys.exit(84)
    allWord = allWord.replace(' ', '')
    allWord = allWord.split('\n')

    lastword = 0
    print(allWord)
    word = []
    for line in allWord:
        if lastword == 2:
            break
        if lastword == 1 or line[:5] == "IDFRA":
            lastword += 1
            word.append(line)

    print(word)
    #Nom
    nom = word[0].split('<<')
    nom = nom[0][5:].replace('<', ' ')

    #Prenom
    prenom = word[1].split('<')[0]
    for num, letter in enumerate(prenom):
        if letter.isalpha():
            prenom = prenom[num:]
            break

    #Date
    date = word[1].split('<')[-1].replace('<', '')
    date = ''.join([i for i in date if i.isdigit()])
    date = date[:6]
    naissance = list()
    naissance.append(date[:2])
    naissance.append(date[2:4])
    naissance.append(date[4:6])
    return [nom, prenom, naissance]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))