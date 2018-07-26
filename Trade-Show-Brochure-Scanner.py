##Andrew Callahan

#Desktop Application Modules
import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

#OCR (Optical Charecter Recognition) Modules
import pytesseract
import random
import string
from PIL import Image

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(50,50,1000,1500)
        self.setWindowTitle("Brochure Scanner")
        self.setWindowIcon(QtGui.QIcon('griffith-logo.png'))

        palette = QtGui.QPalette()
        myPixmap = QtGui.QPixmap('green-wave.jpg')
        myScaledPixmap = myPixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation)
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(myScaledPixmap))
        self.setPalette(palette)

        extractAction = QtGui.QAction('Quit', self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Leave the App")
        extractAction.triggered.connect(QtCore.QCoreApplication.instance().quit)

        openEditor = QtGui.QAction("&Editor",self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip('Open Editor')
        openEditor.triggered.connect(self.editor)
        
        openFile = QtGui.QAction("&Open File",self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)

        editorMenu = mainMenu.addMenu('&Editor')
        editorMenu.addAction(openEditor)

        tabs    = QtGui.QTabWidget()
        self.home()
    
    def home(self):
    
        pic = QtGui.QLabel(self)
        pic.setGeometry(10, 10, 500, 500)
        pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/bigger-griffith-logo.png"))
        pic.move(600,275)
        self.show
        
        intro_pic = QtGui.QLabel(self)
        intro_pic.setGeometry(10, 10, 500, 500)
        intro_pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/Intro-Text.png"))
        intro_pic.move(50,75)

        self.show()

    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        file = Image.open(name)

        #scans jpg for text and converts it to txt file
        img = file
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        result = pytesseract.image_to_string(img)
        
        #turn result into text file
        with open("result.txt",mode = "w", encoding ='utf-8') as file:
            file.write(result)
        with open("result.txt",mode = "r", encoding ='utf-8') as f:
            data = f.readlines()

        #find out TITLE
        def find_TITLE():
            #use first line with text and is not short
            with open("result.txt",mode = "r", encoding ='utf-8') as f:
                data = f.readlines()
            TITLE = "N/A"
            count = 0
            while len(TITLE) <= 4:
                TITLE = data[count]
                count += 1

            return TITLE

        #find out purpose
        def find_purpose():
            purpose = []
            count = 0
            row_num = 0
            tester = 'F'
            with open("result.txt",mode = "r", encoding ='utf-8') as f:
                for line in f:
                    count += 1
                    #tester = []
                    if '.' in line and ".." not in line and '. .' not in line:
                        ##making sure it's not a bullet
                        lower_case_alpha = string.ascii_lowercase
                        for i in lower_case_alpha:
                            if (i + '.') in line:
                                row_num = count - 1
                                tester = 'T'
                                break
                    if row_num != 0:
                        break
            with open("result.txt",mode = "r", encoding ='utf-8') as f:
                data = f.readlines()
            if tester == 'F':
                ##if we weren't able to find a period use the first body of text
                for i in list(range(len(data))):
                    new_test = False
                    if data[i] != '\n' and data[i+1] != '\n':
                        purpose.append(data[i])
                        purpose.append(data[i+1])
                        index = i+1
                        while new_test == False:
                            index += 1
                            if data[index] != '\n':
                                purpose.append(data[index])
                            else:
                                new_test = True
                                break
                    if new_test:
                        break

            else:
                purpose.append(data[row_num])
                ##add lines following until \n, go reverse too
                not_blank = True
                add_count = 0
                while not_blank == True:
                    add_count += 1
                    if data[row_num + add_count] != '\n':
                        purpose.append(data[row_num + add_count])
                    else:
                        not_blank = False
                        break
                not_blank = True
                sub_count = 0
                while not_blank == True:
                    sub_count += 1
                    if data[row_num - sub_count] != '\n':
                        purpose.insert(0,data[row_num - sub_count])
                    else:
                        not_blank = False
                        break

                ##get rid of '\n' if the line has less than two spaces
                for i in list(range(len(purpose))):
                    num_space = 0
                    for j in list(range(len(purpose[i]))):
                        if purpose[i][j] == ' ':
                            num_space += 1
                    if num_space <= 2:
                        purpose[i] = purpose[i][:-1] + ' '
                purpose.append('\n')

            ##making all lower case if all upper case
            for i in list(range(len(purpose))):
                if purpose[i].isupper():
                    purpose[i] = purpose[i].lower()

            return purpose

        #finding out key selection criteria (ksc)
        def find_ksc():
            ksc = []
            with open("result.txt",mode = "r", encoding ='utf-8') as f:
                data = f.readlines()

            for i in list(range(len(data))):
                count = 0
                line = data[i]
                first_char = line[0]
                if first_char in ['+', '-','.','0'] and '..' not in line and '. .' not in line:
                    if first_char in ['+', '-','.','0']:
                        s = data[i]
                        s = list(s)
                        s[0] = '-'
                        data[i] = ''.join(s)
                    line = data[i]
                    new_line = line
                    while new_line != '\n' and '..' not in new_line and '. .' not in new_line:
                        count += 1
                        ksc.append(new_line)
                        if (i + count) > (len(data) - 1): 
                            break
                        else:
                            new_line = data[i + count]

            ##if still ksc empty look for groups of two lines together without periods
            if ksc == []:
                for i in list(range(len(data))):
                    if i == len(data) - 1:
                        break
                    temp_addition = ''
                    temp_addition_2 = ''
                    temp_addition_3 = ''
                    if data[i] != '\n' and '.' not in data[i] and data[i-1] == '\n':
                        temp_addition = '-' + data[i]
                        if data[i+1] != '\n' and '.' not in data[i+1]:
                            temp_addition_2 = data[i+1]
                            if data[i+2] != '\n' and '.' not in data[i+2]:
                                temp_addition_3 = data[i+2]
                    ###note that temp_addition_3 must be empty, this is so we know they are groups of 2
                    if temp_addition != '' and temp_addition_2 != '' and temp_addition_3 == '':
                        ksc.append(temp_addition)
                        ksc.append(temp_addition_2)
                        ksc.append(temp_addition_3)

            return ksc

        #finding out vendor
        def find_vendor():
            count = 0
            for i in result:
                count += 1
                new_count = 1
                if i == '®':
                    last_char = result[count - 1]
                    vendor = ''
                    while last_char != ' ' and  last_char != '.' and (count - new_count) > -1:
                        new_count += 1
                        vendor += str(last_char)
                        last_char = result[count - new_count]
                    break
            ##if the trademark symbol did't work then look for first all caps word
            if new_count == 1:
                vendor =''
                for i in data:
                    for j in list(range(len(i))):
                        condition = "Not Yet Determined"
                        if i[j] in string.ascii_uppercase:
                            letter = i[j]
                            while letter != ' ' and letter != '.' and letter in string.ascii_uppercase:
                                vendor += letter
                                j += 1 
                                letter = i[j]
                            if len(vendor) >= 3:
                                condition = 'satisfied'
                            else:
                                vendor = "none_available"
                        if condition == 'satisfied':
                            break
                    if condition == 'satisfied':
                        break
            else:
                vendor = vendor[::-1]
                vendor = vendor.replace('\r', '').replace('\n', '')
            
            if "none_available" in vendor:
                vendor = "none_availble"
            return vendor
            
        #calling functions
        TITLE = find_TITLE()
        vendor = find_vendor()
        purpose = find_purpose()
        ksc = find_ksc()


        #creating the txt file
        num = random.randint(1,10001)
        title = "new-tech-from-" + str(vendor)+ str(num)
        file = open(title + ".txt", mode = "w", encoding ='utf-8')
        file.write("TITLE: " + TITLE + "\n")
        file.write("Known Locations Used: N/A \r\n")

        ##adding purpose
        if len(purpose) >= 1:
            file.write("Purpose:"  + purpose[0])
            for i in list(range(len(purpose))):
                if i != 0:
                    file.write(purpose[i])
        else:
            file.write("Purpose: N/A")

        #adding ksc
        if len(ksc) >= 1:
            file.write("\nKey Selection Criteria:\r\n"  + ksc[0])
            for i in list(range(len(ksc))):
                if i != 0:
                    file.write(ksc[i])
        else:
            file.write("\nKey Selection Criteria: N/A \n")

        ##adding vendor
        file.write("\nVendor: " + vendor + "\r\n")

        file.close()

        #displaying result in the editor
        self.editor()
        new_file = open(title + ".txt", 'r', encoding ='utf-8')

        with new_file:
            text = new_file.read()
            self.textEdit.setText(text)
            
            
#creating instance of the application        
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

#automatically running the program
run()
