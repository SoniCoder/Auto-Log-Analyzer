import sys

from core import *

def main():
    app = QApplication(sys.argv)
    USE_GUI = False
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        USE_GUI = True
    if USE_GUI:
        print("Creating Primary Window Object")
        GUI = Window()
        print("Primary Window Object Created")
        sys.exit(app.exec_())
    else:
        analyze()
        histogram()
        save_chart()

if __name__ == '__main__':
    main()
