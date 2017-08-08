SET PATH=%PATH%;C:\Users\1022285\AppData\Local\Programs\Python\Python35-32\Lib\site-packages\PyQt5\Qt\bin
pyinstaller manage.py --hidden-import=PyQt5 --exclude-module config
copy icon.png dist\manage\ /Y
copy config.py dist\manage\ /Y