from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pytube import YouTube
import sys 
import os 
from time import sleep as tmSleep
import time
import traceback
import math
import urllib.request, io
from PIL import ImageTk, Image
from PIL.ImageQt import ImageQt
from threading import *

class YtDetailThread(QThread):
    ytsgl = QtCore.pyqtSignal(str,bytes,str,str)
    ytsglException = QtCore.pyqtSignal(str)

    def __init__(self):
        super(YtDetailThread, self).__init__()
        self.yt_url = ''
        self.yt_title = ''
        self.yt_thumbnail = ''
        self.yt_videoquality=''
        self.yt_videoTime=''

    @pyqtSlot(str, bytes)
    def run(self):
        try:
            self.yt_title = self.getyttitle(self.yt_url)
            self.yt_thumbnail = self.getytthumbnail(self.yt_url)
            self.yt_videoquality = self.getytresolution(self.yt_url)
            self.yt_videoTime = self.getytvideosize(self.yt_url)
            self.ytsgl.emit(self.yt_title, self.yt_thumbnail,self.yt_videoquality,self.yt_videoTime)
            
        except:
            print("Invalid URL")
            self.ytsglException.emit(str(sys.exc_info()[1]))
            
            
    
    
    def getytvideosize(self,url):
        yt=YouTube(url)
        videoSizeMinute=self.convert(yt.length)
        return videoSizeMinute
        
    def convert(self,seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
      
        return "%d:%02d:%02d" % (hour, minutes, seconds)
    
    def getytthumbnail(self, url):
        yt = YouTube(url)
        tempurl = 'https://i.ytimg.com/vi/'+yt.video_id+'/default.jpg'
        return urllib.request.urlopen(tempurl).read()

    def getyttitle(self, url):
        yt = YouTube(url)
        return yt.title
    
    def convert_size(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
    def getytresolution(self,url):
        yt=YouTube(url)
        res=""
        for stream in yt.streams.filter(progressive=True):
            print(stream)
            before_nth = str(stream.type)[:0]
            n = str(stream.type)[0].upper()
            new_pos = 1
            after_nth = str(stream.type)[new_pos:]
            word = before_nth + n + after_nth
            res+=word+"    "+str(stream.resolution)+"    "+str(self.convert_size(stream.filesize))+"\n"
        audioStream=yt.streams.filter(type='audio').first()
        res+="Audio Only"+"    "+str(self.convert_size(audioStream.filesize))+"\n"
        return res


class YtDownloadThread(QThread):
    ytdwldsgl = QtCore.pyqtSignal(float)
    ytDownloadException = QtCore.pyqtSignal(str)

    filesize = 0

    def __init__(self):
        super(YtDownloadThread, self).__init__()
        self.yt_url = ""
        self.yt_savepath = ""
        self.yt_quality = ""

    @pyqtSlot(str)
    def run(self):
        self.downloadyt(self.yt_url,self.yt_savepath, self.yt_quality)

    def downloadyt(self, url, pth, comboboxSelectedIndex):

        yt = YouTube(url)
        yt.register_on_progress_callback(self.progress_bar)
        print(comboboxSelectedIndex)
        try:
            if comboboxSelectedIndex.find("1080") !=-1:
                print("1080p Download Ready")
                stream = yt.streams.filter(res="1080p").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif comboboxSelectedIndex.find("720") !=-1:
                print("720p Download Ready")
                stream = yt.streams.filter(res="720p").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif comboboxSelectedIndex.find("480") !=-1:
                print("480p Download Ready")
                stream = yt.streams.filter(res="480p").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif comboboxSelectedIndex.find("360p") !=-1:
                print("360p Download Ready")
                stream = yt.streams.filter(res="360p").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif comboboxSelectedIndex.find("144p") !=1:
                print("144p Download Ready")
                stream = yt.streams.filter(res="144p").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif comboboxSelectedIndex.find("Audio") !=-1:
                print("Audio Download Ready")
                stream = yt.streams.filter(type = "audio").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
        except:
            self.ytDownloadException.emit(str(sys.exc_info()[1]))

    def progress_bar(self, chunk, file_handle, bytes_remaining):
        remaining = (100 * bytes_remaining) / self.filesize
        step = 100 - int(remaining)
        self.ytdwldsgl.emit(step)



class App(QMainWindow):
    yturl = ""
    ytviews = ""
    ytlength = ""
    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui",self)
        self.temp = 0
        self.ytthread = YtDetailThread()
        self.ytthread.ytsgl.connect(self.finished)
        self.ytthread.ytsglException.connect(self.exceptionhandle)
        self.setWindowIcon(QIcon("icons/youtube_icon.png"))
        #connect
        self.sourceLineEdit.returnPressed.connect(lambda: self.on_fetchbtn_clicked())
        self.pushButton_2.clicked.connect(self.browseDestination)
        self.downloadButton.clicked.connect(self.on_dwnld_clicked)
        self.convertButton.clicked.connect(self.on_fetchbtn_clicked)
        self.convertButton.setIcon(QIcon("icons/convert.png"))
        #hide widget
        self.videoGruopBox.hide()
        #defaul save path
        self.savepath = os.path.expanduser("~\Desktop")
        self.destinationLineEdit.setText(str(self.savepath))
        
        self.ytdwlthread = YtDownloadThread()
        self.ytdwlthread.ytdwldsgl.connect(self.processdwld)
        self.ytdwlthread.ytDownloadException.connect(self.exceptionhandle)
        
        
        
    @pyqtSlot()
    def on_fetchbtn_clicked(self):
        #video infos
        self.temp = 0
        self.progressBar.setValue(0)
        self.ytthread.yt_url = self.sourceLineEdit.text()
        rect = self.videoImage.geometry()
        size = QtCore.QSize(min(rect.width(), rect.height()), min(rect.width(), rect.height()))
        movie = QMovie("icons/loading.gif")
        movie.setScaledSize(size)
        movie.start()
        self.videoImage.setMovie(movie)
        self.videoImage.setGeometry(280, 30, 120, 66)
        print("URL " + str(self.ytthread.yt_url))
        print("Waiting for response ..........")
        self.ytthread.start()
        self.disableBeforeFetchInfo()
        
            
    def disableBeforeDownloadWidget(self):
        self.video_tittle.show()
        self.video_Quality_ComboBox.show()
        self.videoImage.show()
        self.progressBar.hide()
        self.downloadButton.show()
        self.videoTime.show()
        #group box container in other elements
    
    def disableBeforeFetchInfo(self):
        self.videoGruopBox.show()
        self.videoImage.show()
        self.videoTime.hide()        
        self.video_tittle.hide()
        self.video_Quality_ComboBox.hide()
        self.progressBar.hide()
        self.downloadButton.hide()
        
        
        
    def processdwld(self, dwnld):
        print(dwnld)
        self.progressBar.setValue(int(dwnld))
        if dwnld >= 100 and self.temp == 0:
            self.temp = self.temp + 1
            self.downloadcomplete()
    def on_dwnld_clicked(self):
        #downloading start
        print("Starting download....")
        self.downloadButton.hide()
        self.progressBar.show()
        self.video_Quality_ComboBox.hide()
        
        
        self.ytdwlthread.yt_url = self.sourceLineEdit.text()
        self.ytdwlthread.yt_savepath = self.savepath
        self.ytdwlthread.yt_quality = self.video_Quality_ComboBox.itemText(self.video_Quality_ComboBox.currentIndex())
        self.ytdwlthread.start()
    
    def finished(self, yttitle,ytthumbnail,ytquality,ytvideolenght):
        #enabled ui elements
        self.videoGruopBox.show()
        self.disableBeforeDownloadWidget()
        #set video title
        self.video_tittle.setText(yttitle)  # Show the output to the user
        self.videoTime.setText(ytvideolenght)
        #set image
        image = QImage()
        image.loadFromData(ytthumbnail)
        rect = QRect(0,12,120,66)
        image = image.copy(rect)
        self.videoImage.setPixmap(QPixmap(image))
        self.videoImage.setGeometry(20, 30, 120, 66)
        #set quality
        self.video_Quality_ComboBox.clear()
        qualityS=''
        for items in ytquality:
            if items!='\n':
                qualityS+=items
            elif items=='\n':
                self.video_Quality_ComboBox.addItem(qualityS)
                qualityS=''
        #self.dwnld.setEnabled(True)
    
    def browseDestination(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName=str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.savepath=fileName
        if self.savepath=="":
            self.savepath = os.path.expanduser("~\Desktop")
        self.destinationLineEdit.setText(self.savepath)
    
    def exceptionhandle(self, msg):
        errorMessage=""
        if msg.find("regex_search")!=-1:
            errorMessage="The URL you entered is invalid. Please enter a different URL."
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(errorMessage)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        #self.thumbnail.setPixmap(QPixmap("icon/failed.jpg"))
    
    def downloadcomplete(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The video has been downloaded successfully.")
        msg.setWindowTitle("Info")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.downloadButton.show()
        self.video_Quality_ComboBox.show()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    application=App()
    application.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Closing Window...")

    
    
    
