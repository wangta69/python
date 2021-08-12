from PyQt5 import QtCore, QtGui, QtWidgets

class HelperMessageOverlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HelperMessageOverlay, self).__init__(parent)

        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)

        self.font_size = 13
        self.empty_json_message = "Drag and drop a JSON file, \n" \
                                  "or drag in JSON readable data, \n" \
                                  "or paste data from clipboard."

        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(100, 100, 100, 100)))
        painter.setFont(QtGui.QFont("seqoe", self.font_size))
        painter.drawText(event.rect(), QtCore.Qt.AlignCenter, self.empty_json_message)
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))