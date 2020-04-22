pyinstaller pylogger.py --onefile --noconsole
rmdir /Q /S build
rmdir /Q /S __pycache__
del pylogger.spec  

