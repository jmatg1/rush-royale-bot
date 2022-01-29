import os
import time
from PIL import Image
from tkinter import Tk, Button, Text, END
from tkinter import ttk
import re
import threading
from subprocess import check_output
from datetime import datetime

tkWindow = Tk()
tkWindow.geometry('400x250')
tkWindow.title('Rush Royale Bot By Jmatg1')


class Bot:
    work = 1
    screenshot = 0
    screenshotName = ''
    t1 = 0
    fight = 1
    device = 0
    coopMode = True
    countMana = 0
    runCount = 0
    # def __init__(self):
    def shadeVariation(self, col, col2, shade=0):
        if shade == 0:
            return col == col2
        rezult = (abs(col[0] - col2[0]), abs(col[1] - col2[1]), abs(col[2] - col2[2]))
        shadowCount = 0
        for rgb in rezult:
            if rgb <= shade:
                shadowCount += 1
        return shadowCount == 3

    def getXYByColor(self, color, isGetSCreen=True, shade=0, startXY=(0, 0), endXY=(0, 0)):
        if (isGetSCreen):
            self.getScreen()
        img = self.screenshot
        coordinates = False

        if endXY[0] == 0 and endXY[1] == 0:
            endXY = (img.size[0], img.size[1])
        for x in range(img.size[0]):
            if not (startXY[0] < x < endXY[0]):
                continue

            for y in range(img.size[1]):
                if not (startXY[1] < y < endXY[1]):
                    continue
                if self.shadeVariation(img.getpixel((x, y))[:3], color, shade):
                    coordinates = (x, y)
                    continue
        return coordinates

    def pixelSearch(self, x1, y1, color):  # x2=1600, y2=900,
        # im = ImageOps.crop(im, (x1, y1, x2, y2))
        colorPixel = self.screenshot.getpixel((x1, y1))[:3]
        if colorPixel == color:
            return True
        else:
            return False

    def getScreen(self):
        self.shell(f'/system/bin/screencap -p /sdcard/{self.screenshotName}')
        # os.system('hd-adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        # Using the adb command to upload the screenshot of the mobile phone to the current directory

        os.system(f'hd-adb -s {self.device} pull /sdcard/{self.screenshotName}')
        try:
            self.screenshot = Image.open(f"{self.screenshotName}")
        except ValueError:
            print(ValueError)
            self.getScreen()

    def getPixelColor(self, x1, y1):
        self.getScreen()
        im = Image.open(f"{self.screenshotName}")
        # im1 = ImageOps.crop(im, (0, 0, 1000, 300))
        # im1.show()
        pixelRGB = im.getpixel((x1, y1))[:3]
        return pixelRGB

    def click(self, x, y, timer=True):
        if (timer):
            time.sleep(1)
        # os.system(f'hd-adb shell input tap {x} {y}')
        self.shell(f'input tap {x} {y}')
        if (timer):
            time.sleep(1)

    def main(self):
        while self.work:

            self.getScreen()
            self.log(f'getScreen {self.runCount}')

            # if self.countMana != 0 and self.countMana % 15 == 0:
            #     path = f'screens\{datetime.now().strftime("%d-%m-%Y_%H-%M")}.png'
            #     # Задайте имя файла с путем
            #     self.log(f'Save file {path}')
            #     shutil.copy(self.screenshotName, path)
            #     self.countMana = 16

            # if self.countMana != 0 and self.countMana >= 15:
            #     self.click(84, 1504)
            #     self.click(214, 1504)
            #     self.click(362, 1504)
            #     self.click(500, 1504)
            #     self.click(636, 1504)

            if self.isMainScreen():
                self.runCount = 0
                self.log('Is Main Screen')
                if self.coopMode:
                    self.log('Click Coop')
                    self.click(660, 1300)
                    self.log('Click Coop Random')
                    self.click(400, 700)
                    time.sleep(5)
                else:
                    self.log('Click Match')
                    self.click(250, 1300)


            if self.isFightScreen():
                self.log(f'isFightScreen')
                self.runCount = 0
                coordMana = self.getXYByColor((245, 190, 48), False, 10, (338, 1290), (574, 1414))
                if coordMana:
                    self.log(f'Click Mana {self.countMana}')
                    self.countMana = self.countMana + 1
                    self.click(450, 1360)

            if (self.getXYByColor((185,58,60), False, 1, (776, 490), ((776 + 62), (490 + 64)))):
                self.runCount = 0
                self.log('Detect Support Box. Exit...')
                self.click(570, 1350)
                time.sleep(1)
                self.getScreen()

            if (self.getXYByColor((186,58,62), False, 1, (618, 8), ((618 + 282), (8 + 1348)))):
                self.runCount = 0
                self.log('Detect Ads. Exit...')
                self.keyBack()
                time.sleep(1)
                self.getScreen()

            if (self.getXYByColor((247,221,85), False, 0, (30, 1276), (46, 1276 + 24))):
                self.runCount = 0
                self.log('Detect Arena Screen. Exit...')
                self.keyBack()
                time.sleep(1)
                self.getScreen()

            if (self.getXYByColor((40,118,239), False, 5, (327, 1443), (582, 1530))):
                self.runCount = 0
                self.log('Click Colllect')
                self.countMana = 0
                self.click(400, 1485)
                self.click(400, 1485)
                self.click(400, 1485)


            self.runCount = self.runCount + 1

            if (self.runCount >=30 ):
                self.appClose()
                time.sleep(10)
                self.appRun()
                time.sleep(30)
                self.runCount = 0

    def isMainScreen(self):
        return self.getXYByColor((32,129,247), False, 0, (0,1), (900, 200))


    def isFightScreen(self):
        return self.getXYByColor((178,255,244), False, 0, (239, 1358), (239+76, 1358+45)) != False

    def appClose(self):
        self.shell(f'am force-stop com.my.defense')

    def appRun(self):
        self.shell(f'am start -n com.my.defense/games.my.heart.commonpreloaderlib.PreloadActivity')

    def clickBack(self):
        self.click(67, 50)

    def keyQ(self):
        self.shell(f'input keyevent 45')

    def keyE(self):
        self.shell(f'input keyevent 33')

    def keyBack(self):
        self.shell(f'input keyevent 4')

    def start(self):
        self.device = inputDevice.get()
        self.screenshotName = self.device + '-screenshot.png'
        self.work = 1
        self.t1 = threading.Thread(target=self.main, args=[])
        self.t1.start()

    def stop(self):
        self.work = 0

    def closeWindow(self):
        self.work = 0
        tkWindow.destroy()

    def shell(self, cmd):
        os.system(f'hd-adb -s {self.device} shell {cmd}')

    def log(self, value):
        timeVal = datetime.now().strftime("%D %H:%M:%S")
        logString = "%s %s" % (timeVal, value)
        text.insert(END, logString + " \r\n")
        text.see("end")
        f = open("log.txt", "a")
        f.write(logString + " \r")
        f.close()

    def selectedDevice(self, event):
        self.device = inputDevice.get()

    def getXYByImage(self, imgSrc='icons/train.png'):
        img_rgb = cv2.imread(f"{self.screenshotName}")
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(imgSrc, 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            y = loc[0][0]
            x = loc[1][0]
            return (x, y)
        else:
            return False

    def getText(self, x, y, x1, y1, color):
        # img_rgb = cv2.imread('emulator-5554-screenshot.png')
        img_rgb = cv2.imread(self.screenshotName)
        (a, img_gray) = cv2.threshold(img_rgb, 127, 255, cv2.THRESH_BINARY)

        img_gray = img_gray[y:y + y1, x:x + x1]
        height, width, channels = img_gray.shape
        for x in range(height):
            for y in range(width):
                (b, g, r) = img_gray[x, y]
                if (b, g, r) != (255, 255, 255):
                    img_gray[x, y] = [0, 0, 0]

        # cv2.imshow('Detected', img_gray)
        # cv2.waitKey()
        cv2.imwrite('timeTrain.png', img_gray)

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        strTime = pytesseract.image_to_string('timeTrain.png').replace('\n', '').replace(' ', '')
        print(strTime)
        return (strTime)



bot = Bot()
buttonStart = Button(tkWindow, text='Start', command=bot.start)
buttonStart.pack()
buttonStop = Button(tkWindow, text='Stop', command=bot.stop)
buttonStop.pack()

tkWindow.protocol("WM_DELETE_WINDOW", bot.closeWindow)
devList = check_output("hd-adb devices")
text = Text(tkWindow, height=10, width=50)
text.insert(END, devList)

print(devList)
devListArr = re.compile(r'emulator-\d\d\d\d').findall(str(devList))
print('ARRAY DEVICES', devListArr)
rezArr = []
for x in devListArr:
    if (x.startswith('emulator-')):
        rezArr.append(x)
print(rezArr)

inputDevice = ttk.Combobox(tkWindow, width=15)
inputDevice['values'] = rezArr
inputDevice.bind("<<ComboboxSelected>>", bot.selectedDevice)
inputDevice.current(0)
inputDevice.pack()
text.pack()

tkWindow.mainloop()
