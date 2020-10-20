from DcsUi.InitProject import Ui_InitProject
from DcsUi.LogWindow import LogWindow
from PyQt5 import QtWidgets
from static.Stylesheets.ImportQss import load_stylesheet_pyqt5
import sys

if __name__ == '__main__':
    sys.excepthook = LogWindow.errorLog
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_InitProject()
    app.setStyleSheet(load_stylesheet_pyqt5(style="style_Classic"))
    mainWindow.show()
    sys.exit(app.exec_())
