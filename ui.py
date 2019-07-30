from PyQt5.QtWidgets import (QPushButton, QLineEdit, QLabel, QApplication,
                             QWidget, QMainWindow, QHBoxLayout, QGridLayout, QTextEdit, QFrame)
import pyaudio
import wave
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt5.QtCore import QPropertyAnimation, Qt
import sys
import speech_recognition as sr
import win32com.client as wincl
from PIL import Image
import datetime
from process_language import Process
#from get_answer import *
from nlp_get_answer import *

objects = list()
class do_it:
    def speak(self,audio):
        print('Computer: ' + audio)
        #engine.say(audio)
        #engine.runAndWait()
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(audio)

    def greetMe(self):
        currentH = int(datetime.datetime.now().hour)
        if currentH >= 0 and currentH < 12:
            self.speak('Good Morning! I am your digital assistant Prishi!')

        if currentH >= 12 and currentH < 18:
            self.speak('Good Afternoon! I am your digital assistant Prishi!')

        if currentH >= 18 and currentH != 0:
            self.speak('Good Evening! I am your digital assistant Prishi!')

        self.speak('How may I help you?')
        process = Process()
        global objects
        objects = process.fit_model()

    def myCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Listening...")
            #r.pause_threshold = 1
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')

        except sr.UnknownValueError:
            self.speak('Sorry sir! I didn\'t get that! Try typing the command!')
            query = ""

        return query


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.r = sr.Recognizer()
        self.setFixedSize(400,500)
        self.setMaximumHeight(500)
        self.setMaximumWidth(300)
        self.setWindowTitle("Prishi")
        self.vbox = QGridLayout()
        self.setLayout(self.vbox)
        self.mainframe = QFrame()
        self.setWindowIcon(QIcon(".\icons\prishi.png"))
        self.mainframe.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        mic = Image.open(".\icons\mic.png")
        mic = mic.resize((63,60), Image.ANTIALIAS)
        mic.save("./temp.png", mic.format)
        pixmap = QPixmap("./temp.png")
        self.label = QLabel(self)
        self.label.setFixedSize(65,60)
        self.label.move(160,170)
        self.label.setPixmap(pixmap)
        self.vbox.addWidget(self.mainframe)
        self.mainframe.setFixedSize(380, 400)
        self.button = QPushButton()
        self.text = QLineEdit(self)
        self.text.setFixedSize(300, 50)
        self.textarea = QTextEdit(self)
        self.textarea.setFixedSize(300,200)
        self.textarea.hide()
        self.textarea.setFixedSize(200, 200)
        self.textarea.move(90, 140)
        self.button.setIcon(QIcon(".\icons\prishi.png"))
        self.hbox = QHBoxLayout()
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Raised | QFrame.WinPanel)
        self.frame.setLayout(self.hbox)
        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.text)
        self.vbox.addWidget(self.frame)
        self.frame.move(50,350)
        self.button.setFixedSize(50,50)
        self.button.pressed.connect(self.hidetext)
        self.button.released.connect(self.answer)
        self.text.returnPressed.connect(self.textanswer)
        self.show()

    def play_audio(self, filename):
        chunk = 512
        wf = wave.open(filename, "rb")
        pa = pyaudio.PyAudio()

        stream = pa.open(
            format=pa.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data_stream = wf.readframes(chunk)

        while data_stream:
            stream.write(data_stream)
            data_stream = wf.readframes(chunk)

        stream.close()
        pa.terminate()

    def record(self):
        self.play_audio("./audio/start.wav")
        try:
            self.query = do.myCommand()
            self.text.setText(self.query)
            start = self.query.split(" ")[0]
            if start == 'run':
                pass
            else:
                self.query = self.query.lower()
        except ValueError:
            do.speak("You are not connected to the internet, try typing your command")
            self.query = ""

    def answer(self):
        global objects
        self.play_audio("./audio/end.wav")
        if self.query in ["quit", "exit", "close", "bye", "goodbye"]:
            do.speak("Good bye")
            global running
            running = False
            sys.exit()
        elif self.query:
            answers = find_answer()
            answer = answers.answers(do,self.query,self,objects[0],objects[1])
            if answer is not 0:
                if "prishi" in answer:
                    try:
                        answer = answer.split("prishi")[1]
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                    except:
                        #answer = answer.split("prishi")[1]
                        #answer = str(answer)
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                        self.text.setText(str(answer))
                else:
                    try:
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                        do.speak(answer)
                    except:
                        answer = str(answer)
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                        self.text.setText(str(answer))

    def textanswer(self):
        global objects
        self.query = self.text.text()
        start = self.query.split(" ")[0]
        if start == 'run':
            pass
        else:
            print("in")
            self.query = self.query.lower()
        if self.query in ["quit", "exit", "close", "bye", "goodbye"]:
            do.speak("Good bye")
            global running
            running = False
            sys.exit()
        elif self.query:
            answers = find_answer()
            answer = answers.answers(do,self.query,self,objects[0],objects[1])
            if answer is not 0:
                if "prishi" in answer:
                    try:
                        answer = answer.split("prishi")[1]
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                    except:
                        #answer = answer.split("prishi")[1]
                        #answer = str(answer)
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                        self.text.setText(str(answer))
                else:
                    try:
                        self.label.hide()
                        self.textarea.show()
                        self.textarea.setText(str(answer))
                        do.speak(answer)
                    except:
                        answer = str(answer)
                        self.label.show()
                        self.textarea.hide()
                        self.textarea.setText(str(answer))
                        self.text.setText(str(answer))

    def hidetext(self):
        self.textarea.hide()
        self.label.show()
        self.record()

    def hidefromtext(self):
        self.textarea.hide()
        self.label.show()
        self.textanswer()


if __name__ == '__main__':
    do = do_it()
    app = QApplication(sys.argv)
    w = Window()
    do.greetMe()
    sys.exit(app.exec_())