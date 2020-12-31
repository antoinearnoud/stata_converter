# stata_converter
This programs converts newer versions of Stata files into older versions.

The user needs to install the packages from `requirements.txt`. To do so, run
```
pip install -r requirements.txt
```
or simply
```
pip install pandas
pip install -U wxPython
```
One might also need `pyinstaller` to create the executable.

To launch the program, run (note the `w` at the end of `python`, this runs wxPython):
```
pythonw converter.py
```

The program let the user choose the file to convert as well as the version of the file (Stata v10, Stata v13 or Stata v14). The new file is saved in the same folder with an extension to the name (`_v10`, `_v13` or `_v14`).
Preview of the program:
![alt text](screenshot.png)

To create the executable, run
```
pyinstaller --onefile --windowed --icon="images\myicon.ico" --name converter.py
```
