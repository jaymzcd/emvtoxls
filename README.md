# EmailVision XML To Excel Convertor

Convert Emailvision XML exports of member lists to native Microsoft XLS files.
This uses lxml and a custom file-like object to handle large (>100Mb) files without
erroring on malformed content - so far I've noticed that ampersands are passed
through without being converted to an entity.

A command line interface and TK GUI are provided. By using PyInstaller a standalone
exe can be generated - current build provided in dist.

![screenshot-gui](http://i.imgur.com/MGt4wvZ.png)

![screenshot-cli](http://i.imgur.com/LNKwl5z.png)

For no other reason that to make @ninjaneenaa's life a bit easier.

## Resources

* Reading XML into Excel directly: http://office.microsoft.com/en-gb/excel-help/viewing-an-xml-file-in-excel-HA001034645.aspx
* Python EXE packaging: http://www.py2exe.org/index.cgi/Tutorial#Step51
* EXE Installer: http://nsis.sourceforge.net/Main_Page
* Simple spreadsheet writing: https://github.com/python-excel/xlwt/blob/master/xlwt/examples/simple.py
* TKInter & Threads: http://stackoverflow.com/questions/15323574/how-to-connect-a-progress-bar-to-a-function
