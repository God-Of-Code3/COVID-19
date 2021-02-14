import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication,
                             QPushButton, QLabel, QMessageBox,
                             QHBoxLayout, QScrollArea)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from PIL import Image, ImageDraw
import nibabel as nib

from Test import testFiles


WNDW_SZ = (800, 400)
WNDW_MAX_SZ = (1600, 800)
BTN_SZ = (100, 25)
IMG_SZ = (100, 100)


def openFile(way, images):
    name = "data/" + way.split('/')[-1].split('.')[0] + ".png"
    if os.path.exists(name):
        return False
    else:
        img = nib.load(way)
        array = img.get_fdata()
        
        image = Image.new("RGB", (256, 256), (0, 0, 0))
        
        for x in range(256):
            for y in range(256):
                value = (array[x * 2][y * 2][0] + 2048) // 16
                value = int(min(255, value))
                image.putpixel((x, y), (value, value, value))
        name = "data/" + way.split('/')[-1].split('.')[0] + ".png"
        image.save(name, "PNG")
        return name        


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.textEdit = QTextEdit()
        self.statusBar()
        
        self.setMinimumSize(*WNDW_SZ)
        self.setMaximumSize(*WNDW_MAX_SZ)
        self.setGeometry(300, 300, *WNDW_SZ)
        self.setWindowTitle('Definition of infection COVID-19')
 
        openFile = QAction('Settings', self)
        openFile.setShortcut('Ctrl+S')
        openFile.setStatusTip('Open Settings window')
        openFile.triggered.connect(self.showSettings)
 
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openFile)
        
        self.button = QPushButton('Select files', self)
        self.button.resize(*BTN_SZ)
        self.button.clicked.connect(self.showFiles)
        
        self.loading = QLabel('', self)
        
        self.labels = [0] * 20
        self.image_ways = []
        self.paths = []
        self.names = []       
        
        self.test = QPushButton('Test scans', self)
        self.test.resize(*BTN_SZ)
        self.test.clicked.connect(self.testFiles)
        
        self.show()
        
    def testFiles(self):
        if self.image_ways:
            results = testFiles(self.paths)
            for i in range(len(results)):
                for j in range(len(self.labels)):
                    if self.labels[j] != 0 and self.labels[j][3] == self.names[i]:
                        index = j
                        break
                
                data = str(results[i][1]) + '\n' + str(results[i][2])

                if results[i][0] == 1:
                    self.labels[index][4].setText('Sick' + '\n' + data)
                else:
                    self.labels[index][4].setText('Health' + '\n' + data)
        else:
            self.loading.setText('First you need to select files')
        
    def alignImages(self):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()        
        
        lbls = [i for i in self.labels if i != 0]
        start = (width - len(lbls) * IMG_SZ[0] * 6 / 5) / 2 + IMG_SZ[0] / 10
        
        for i in range(len(lbls)):
            x = int(start + i * (IMG_SZ[0] * 6 / 5))
            y = int(IMG_SZ[1] + 20)
            index = self.labels.index(lbls[i])
            
            self.labels[index][0].move(x, y)
            self.labels[index][0].show()
                
            self.labels[index][1].move(int(x + IMG_SZ[0] * 4 / 5), y)
            self.labels[index][1].show()
            
            self.labels[index][3].resize(IMG_SZ[0], IMG_SZ[1])
            self.labels[index][3].move(x, int(y - IMG_SZ[1]))
            self.labels[index][3].show()
            
            self.labels[index][4].resize(IMG_SZ[0], int(IMG_SZ[1] / 2))
            self.labels[index][4].move(x, int(y + IMG_SZ[1]))
            self.labels[index][4].show()            
    
    def paintEvent(self, event):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        
        self.test.move(int(width - BTN_SZ[0] * 5 / 4),
                       int(height - BTN_SZ[1] * 3))        
        self.button.move(int(BTN_SZ[0] / 4),
                         int(height - BTN_SZ[1] * 3))
        self.loading.move(int(BTN_SZ[0] * 3 / 2),
                          int(height - BTN_SZ[1] * 3))
        self.loading.resize(int(width - BTN_SZ[0] * 3), BTN_SZ[1])
        self.alignImages()
                
    def deleteImage(self):
        sender = self.sender()
        
        for i in range(len(self.labels)):
            if self.labels[i] != 0 and self.labels[i][1] == sender:
                index = i
                break
        self.labels[index][0].hide()
        self.labels[index][1].hide()
        self.labels[index][3].hide()
        self.labels[index][4].hide()
        
        images_index = self.image_ways.index(self.labels[index][2])
        del self.image_ways[images_index]
        del self.paths[images_index]
        del self.names[images_index]
        
        os.remove(self.labels[index][2])
        self.labels[index] = 0
        
        self.loading.setText('The selected file has been deleted')
    
    def showFiles(self):
        dialogSelectFiles = QFileDialog()
        dialogSelectFiles.setFileMode(QFileDialog.ExistingFiles)
        dialogSelectFiles.exec_()
 
        ignored = ''
        empty = True
        data = dialogSelectFiles.selectedFiles()
        n = 0
        for way in data:
            n += 1
            self.loading.setText(str(n) + '/' + str(len(data)))
            self.loading.show()
            
            filename = openFile(way, self.image_ways)
            if not filename:
                ignored = ' (already uploaded files were ignored)'
            else:
                self.image_ways.append(filename)
                self.paths.append(way)
                
                name = way.split('/')[-1].split('.')[0]
                nm_lbl = QLabel(name, self)
                width = nm_lbl.fontMetrics().boundingRect(nm_lbl.text()).width()
                k = len(name) // ((width - 1) // IMG_SZ[0] + 1)
                name = [name[i - k:i] for i in range(k, len(name) + 1, k)]
                nm_lbl.setText('\n'.join(name))
                self.names.append(nm_lbl)
                
                empty = False
        for i in range(len(self.labels)):
            if self.labels[i] != 0:
                self.labels[i][0].hide()
                self.labels[i][1].hide()
                self.labels[i][3].hide()
                self.labels[i] = 0
        for i in range(len(self.image_ways)):
            pixmap = QPixmap(self.image_ways[i])
            pixmap = pixmap.scaled(100, 100,
                                   Qt.KeepAspectRatio,
                                   Qt.FastTransformation)
            
            for j in range(len(self.labels)):
                if self.labels[j] == 0:
                    self.labels[j] = [QLabel(self),
                                      QPushButton('✖', self),
                                      self.image_ways[i],
                                      self.names[i],
                                      QLabel(self)]
                    
                    self.labels[j][0].setPixmap(pixmap)
                    self.labels[j][0].resize(*IMG_SZ)
                    self.labels[j][0].show()
                    
                    self.labels[j][1].resize(int(IMG_SZ[0] / 5),
                                             int(IMG_SZ[1] / 5))
                    self.labels[j][1].clicked.connect(self.deleteImage)
                    self.labels[j][1].show()
                    
                    self.labels[j][3].show()
                    break
        if empty:
            self.loading.setText('Already uploaded files were ignored')
        else:
            self.loading.setText('Files uploaded' + ignored)
        self.loading.show()
        
    def showSettings(self):
        print('settings')
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
                                     "Are you sure you want to leave?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            for i in range(len(self.image_ways)):
                os.remove(self.image_ways[i])
            event.accept()
        else:
            event.ignore()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()   
    sys.exit(app.exec_())
