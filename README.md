# lattes_download

This repository contains the code for download a set of lattes curriculum through a vector of id_cnpq. Note that this project was developed on PyCharm IDE. Thus, use PyCharm IDE for better experience.

## Prerequisities

Create "outputs" directory in the root directory if not created automatically. Also, you must install the following prerequisites:

* [Selenium](https://selenium-python.readthedocs.io/)
* [Pydub](https://pypi.org/project/pydub/)
* [Speech recognition](https://pypi.org/project/SpeechRecognition/)

## Run

* git clone https://github.com/regicsf2010/lattes_download.git
* cd lattes_download
* open Pycharm IDE on main.py


```diff
- Please note that this robot will search for a directory called 'outputs'. Each curriculum will be placed in this named directory. Thus, do not forget to create it.
```

## Instructions for Windows O.S.
* In the 'main.py', please change 'path_to_download' variable to use symbol '\' instead of '/'
* Also, add the following line to the option object: 'options.binary_location = r'C:\<path_to_firefox>\Mozilla Firefox\firefox.exe'
* Install ffmpeg and add '<path_to_ffmpeg>\bin' folder to the Environment Variables


## Contact

[Reginaldo Santos](http://lattes.cnpq.br/9157422386900321) - [regicsf2010@gmail.com](regicsf2010@gmail.com)

## 🙏 Donate

If you found this project useful, please contribute:

* Pix-key: c3b63d33-316f-422e-928a-7dd421a0f1b9

