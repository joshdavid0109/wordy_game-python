## _**WORDY GAME**_

## AUTHORS
AGBAYANI, Rey John

ANDAYA, Trisha

DAVID, Joshua Daniel 

DE GUZMAN, Alastair Zeph

DOMANTAY, Darren Franz

TARLIT, Ariel Jr.

VILLALOBOS, Maervin

## Necessary files

- [ ] [Python](https://www.python.org/downloads/) 
- [ ] [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) 

```
Install the latest version of the links provided
```

## Python Installation
1. After installing Python,
2. Click on the "Downloads" tab located on the top navigation bar.
3. On the Downloads page, you will see the latest version of Python available for download. Choose the version that corresponds to your operating system (e.g., Windows, macOS, or Linux). It's recommended to download the stable release, which is usually displayed prominently.
4. Click on the download link for the selected version of Python. You will be redirected to the download page.
5. Scroll down the page and locate the installer appropriate for your operating system. For Windows, download the executable installer (e.g., Python 3.9.5.exe). For macOS, download the macOS installer (e.g., Python 3.9.5 macOS 64-bit installer). For Linux, the process may vary depending on your distribution, but you can usually find Python in the package manager or download the source code from the Python website.
6. Once the installer file is downloaded, run it to start the installation process.
7. On the installation wizard, make sure to check the box that says "Add Python to PATH" (Windows) or "Install Python to the standard locations" (macOS). This step ensures that Python is accessible from the command line or terminal.
8. Proceed with the installation by following the on-screen instructions. You can typically accept the default settings unless you have specific requirements.
9. After the installation is complete, open the command prompt (Windows) or terminal (macOS/Linux) and type python --version to verify that Python is installed correctly. You should see the version number of Python displayed.

## PyCharm Installation
1. On the PyCharm homepage, you will see the various editions available for download. Choose the edition that suits your needs (e.g., PyCharm Community or PyCharm Professional). The Community edition is free and offers essential features, while the Professional edition includes additional advanced functionality and requires a license.
2. Click on the "Download" button for your chosen edition. You will be redirected to the download page.
3. On the download page, select the operating system you're using (e.g., Windows, macOS, or Linux). Choose the appropriate version for your OS.
4. Click on the download link to start the download process. The installer file will be saved to your computer.
5. Once the download is complete, locate the installer file and run it.
6. Follow the installation wizard's instructions. You can generally accept the default settings unless you have specific preferences.
7. During the installation, you may be asked to select additional components or configure settings. Make your choices based on your needs or leave them as default.
8. After the installation is complete, you can launch PyCharm from the Start menu (Windows) or the Applications folder (macOS). The first time you run PyCharm, it may prompt you to import settings or customize your preferences.
9. PyCharm will ask you to choose the theme and keymap preferences. You can select the options you prefer or keep the defaults.
10. Once you've completed the initial setup, PyCharm is ready to use.


## Setting up the project
1. Open PyCharm, load the project
2. Edit Run/Debug configurations for main.py (Click Add Configuration on the right top side)
3. Click the add button and look for Python
4. On the script path, type main.py.
5. On the parameters, type

**      -ORBInitRef NameService=corbaname::localhost:9999**
```
Make sure to change the localhost and port(9999) as what is used by the server program.
```
6. Click Apply, then close the window.

## Running the client program
1. Make sure that the orb daemon and java server is running on the server's machine
2. Run main.py, and that's it. Login a registered user and Enjoy the Wordy game!

