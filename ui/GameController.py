from battlefield import Cell
from PySide2 import QtCore, QtGui, QtWidgets


class GameController:
    def __init__(self,  game):
        """
        last_point = Cell() -- последняя точка, на которую указывает игрок
        """
        self.the_game = game

        self.gameRoot = None
        self.tr = QtGui.QTransform()

        self.cursor = QtWidgets.QGraphicsEllipseItem(-10, -10, 20, 20)

        self.last_point = Cell(0, 0)
        self.selected_point = Cell(0, 0)


    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.cfg = self


    def setUp(self, world, units, middleLayer):
        self.world = world
        self.units = units
        self.middleLayer = middleLayer

    def moveCursor(self, newPos):
        self.cursor.setX(newPos.x())
        self.cursor.setY(newPos.y())

    def mouseMoveEvent(self, e):
        """ Метод перехватывает событие движение мыши
        """
        newPos = self.view.mapTogameRoot.scene(e.x(), e.y())
        self.moveCursor(newPos)
        self.itemSelect(newPos)

    def mousePressEvent(self, e):
        self.the_game.ui_order(self.last_point.x, self.last_point.y)
        self.selected_point.x, self.selected_point.y = self.last_point.x, self.last_point.y
        self.middleLayer.showSelectedItem(self.selected_point.x, self.selected_point.y)

    def keyPressEvent(self, e):
        pass

    def wheelEvent(self, e):
        """ Метод перехватывает событие мышки скролл, скролл больше 0 зумм +,
        скролл меньше нуля зумм -
        """
        if e.delta() > 0.0:
            self.zoomIn()
        elif e.delta() < 0.0:
            self.zoomOut()

    def zoomIn(self):
        self.tr.scale(1.05, 1.05)
        self.world.setTransform(self.tr)
        self.middleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def zoomOut(self):
        self.tr.scale(1/1.05, 1/1.05)
        self.world.setTransform(self.tr)
        self.middleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def moveScene(self, rect, x, y):
        rect.translate(x, y)
        self.gameRoot.scene.setSceneRect(rect)
        self.gameRoot.gameMenu.setDefaultPos()

    def translatScene(self, e):
        """Данный метод обеспечивает перемещение сцены внутри представления
         метод проверяет приблизился ли курсор к краю представления
        """
        rect = self.gameRoot.scene.sceneRect()
        if e.x() - 5.0 < 5.0:
            rect.translate(-10, 0)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

        if e.x() + 5.0 > self.view.viewport().width() - 5.0:
            rect.translate(10, 0)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

        if e.y() - 5.0 < 5.0:
            rect.translate(0, -10)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

        if e.y() + 5.0 > self.view.viewport().height() - 5.0:
            rect.translate(0, 10)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

    def itemSelect(self, newPos):
        x = int((newPos.x() / self.tr.m11()) / self.gameRoot.cfg.unit_size[0])
        if newPos.x() < 0:
            x -= 1

        y = int((newPos.y() / self.tr.m11()) / self.gameRoot.cfg.unit_size[1])
        if newPos.y() < 0:
             y -= 1

        world_x, world_y = self.gameRoot.cfg.world_size
        if 0 <= x < world_x and  0 <= y < world_y:
            self.last_point.x, self.last_point.y = x, y

        self.middleLayer.showToolTip(self.last_point, self.units.units_at)
        self.middleLayer.showSelectItem(x, y)