import view
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import requests
from datetime import datetime


class Messenger(QtWidgets.QMainWindow, view.Ui_Form):
    def __init__(self):
        super(Messenger, self).__init__()
        self.setupUi(self)
        self.last = 0
        self.pushButton.clicked.connect(self.send_message)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)
        self.lastuser = " "
        self.color = QColor(220,235,235)
        self.elsecolor = QColor(235,235,220)
        self.message.returnPressed.connect(self.send_message)


    def show_messages(self, message):
        current_message = QtWidgets.QListWidgetItem()
        if message['name'] == self.lastuser:
            current_message.setBackground((self.color))
        else:
            current_message.setBackground(self.elsecolor)
            self.color, self.elsecolor = self.elsecolor, self.color
            self.lastuser = message['name']
        time = datetime.fromtimestamp(message['time'])
        current_message.setText(f"{message['name']} at {time.strftime('%H:%M')} :\n{message['text']}")
        self.messages.addItem(current_message)

    def get_messages(self):
        try:
            response = requests.get(url='http://127.0.0.1:5000/messages', params={'last': self.last})
        except:
            return
        messages = response.json()['messages']
        for message in messages:
            self.show_messages(message)
            self.last = message['time']
            self.messages.scrollToBottom()

    def send_message(self):
        name = self.name.text()
        text = self.message.text()
        if len(name) > 0 and len(text) > 0:
            try:
                _ = requests.post(url='http://127.0.0.1:5000/send', json={'name': name, 'text': text})
            except:
                return
            self.get_messages()
            self.message.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    messenger = Messenger()
    messenger.show()
    app.exec()
