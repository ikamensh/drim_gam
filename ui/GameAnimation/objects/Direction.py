from PySide2 import QtCore, QtWidgets

class Direction(QtCore.QObject, QtWidgets.QGraphicsPixmapItem):
    """docstring for ."""
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsPixmapItem.__init__(self, parent)
        self.setProperty('qangel', 0.0)

    def setQAngel(self, angel):
        self.setRotation(angel)
