import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
import re




def inspect(f,rexpr):
    print("Opening file")
    f = open(f)
    print("fileOpened")
    ocDict = {}
    mainPattern = re.compile(rexpr)

            
    count = 0

    while True:
        line = f.readline()
        if line == '': break
        matchObj = mainPattern.match(line)
        if matchObj:
            res = matchObj.group()
            if res in ocDict: ocDict[res] += 1
            else: ocDict[res] = 1

    print(ocDict)
    return ocDict

class Window(QMainWindow):
    def __init__(self):
        self.fileSelected = ""
        self.re = "TNS-\d{5}: .*"
        
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Performance Analyzer")
        self.setWindowIcon(QIcon('icon.png'))

        extractAction = QAction("&Browse Log File", self)
        extractAction.setShortcut("Ctrl+B")
        extractAction.setStatusTip('Select Appropriate Log File')
        extractAction.triggered.connect(self.file_select)

        customRE = QAction("&Enter Custom RE", self)
        customRE.setStatusTip('Enter a custom regular expression')
        customRE.triggered.connect(self.custRE)


        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        optionMenu = mainMenu.addMenu('&Options')
        fileMenu.addAction(extractAction)
        optionMenu.addAction(customRE)
        
        self.home()

    def home(self):
        btn = QPushButton("Analyze", self)
        btn.clicked.connect(self.analyze)
        btn.resize(btn.minimumSizeHint())
        btn.move(20,40)
        self.show()

    def custRE(self):
        text, okPressed = QInputDialog.getText(self, "Custom RE","Enter a valid Regular Expression", QLineEdit.Normal, "")
        if okPressed and text != '':
            print("Using Regular Expression:",text)
            self.re = text

    def analyze(self):
        if self.fileSelected:
            #print("Starting analysis")
            ocDict = inspect(self.fileSelected, self.re)
            
            
            self.window = QWidget()
            self.table = QTableWidget(self.window)
            self.tableItem = QTableWidgetItem()
            

            # initiate UI
            w_width = 800
            w_height = 300
            mb_height = 0
            #print("I did analysis")
            self.window.setWindowTitle("Error Frequency Table")
            self.window.resize(w_width, w_height)
            self.table.move(0, mb_height)
            self.table.resize(w_width, w_height-mb_height)
            self.table.setRowCount(len(ocDict))
            self.table.setColumnCount(2)
            self.table.setColumnWidth(0, w_width/2)
            self.table.setColumnWidth(1, w_width/2)

            self.table.setHorizontalHeaderLabels("Error Name;Frequency;".split(";"))

            curRow = 0

            # set data
            for i in ocDict:
                self.table.setItem(curRow,0, QTableWidgetItem(i))
                self.table.setItem(curRow,1, QTableWidgetItem(str(ocDict[i])))
                curRow += 1
            self.window.show()
            self.table.show()
    def file_select(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print("File Selected:",fileName)
            self.fileSelected = fileName
    def close_application(self):
        #print("whooaaaa so custom!!!")
        sys.exit()



# Run Everything
app = QApplication(sys.argv)
GUI = Window()
app.exec_()
