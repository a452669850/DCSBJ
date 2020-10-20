import os


if __name__ == '__main__':

    os.system('pyinstaller -n dcsNext bin.py -w --hidden-import passlib.handlers.pbkdf2 --add-data static;static -y')
    # os.system('pyinstaller -n client xps/cleint.py -w --add-data static;static -y')
