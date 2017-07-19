import datetime
import re
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *

from net import *

# test data 
testDict = None


def inspect(f,rexpr, hist, ocDict):
    global testDict
    print("Opening File")
    f = open(f)
    if f:
        print("File Opened Successfully")
    else:
        print("File Opening Exception")
        exit(1)
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
    testDict = ocDict
    #print(ocDict)
    return

class BarChart:
    def __init__(self, arg, arg2, week = None):
        if week:
            self.series = QBarSeries()
            self.chart = QChart()
            self.axis = QBarCategoryAxis(self.chart)
            self.categories = [str(i) for i in range(7*(week-1) + 1, 7*week)]
            self.barsets = []
            for err in arg:
                self.barsets.append(QBarSet(err))
                freqList = []
                for i in range(7*(week-1) + 1, 7*week + 1):
                    if arg2[0] in arg[err] and arg2[1] in arg[err][arg2[0]]:
                        key = None
                        if i < 10:
                            key = "0"+str(i)
                        else: key = str(i)
                        if key in arg[err][arg2[0]][arg2[1]]: freqList.append(arg[err][arg2[0]][arg2[1]][key])
                        else: freqList.append(0)
                    else:
                        freqList.append(0)
                self.barsets[-1].append(freqList)
            for bset in self.barsets:
                self.series.append(bset)
            self.chart.addSeries(self.series)
            self.axis.append(self.categories)

            self.chart.setTitle('Frequency Histogram')
            self.chart.createDefaultAxes()
            self.chart.setAxisX(self.axis, self.series)
            self.chart.legend().setAlignment(Qt.AlignBottom)

            self.cv = QChartView(self.chart)    
        else:
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
        self.data = {}
        self.fileSelected = ""
        self.files = []
        self.patterns = []
        self.re = "TNS-\d{5}: .*"
        self.patterns.append(self.re)
        
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 400)
        self.setWindowTitle("Performance Analyzer")
        self.setWindowIcon(QIcon('icon.png'))

        extractAction = QAction("&Browse Log File", self)
        extractAction.setShortcut("Ctrl+B")
        extractAction.setStatusTip('Select Appropriate Log File')
        extractAction.triggered.connect(self.file_select)

        multifileAction = QAction("&Open multiple files", self)
        multifileAction.setStatusTip('Select Multiple Log Files At Once')
        multifileAction.triggered.connect(self.multi_file_select)

        importPatAction = QAction("&Import Patterns", self)
        importPatAction.setStatusTip('Import Patterns from file')
        importPatAction.triggered.connect(self.pat_import)

        savePatAction = QAction("&Save Pattern List", self)
        savePatAction.setStatusTip('Save Current Pattern List to File')
        savePatAction.triggered.connect(self.pat_save)

        saveChartAction = QAction("&Save Chart", self)
        saveChartAction.setStatusTip('Save Chart As Image')
        saveChartAction.triggered.connect(self.save_chart)
        
        customRE = QAction("&Enter custom expression", self)
        customRE.setStatusTip('Enter a custom regular expression')
        customRE.triggered.connect(self.custRE)

        clearLogList = QAction("&Clear log list", self)
        clearLogList.setStatusTip('Clears all logs from the list')
        clearLogList.triggered.connect(self.clear_logs)

        clearPatList = QAction("&Clear pattern list", self)
        clearPatList.setStatusTip('Clears all patterns from the list')
        clearPatList.triggered.connect(self.pat_clear)        
        
        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(self.close_application)

        smailAction = QAction("&Send Mail", self)
        smailAction.triggered.connect(self.send_mail)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        optionMenu = mainMenu.addMenu('&Options')
        networkMenu = mainMenu.addMenu('&Network')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(multifileAction)
        fileMenu.addAction(importPatAction)
        fileMenu.addAction(savePatAction)
        fileMenu.addAction(saveChartAction)
        fileMenu.addAction(exitAction)
        optionMenu.addAction(customRE)
        optionMenu.addAction(clearLogList)
        optionMenu.addAction(clearPatList)
        networkMenu.addAction(smailAction)
        self.design()

    def design(self):
        flLbl = QLabel("Log File:",self)
        flLbl.move(20, 35)

        patLbl = QLabel("Pattern:",self)
        patLbl.move(20, 75)

        btn = QPushButton("Analyze", self)
        btn.clicked.connect(self.analyze)
        btn.resize(btn.minimumSizeHint())
        btn.move(20,120)

        chartRefreshBtn = QPushButton("Show Histogram", self)
        chartRefreshBtn.clicked.connect(self.histogram)
        chartRefreshBtn.resize(chartRefreshBtn.minimumSizeHint())
        chartRefreshBtn.move(20,230)

        self.flCB = QComboBox(self)
        self.flCB.move(150, 35)
        self.flCB.addItem("Add log file(s) using file menu")
        self.flCB.resize(300,chartRefreshBtn.height())
        self.flCB.currentIndexChanged.connect(self.file_changed)

        self.patCB = QComboBox(self)
        self.patCB.move(150, 75)
        self.patCB.addItem("TNS-\d{5}: .*")
        self.patCB.resize(300,chartRefreshBtn.height())
        self.patCB.currentIndexChanged.connect(self.pat_changed)

        yrlbl = QLabel("Year-Month",self)
        yrlbl.move(20, 170)
        
        self.yearSel = QLineEdit(str(datetime.datetime.now().year),self)
        self.yearSel.move(120, 177)
        self.yearSel.resize(self.yearSel.minimumSizeHint())

        self.monthCB = QComboBox(self)
        self.monthCB.move(200, 177)
        self.monthCB.resize(self.monthCB.minimumSizeHint())
        self.monthCB.addItems(["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"])

        self.errorCB = QComboBox(self)
        self.errorCB.move(150, 230)
        self.errorCB.addItem("Select Error Category from here")
        self.errorCB.resize(300,chartRefreshBtn.height())
        
        
        self.chbox1 = QCheckBox("Histogram", self)
        self.chbox1.move(120, 120)

        self.chbox2 = QCheckBox("Prepare Weekly", self)
        self.chbox2.move(20, 270)

        self.chbox3 = QCheckBox("Combine Files", self)
        self.chbox3.move(220, 120)
        self.chbox3.setChecked(True)
        
        self.weekCB = QComboBox(self)
        self.weekCB.move(150, 270)
        self.weekCB.addItem("Select Week from here")
        self.weekCB.resize(300,chartRefreshBtn.height())
        self.weekCB.addItems(["Week 1: Day 1 - 7", "Week 2: Day 8 - 14", "Week 3: Day 15 - 21", "Week 4: Day 22 - 28", "Week 5: Day 29 - 31"])
        
        self.show()
        
    def custRE(self):
        text, okPressed = QInputDialog.getText(self, "Custom RE","Enter a valid Regular Expression", QLineEdit.Normal, "")
        if okPressed and text != '':
            print("Added Regular Expression:",text)
            self.patterns.append(text)
            self.refresh_patterns()
    def histogram(self):
        self.chartWindow = QMainWindow()
        self.chartWindow.setWindowTitle("Frequency Charts")
        self.chartWindow.resize(800, 600)


        arg = None
        self.ch = None
        if(self.chbox2.checkState()):            
            self.ch = BarChart(self.data, (self.yearSel.text(), self.monthCB.currentText()), self.weekCB.currentIndex())
            #self.ch = BarChart(self.data, ("2017", "MAY"), 3)
        else:
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
            self.data = {}
            if(self.chbox3.checkState()):
                for f in self.files:   
                    inspect(f, self.re, self.chbox1.checkState(), self.data)
            else:
                inspect(self.fileSelected, self.re, self.chbox1.checkState(), self.data)

            ocDict = self.data
            
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
            self.table.setRowCount(len(ocDict)+1)
            self.table.setColumnCount(2)
            self.table.setColumnWidth(0, w_width/2)
            self.table.setColumnWidth(1, w_width/2)

            self.table.setHorizontalHeaderLabels("Error Name;Frequency;".split(";"))

            curRow = 0
            total = 0
            # set data
            for i in ocDict:
                self.table.setItem(curRow,0, QTableWidgetItem(i))
                self.table.setItem(curRow,1, QTableWidgetItem(str(ocDict[i]["count"])))
                total += ocDict[i]["count"]
                curRow += 1
            self.table.setItem(curRow,0, QTableWidgetItem("Total Issues"))
            self.table.setItem(curRow,1, QTableWidgetItem(str(total)))
            self.window.show()
            self.table.show()
    def file_select(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select a log file", "","All Files (*);;Log Files (*.log)", options=options)
        if fileName:
            print("File Selected:",fileName)
            self.files.append(fileName)
        self.refresh_files()
    def multi_file_select(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Select a log file", "","All Files (*);;Log Files (*.log)", options=options)
        if fileNames:
            print("Files Selected:",fileNames)
            self.files += fileNames
        self.refresh_files()
    def clear_logs(self):
        self.files = []
        self.refresh_files()
    def close_application(self):
        #print("whooaaaa so custom!!!")
        sys.exit()


    def pat_changed(self):
        self.re = self.patCB.currentText()
        pass
    def pat_clear(self):
        self.patterns = []
        self.refresh_patterns()

    def pat_import(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select a pattern file", "","All Files (*);;Pattern Files (*.pat)", options=options)
        if fileName:
            print("Pattern File Selected:",fileName)
            f = open(fileName)
            s = f.readline()
            self.patterns += s.split("~")
        self.refresh_patterns()
    def pat_save(self):
        text, okPressed = QInputDialog.getText(self, "Save Patterns","File Name", QLineEdit.Normal, "")
        s = "~".join(self.patterns)
        if okPressed and text != '':
            f = open(text+".pat","w")
            f.write(s)
            print("Pattern File Saved:",text)
            
    def file_changed(self):
        self.fileSelected = self.flCB.currentText()

    def refresh_files(self):
        self.flCB.clear()
        
        if self.files:
            self.flCB.addItems(self.files)
            
            self.flCB.setCurrentIndex(len(self.files)-1)
            self.fileSelected = self.files[-1]
            
        else:
            self.flCB.addItem("Add log file(s) using file menu")
            self.fileSelected = ""

    def refresh_patterns(self):
        self.patCB.clear()

        if self.patterns:
            self.patCB.addItems(self.patterns)
            
            self.patCB.setCurrentIndex(len(self.patterns)-1)
            self.re = self.patterns[-1]
            
        else:
            self.patCB.addItem("Import patterns using file menu or enter custom using Options")
            self.re = ""
        

    def save_chart(self):
        print("Rendering and Saving Image")
        self.im = QImage(1600,1200, QImage.Format_ARGB32)
        self.painter = QPainter(self.im)
        self.ch.cv.render(self.painter)
        fileName = ""
        print("Creating File Name")
        if(self.chbox2.checkState()):
            fileName = self.yearSel.text()+"-"+self.monthCB.currentText()+"-Week-"+str(self.weekCB.currentIndex())+".jpg"
        else:   fileName = self.yearSel.text()+"-"+self.monthCB.currentText()+".jpg"
        self.im.save(fileName)
        print("Image Saved")
        self.painter.end()
        return

    def send_mail(self):
        self.mailer = Mailer()
# Run Everything
##def main():
##    app = QApplication(sys.argv)
##    print("Creating Primary Window Object")
##    GUI = Window()
##    print("Primary Window Object Created")
##    app.exec_()
##
##if __name__ == '__main__':
##    main()

app = QApplication(sys.argv)
print("Creating Primary Window Object")
GUI = Window()
print("Primary Window Object Created")
app.exec_()
