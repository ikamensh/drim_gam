from PySide2 import QtCore, QtGui, QtWidgets

from ui.gamecore.GameObject import GameObject
from ui.GamePages.suwidgets.GuiConsole import GuiConsole


class NotifyText(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super(NotifyText, self).__init__()
        self.w = 320
        self.h = 240
        # self.setOpacity(1.0)
        self.setFont(QtGui.QFont("Times", 48, 10, False))
        self.setDefaultTextColor(QtCore.Qt.blue)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerSlot)
        # Связать с gameconfig
        self.setPos(300, 300)
        self.setVisible(False)

    def setText(self, value):
        self.setOpacity(1.0)
        self.setPlainText(str(value))
        self.setVisible(True)
        self.timer.start(500)

    def timerSlot(self):
        self.setOpacity(self.opacity() - 0.1)
        if self.opacity() < 0.3:
            self.setVisible(False)
            self.timer.stop()

class ScreenMenu(QtWidgets.QGraphicsItemGroup):
    """docstring for ScreenMenu."""
    def __init__(self, *arg):
        super(ScreenMenu, self).__init__(*arg)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.gui_console = None
        self.gameRoot = None

    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameconfig = self.gameRoot.cfg
        self.setUpDefaultPosition()

    def showNotify(self, text):
        self.notify.showText(text)

    def setUpDefaultPosition(self):
        self.console_pos = self.gameconfig.dev_size[0] - 320, self.gameconfig.dev_size[1] - 240

    def setUpGui(self):
        self.notify = self.gameRoot.suwidgetFactory.getNotifyText(self.gameRoot)
        self.addToGroup(self.notify)

        self.unitStack = QtWidgets.QGraphicsRectItem(self)
        self.unitStack.setBrush(QtCore.Qt.blue)
        self.unitStack.setPos(0, 0)
        self.active_select = GameObject()
        self.active_select.setPixmap(self.gameconfig.getPicFile('active select 96.png').scaled(64, 64))
        self.active_select.setParentItem(self.unitStack)
        self.active_select.setPos(self.unitStack.x(), self.unitStack.y())
        if not self.gameRoot.level is None:
            self.createUnitStack()
            self.updateUnitStack()

    def createUnitStack(self):
        self.unitStack.items = {}
        i = 0
        for unit in self.gameRoot.level.units.units_at.values():
            item = GameObject(64, 64)
            item.setParentItem(self.unitStack)
            item.setPixmap(unit.pixmap().scaled(64, 64))
            item.setPos(self.unitStack.x() + i* 64, self.unitStack.y())
            item.stackBefore(self.active_select)
            self.unitStack.items[unit.uid] = item
            i+=1

    def setUpConsole(self):
        self.gui_console = GuiConsole(self.gameRoot.game.gamelog)
        self.gui_console.startTimer(50)
        self.gui_console.setTabChangesFocus(False)
        self.gui_console.move(self.console_pos[0], self.console_pos[1])
        self.gui_console.setEnabled(False)
        self.gui_console.resize(320, 240)
        self.scene().addWidget(self.gui_console)

    def rmToUnitStack(self, uid):
        self.unitStack.items[uid].setParentItem(None)
        del self.unitStack.items[uid]
        self.updateUnitStack()


    def updateUnitStack(self):
        units_stack = self.gameRoot.game.turns_manager.managed_units
        w = len(units_stack)
        self.unitStack.rect().setWidth(w * 64)
        i = 0
        #next_unit = my_context.the_game.turns_manager.get_next()
        for bf_unit in units_stack:
            self.unitStack.items[bf_unit.uid].setPos(self.unitStack.x() + i * 64, self.unitStack.y())
            i+=1

    def setDefaultPos(self):
        pos = self.scene().views()[0].mapToScene(self.gameconfig.correct_size[0], self.gameconfig.correct_size[1])
        self.gui_console.move(self.console_pos[0] + pos.x(), self.console_pos[1] + pos.y())
        self.setX(pos.x())
        self.setY(pos.y())

    def updateGui(self):
        self.gui_console.move(self.gameconfig.dev_size[0] - 320, self.gameconfig.dev_size[1] - 240)
