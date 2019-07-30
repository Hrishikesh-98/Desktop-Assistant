import sys, os, sqlite3, time, subprocess
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from zipfile import *

global extension
extension = list()
extension.append("exe")
extension.append("EXE")

class extract:
    def __init__(self, path):
        print("Extracting setup.zip")
        file_name = ".\setup.zip"
        zip_archive = ZipFile(file_name)
        names = zip_archive.namelist()
        for name in names:
            print("Extracting " + name)
            zip_archive.extract(name,path)

class create_db:
    def __init__(self,path,extens,install):
        path = path + "\\dist\\ui\\mp4videos.db"
        connection = sqlite3.connect(path)
        install.textEdit.setEnabled(False)
        drives = [chr(x) + ":" for x in range(65, 90) if os.path.exists(chr(x) + ":")]
        to_print = ""
        for i in range(len(drives)):
            #for r, d, f in os.walk(drives[i] + "//"):
            for r,d,f in os.walk(("A://vids")):
                for files in f:
                    if "C://Windows" in os.path.join(r,files):
                        pass
                    else:
                        try:
                            rev = files[::-1]
                            name = rev.split('.',1)[1]
                            name = name[::-1]
                            rev = rev.split(".",1)[0]
                            rev = rev[::-1]
                            if rev in extens:
                                ext = rev
                                path = os.path.join(r, files)
                                name = name.lower()
                                print(name + " " + path + " " + ext)
                                #install.textEdit.setText(name + " " + path + " " + ext)
                                query = 'INSERT INTO paths values("' + name + '","' + path + '", "' + ext + '");'
                                connection.execute(query)
                                connection.commit()
                        except:
                            pass
            install.nextButton.setEnabled(True)

class MainPage(QWidget):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.resize(568, 326)
        self.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 561, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 571, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 571, 41))
        self.label_2.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 571, 41))
        self.label_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 120, 571, 201))
        self.label_4.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(370, 260, 75, 23))
        self.closeButton.setObjectName("pushButton")
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(470, 260, 75, 23))
        self.nextButton.setObjectName("pushButton_2")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(self)
        self.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "                 Setup Your Virtual Assistant"))
        self.label_2.setText(_translate("MainWindow", "Welcome to the setup of your virtual assistant"))
        self.label_3.setText(_translate("MainWindow", " Follow the steps to setup the assistant and make your boring stuff automated."))
        self.closeButton.setText(_translate("MainWindow", "Cancel"))
        self.nextButton.setText(_translate("MainWindow", "Next"))

class directory(QWidget):
    def __init__(self, parent=None):
        super(directory, self).__init__(parent)
        self.setupui()

    def setupui(self):
        self.resize(568, 326)
        self.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 561, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 571, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 571, 41))
        self.label_2.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 571, 121))
        self.label_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 200, 571, 201))
        self.label_4.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.ext = QtWidgets.QTextEdit(self.centralwidget)
        self.ext.setGeometry(QtCore.QRect(10, 80, 300, 50))
        self.ext.setStyleSheet("background-color: rgb(255,255,255);")
        self.ext.setText("mp4 mp3 avi mkv pdf docx doc xls ppt pptx wav mpeg")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(280, 270, 75, 23))
        self.closeButton.setObjectName("pushButton")
        self.installButton = QtWidgets.QPushButton(self.centralwidget)
        self.installButton.setGeometry(QtCore.QRect(470, 270, 75, 23))
        self.installButton.setObjectName("pushButton_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 200, 47, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 200, 391, 20))
        self.lineEdit.setStyleSheet("color: rgb(0, 0, 0);\n"
                                    "background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(370, 270, 75, 23))
        self.backButton.setObjectName("pushButton_3")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(460, 200, 75, 21))
        self.browseButton.setObjectName("pushButton_4")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.browseButton.clicked.connect(self.browse)
        self.retranslateUi(self)

    def addExtension(self):
        exte = self.ext.toPlainText()
        extensions = exte.split(" ", exte.count(" "))
        print(extensions)
        for i in range(len(extensions)):
            ext_lower = str(extensions[i]).lower()
            extension.append(ext_lower)
            ext_upper = str(extensions[i]).upper()
            extension.append(ext_upper)

    def get_path(self):
        self.path = self.lineEdit.text()

    def browse(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a folder")
        self.lineEdit.setText(str(filename))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "                 Setup Your Virtual Assistant"))
        self.label_2.setText(_translate("MainWindow", "Write Files extension you want the assistant to have access to"
                                                      " (other than exe and without '.' )"))
        self.label_3.setText(_translate("MainWindow", "Select the directory to install assistant"))
        self.closeButton.setText(_translate("MainWindow", "Cancel"))
        self.installButton.setText(_translate("MainWindow", "Install"))
        self.label_5.setText(_translate("MainWindow", "Path:"))
        self.backButton.setText(_translate("MainWindow", "Back"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))


