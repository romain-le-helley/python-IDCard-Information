import sys
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\romain\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"


def main(file):
    img = cv2.imread(file)
    height, width = img.shape[:2]
    img = cv2.resize(img, (2*width, 2*height))

    ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 254, 255, cv2.THRESH_BINARY_INV)

    word = pytesseract.image_to_string(img)

    if not word:
        print("Not a word")
        sys.exit(84)
    word = word.split('\n')

    #Nom
    nom = word[-2].split('<<')
    nom = nom[0][5:].replace('<', ' ')

    #Prenom
    prenom = word[-1].split('<<')[0]
    prenom = ''.join([i for i in prenom if not i.isdigit()])

    #Date
    date = word[-1].split('<<')[-1].replace('<', '')
    date = ''.join([i for i in date if i.isdigit()])
    date = date[:6]
    naissance = list()
    naissance.append(date[:2])
    naissance.append(date[2:4])
    naissance.append(date[4:6])
    return [nom, prenom, naissance]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

'''
img = cv2.imread(sys.argv[1])
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#[   0          1           2           3           4          5         6       7       8        9        10       11 ]
#['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text']
boxes = pytesseract.image_to_data(img)
for a,b in enumerate(boxes.splitlines()):
        print(b)
        if a!=0:
            b = b.split()
            if len(b)==12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.putText(img,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
                cv2.rectangle(img, (x,y), (x+w, y+h), (50, 50, 255), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
'''
'''
def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5,5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=4)
    imgEraded = cv2.erode(imgDialation, kernel, iterations=1)
    return imgEraded

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = np.array([])
    maxArea = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 10)
    return biggest

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

def getWarp(img, biggest):
    biggest = reorder(biggest)
    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    return imgOutput
'''
'''
cv2.imshow("warp", img)


cv2.imshow("warp222", img)
'''

'''
imgContour = img.copy()
imgThres = preProcess(img)
biggest = getContours(imgThres)
if biggest.size == 0:
    sys.exit(84)
imgWarp = getWarp(img, biggest)


imgWarp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
'''

'''
ret, imgWarp = cv2.threshold(imgWarp, 100, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("warp", imgWarp)
ret, imgWarp = cv2.threshold(imgWarp, 10, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("warp222", imgWarp)

word = pytesseract.image_to_string(imgWarp)
'''
'''
for x, y in enumerate(word.splitlines()):
    if y and not y.isspace() and y != 't':
        print(y)
cv2.waitKey(0)
'''