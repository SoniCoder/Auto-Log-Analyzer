import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re

f = open("alert_mydprd.log")

ocDict = {}

mainPattern = re.compile("TNS-\d{5}: .*")

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

app 	= QApplication(sys.argv)
window = QWidget()
table 	= QTableWidget(window)
tableItem = QTableWidgetItem()
mb = QMenuBar(window)

# initiate UI
w_width = 800
w_height = 300
mb_height = 40

window.setWindowTitle("Error Frequency Table")
window.resize(w_width, w_height)
table.move(0, mb_height)
table.resize(w_width, w_height-mb_height)
table.setRowCount(len(ocDict))
table.setColumnCount(2)
table.setColumnWidth(0, w_width/2)
table.setColumnWidth(1, w_width/2)

table.setHorizontalHeaderLabels("Error Name;Frequency;".split(";"))

curRow = 0

# set data
for i in ocDict:
    table.setItem(curRow,0, QTableWidgetItem(i))
    table.setItem(curRow,1, QTableWidgetItem(str(ocDict[i])))
    curRow += 1

# show table
window.show()
app.exec_()
