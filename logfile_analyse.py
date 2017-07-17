import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
import re




def inspect(f,rexpr, hist):
    print("Opening File")
    f = open(f)
    print("File Opened")
    ocDict = {}
    mainPattern = re.compile(rexpr)
    datePattern = re.compile("  Time: (\d*)-(\w*)-(\d*) \d*:\d*:\d*")
    latestYear = None
    latestMonth = None
    latestDay = None
    while True:
        line = f.readline()
        if line == '': break
        if hist:
            dateMatch = datePattern.match(line)
            if dateMatch:
                latestDay = dateMatch.group(1)
                latestMonth = dateMatch.group(2)
                latestYear = dateMatch.group(3)
        matchObj = mainPattern.match(line)
        if matchObj:
            res = matchObj.group()
            if res in ocDict:
                ocDict[res]["count"] += 1
                if latestYear in ocDict[res]:
                    if latestMonth in ocDict[res][latestYear]:
                        if latestDay in ocDict[res][latestYear][latestMonth]:
                            ocDict[res][latestYear][latestMonth][latestDay]+= 1
                        else:
                            ocDict[res][latestYear][latestMonth][latestDay] = 1
                    else:
                        ocDict[res][latestYear][latestMonth] = {latestDay: 1}
                else:
                    ocDict[res][latestYear] = {latestMonth: {latestDay: 1}}
            else:
                ocDict[res] = {"count":1, latestYear:{latestMonth: {latestDay: 1}}}   

    #print(ocDict)
    return ocDict

class BarChart:
    def __init__(self, arg, arg2):
        self.set0 = QBarSet(arg2[0])
        self.series = QBarSeries()
        self.chart = QChart()
        self.axis = QBarCategoryAxis(self.chart)
        self.categories = [str(i) for i in range(1, 32)]

        freqList = []
        for i in range(1, 32):
            if arg:
                key = None
                if i < 10:
                    key = "0"+str(i)
                else: key = str(i)
                if key in arg: freqList.append(arg[key])
                else: freqList.append(0)
            else:
                freqList.append(0)
        self.set0.append(freqList)
        self.series.append(self.set0)
        self.chart.addSeries(self.series)
        self.axis.append(self.categories)

        self.chart.setTitle('Frequency Histogram')
        self.chart.createDefaultAxes()
        self.chart.setAxisX(self.axis, self.series)
        #self.chart.legend().setEnabled(False)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.cv = QChartView(self.chart)
    

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

        customRE = QAction("&Enter Custom Expression", self)
        customRE.setStatusTip('Enter a custom regular expression')
        customRE.triggered.connect(self.custRE)

        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        optionMenu = mainMenu.addMenu('&Options')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(exitAction)
        optionMenu.addAction(customRE)
        
        self.home()

    def home(self):
        btn = QPushButton("Analyze", self)
        btn.clicked.connect(self.analyze)
        btn.resize(btn.minimumSizeHint())
        btn.move(20,40)

        chartRefreshBtn = QPushButton("Show Histogram", self)
        chartRefreshBtn.clicked.connect(self.histogram)
        chartRefreshBtn.resize(chartRefreshBtn.minimumSizeHint())
        chartRefreshBtn.move(20,150)

        yrlbl = QLabel("Year-Month",self)
        yrlbl.move(20, 90)
        
        self.yearSel = QLineEdit(self)
        self.yearSel.move(120, 97)
        self.yearSel.resize(self.yearSel.minimumSizeHint())

        self.monthCB = QComboBox(self)
        self.monthCB.move(200, 97)
        self.monthCB.resize(self.monthCB.minimumSizeHint())
        self.monthCB.addItems(["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"])

        self.errorCB = QComboBox(self)
        self.errorCB.move(150, 150)
        self.errorCB.addItem("Select Error Category from here")
        self.errorCB.resize(300,chartRefreshBtn.height())
        
        
        self.chbox1 = QCheckBox("Histogram", self)
        self.chbox1.move(120, 40)
        
        self.show()
        
    def custRE(self):
        text, okPressed = QInputDialog.getText(self, "Custom RE","Enter a valid Regular Expression", QLineEdit.Normal, "")
        if okPressed and text != '':
            print("Using Regular Expression:",text)
            self.re = text
    def histogram(self):
        self.chartWindow = QMainWindow()
        self.chartWindow.setWindowTitle("Frequency Charts")
        self.chartWindow.resize(800, 600)


        arg = None
        print (self.yearSel.text())
        print(self.yearSel.text() in self.data[self.errorCB.currentText()])
        if self.yearSel.text() in self.data[self.errorCB.currentText()] and self.monthCB.currentText() in self.data[self.errorCB.currentText()][self.yearSel.text()]:
            arg = self.data[self.errorCB.currentText()][self.yearSel.text()][self.monthCB.currentText()]
            print("Valid Month Found")
        else:
            print("Invalid Month Found")
        
        self.ch = BarChart(arg, (self.errorCB.currentText(),))
        
        self.chartWindow.setCentralWidget(self.ch.cv)
        self.chartWindow.show()
    def analyze(self):
        if self.fileSelected:
            #print("Starting analysis")
            ocDict = inspect(self.fileSelected, self.re, self.chbox1.checkState())
            self.data = ocDict
            if self.chbox1.checkState():
                for i in ocDict:
                    if i!="count":
                        self.errorCB.addItem(i)
            
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
                self.table.setItem(curRow,1, QTableWidgetItem(str(ocDict[i]["count"])))
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