class install(QWidget):
    def __init__(self, parent=None):
        super(install, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.resize(568, 326)
        self.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 561, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 571, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 571, 41))
        self.label_2.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 571, 41))
        self.label_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 120, 571, 201))
        self.label_4.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(370, 270, 75, 23))
        self.closeButton.setObjectName("pushButton")
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(470, 270, 75, 23))
        self.nextButton.setObjectName("pushButton_2")
        self.nextButton.setEnabled(False)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 90, 541, 161))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "                 Setup Your Virtual Assistant"))
        self.label_2.setText(_translate("MainWindow", "Seting up your assistant. This might take some time:"))
        self.closeButton.setText(_translate("MainWindow", "Cancel"))
        self.nextButton.setText(_translate("MainWindow", "Next"))


class finish(QWidget):
    def __init__(self, parent=None):
        super(finish, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.resize(568, 326)
        self.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 561, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 571, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 571, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 571, 41))
        self.label_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 120, 571, 201))
        self.label_4.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(370, 270, 75, 23))
        self.closeButton.setObjectName("pushButton")
        self.finishButton = QtWidgets.QPushButton(self.centralwidget)
        self.finishButton.setGeometry(QtCore.QRect(470, 270, 75, 23))
        self.finishButton.setObjectName("pushButton_2")
        self.createShortcut = QtWidgets.QCheckBox(self.centralwidget)
        self.createShortcut.setGeometry(QtCore.QRect(50, 130, 101, 17))
        self.createShortcut.setObjectName("checkBox")
        self.launch = QtWidgets.QCheckBox(self.centralwidget)
        self.launch.setGeometry(QtCore.QRect(50, 170, 70, 17))
        self.launch.setObjectName("checkBox_2")
        self.open_inst = QtWidgets.QCheckBox(self.centralwidget)
        self.open_inst.setGeometry(QtCore.QRect(50, 210, 70, 17))
        self.open_inst.setObjectName("checkBox_3")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "                 Setup Your Virtual Assistant"))
        self.label_2.setText(_translate("MainWindow", "     Finished installing assistant"))
        self.closeButton.setText(_translate("MainWindow", "Cancel"))
        self.finishButton.setText(_translate("MainWindow", "Finish"))
        self.createShortcut.setText(_translate("MainWindow", "Create Shortcut"))
        self.launch.setText(_translate("MainWindow", "Launch"))
        self.open_inst.setText(_translate("MainWindow", "Open Instructions"))

    def finishit(self, path):
        if self.launch.isChecked():
            subprocess.Popen(path + "\\dist\\ui\\prishi.exe")
        if self.open_inst.isChecked():
            os.popen(path + "\\instruction.txt")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prishi")
        self.setWindowIcon(QtGui.QIcon(".\\icons\\prishi.png"))
        self.main = MainPage(self)
        self.main.nextButton.clicked.connect(self.show_dir)
        self.main.closeButton.clicked.connect(self.closeApp)
        self.dir = directory(self)
        self.dir.installButton.clicked.connect(self.show_insta)
        self.dir.backButton.clicked.connect(self.show_main)
        self.dir.hide()
        self.insta = install(self)
        self.insta.nextButton.clicked.connect(self.show_fin)
        self.insta.closeButton.clicked.connect(self.closeApp)
        self.insta.hide()
        self.finish = finish(self)
        self.finish.finishButton.clicked.connect(self.finished)
        self.finish.hide()
        self.main.show()
        self.show()

    def finished(self):
        self.finish.finishit(self.dir.path)
        self.closeApp()

    def closeApp(self):
        #question message box
        reply = QtWidgets.QMessageBox.question(self, "Close Window", "Are you sure", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                     QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()

    def all_hide(self):
        self.main.hide()
        self.dir.hide()
        self.insta.hide()
        self.finish.hide()

    def show_dir(self):
        self.all_hide()
        self.dir.show()

    def show_insta(self):
        if self.dir.lineEdit == '' or self.dir.ext == '':
            QtWidgets.QMessageBox.about(self,'Make sure you have entered all details')
        self.dir.get_path()
        if os.path.isfile(self.dir.path + "\\dist\\ui\\ui.exe"):
            print("in2")
            self.all_hide()
            self.dir.get_path()
            self.dir.addExtension()
            self.insta.show()
            create_db(self.dir.path, extension, self.insta)
        else:
            print("in3")
            self.all_hide()
            self.dir.get_path()
            self.dir.addExtension()
            self.extra()

    def extra(self):
        extra = extract(self.dir.path)
        create = create_db(self.dir.path, extension, self.insta)
        self.show_fin()

    def show_fin(self):
        self.all_hide()
        self.finish.show()

    def show_main(self):
        self.all_hide()
        self.main.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())