# Youtube-Video-Downloader
YouTube Video Downloader with Python
<p align="center">
<img src="https://user-images.githubusercontent.com/60680749/151407098-bf212882-7673-4642-9e6d-8b546264f065.png" width="250" height="250">
<img src="https://user-images.githubusercontent.com/60680749/151404941-fff3e7b5-9a2d-4ad0-bbef-9af3d2cbbf9b.png" width="250" height="250">
<img src="https://user-images.githubusercontent.com/60680749/151404957-e789f80f-f41e-4e04-9e4c-8bae768bfcee.png" width="250" height="250">
</p>
A program made with Python to download YouTube videos in any resolution or audio only format.
The pytube library was used for the program.\
**What is pytube?**\
Pytube is a lightweight, Pythonic, dependency-free, library (and command-line utility) for downloading YouTube Videos.

# Requirements

Python3 libraries
````python
pip install pytube
pip install pyqt5-tools
pip install PyQt5Designer
pip install Pillow
pip install urllib3
````
# Possible errors you may encounter

## Pytube: urllib.error.HTTPError: HTTP Error 410: Gone
Execute the commands below.

```python
python -m pip install --upgrade pytube
python -m pip install git+https://github.com/Zeecka/pytube@fix_1060
````

## Pytube library - Receiving "pytube.exceptions.RegexMatchError: regex pattern" error when attempting to access video data

Replace the var.regex line in the cipher.py file with the code

```python
var_regex = re.compile(r"^$*\w+\W")
````

If you still get an error after trying the solutions, replace the contents of the file below with cipher.py
[cipher.txt](https://github.com/engincandanabas/Youtube-Video-Downloader/files/7952552/cipher.txt)

