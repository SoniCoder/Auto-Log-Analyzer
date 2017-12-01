"""
AUTHOR: Hritik Soni

Description: Executable Module of the project

Pass this module to python without argument "gui" to run the program in GUI manual mode.

Pass this module to python without any arguments to run the program in automatic mode.

Example:

python manage.py gui
python manage.py

"""


import datetime #Datetime module for Mail Scheduler
import getpass #Retrieve Mail Password from user in commandline mode
import sys

from core import *

def main():
    app = QApplication(sys.argv)
    USE_GUI = False
    #print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == "gui" and not globals()['FORCE_AUTO']:
        USE_GUI = True
    if USE_GUI:
        print("Creating Primary Window Object")
        GUI = Window()
        print("Primary Window Object Created")
        sys.exit(app.exec_())
    else:
        """
        The following code is responsible for automatic mode.
        It also has implementation for the scheduler
        """
        end_time = datetime.datetime.now() + datetime.timedelta(minutes = globals()['MAX_DURATION'])
        last_time = datetime.datetime.min
        time_delta = datetime.timedelta(minutes = globals()['TIME_DELTA'])
        while(datetime.datetime.now() <= end_time):
            if(datetime.datetime.now() - last_time > time_delta):
                last_time = datetime.datetime.now()
                print("Executing Procedure")                
                analyze()
                histogram()
                fileName = save_chart()
                if(not globals()["PASSWORD"]): globals()["PASSWORD"] = getpass.getpass("Password:")
                send(globals()["PASSWORD"], [fileName])
if __name__ == '__main__':
    main()
