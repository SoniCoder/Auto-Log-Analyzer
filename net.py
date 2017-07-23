from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from config import *

def send(pswd, attachments):
    img_data_set =[]
    for f in attachments:
        img_data_set.append(open(f, 'rb').read())
    msg = MIMEMultipart()
    msg['Subject'] = globals()['SUBJECT']
    msg['From'] = globals()['FROM']
    msg['To'] = globals()['TO']
    text = MIMEText(globals()['TEXT'])
    msg.attach(text)
    for img_i in range(len(img_data_set)):
        image = MIMEImage(img_data_set[img_i], name=os.path.basename(attachments[img_i]))
        msg.attach(image)

    s = smtplib.SMTP(globals()['SERVER'], globals()['PORT'])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(globals()['FROM'], pswd)
    s.sendmail(globals()['FROM'], globals()['TO'], msg.as_string())
    s.quit()

class Mailer(QMainWindow):
    def __init__(self):        
        super(Mailer, self).__init__()
        self.resize(300, 500)
        self.setWindowTitle("Mailer")
        self.setWindowIcon(QIcon('icon.png'))

        attachfileAction = QAction("&Attach", self)
        attachfileAction.setStatusTip('Add attachment(s)')
        attachfileAction.triggered.connect(self.attach_files)

        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(attachfileAction)
        
        self.design()
        
        self.show()

    def attach_files(self):
        options = QFileDialog.Options()
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Select attachment(s)", "","All Files (*);;JPG Files (*.jpg)", options=options)
        if fileNames:
            print("Files Selected:",fileNames)
            globals()['ATTACHMENTS'] += fileNames
        self.refresh_attachments()
    def design(self):
        fromlbl = QLabel("From:",self)
        fromlbl.move(20, 40)
        
        self.FromField = QLineEdit("hothritik1@gmail.com",self)
        self.FromField.move(80, 40)
        self.FromField.resize(200,fromlbl.height())

        passlbl = QLabel("Password:",self)
        passlbl.move(20, 80)
        
        self.PassField = QLineEdit(self)
        self.PassField.move(80, 80)
        self.PassField.resize(200,fromlbl.height())
        self.PassField.setEchoMode(QLineEdit.Password)

        tolbl = QLabel("To:",self)
        tolbl.move(20, 120)
        
        self.ToField = QLineEdit(self)
        self.ToField.move(80, 120)
        self.ToField.resize(200,fromlbl.height())

        sublbl = QLabel("Subject:",self)
        sublbl.move(20, 160)
        
        self.SubField = QLineEdit("Test Subject",self)
        self.SubField.move(80, 160)
        self.SubField.resize(200,fromlbl.height())

        textlbl = QLabel("Text:",self)
        textlbl.move(20, 200)
        
        self.TextField = QTextEdit("Test Content",self)
        self.TextField.move(80, 200)
        self.TextField.resize(200,100)

        attachlbl = QLabel("Attached:",self)
        attachlbl.move(20, 320)
        
        self.AttachCB = QComboBox(self)
        self.AttachCB.move(80, 320)
        self.AttachCB.resize(200,fromlbl.height())
        self.AttachCB.addItem("No Attachments")

        serverlbl = QLabel("Server:",self)
        serverlbl.move(20, 360)
        
        self.ServerField = QLineEdit("smtp.gmail.com",self)
        self.ServerField.move(80, 360)
        self.ServerField.resize(200,fromlbl.height())

        portlbl = QLabel("Subject:",self)
        portlbl.move(20, 400)
        
        self.PortField = QLineEdit("587",self)
        self.PortField.move(80, 400)
        self.PortField.resize(200,fromlbl.height())

        self.sendBtn = QPushButton("Send",self)
        self.sendBtn.move(20, 460)
        self.sendBtn.resize(self.sendBtn.minimumSizeHint())
        self.sendBtn.clicked.connect(self.send)
    def refresh_attachments(self):
        self.AttachCB.clear()
        
        if globals()['ATTACHMENTS']:
            self.AttachCB.addItems(globals()['ATTACHMENTS'])
            
            self.AttachCB.setCurrentIndex(len(globals()['ATTACHMENTS'])-1)            
        else:
            self.flCB.addItem("No Attachments")

    def reload_vars(self):
        globals()['SUBJECT'] = self.SubField.text()
        globals()['FROM'] = self.FromField.text()
        globals()['TO'] = self.ToField.text()
        globals()['TEXT'] = self.TextField.toPlainText()
        globals()['SERVER'] = self.ServerField.text()
        globals()['PORT'] = self.PortField.text()
        globals()['PASSWORD'] = self.PassField.text()

    def send(self):
        self.reload_vars()
        send(globals()['PASSWORD'], globals()['ATTACHMENTS'])        
