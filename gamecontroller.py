from PySide2 import QtCore, QtGui, QtWidgets
from menu import *
from gameutils import GameMath
from time import sleep

class GameController(object):
    """docstring for GameController."""
    def __init__(self, gameconfig):
        super(GameController, self).__init__()
        self.gameconfig = gameconfig
        self.view = None
        self.tr = QtGui.QTransform()

        self.cursor = QtWidgets.QGraphicsEllipseItem(-10, -10, 20, 20)

        # Выбираемая клетка, точка
        self.last_point = (0, 0)
        # Выбранная клетка, точка
        self.selected_point = None

    def setManager(self, manager):
        self.manager = manager
        for k, v in self.manager.getUnitFacings().items():
            self.setFacing(k, v)

    def setScreenMenu(self, menu):
        self.screenMenu = menu

    def setView(self, view):
        self.view = view

    def setUp(self, world, units, midleLayer):
        self.world = world
        self.units = units
        self.midleLayer = midleLayer

    def moveCursor(self, newPos):
        self.cursor.setX(newPos.x())
        self.cursor.setY(newPos.y())

    def mouseMoveEvent(self, e):
        """ Метод перехватывает событие движение мыши
        """
        newPos = self.view.mapToScene(e.x(), e.y())
        # self.itemSelect(newPos)
        self.moveCursor(newPos)
        self.translateScene(e)
        self.itemSelect(newPos)

    def mousePressEvent(self, e):
        self.manager.moveHero(self.last_point)
        self.updateWorld()
        self.selected_point = self.last_point
        self.midleLayer.showSelectedItem(self.selected_point)
        # print(self.last_point)

    def resizeEvent(self, e):
        self.screenMenu.resize(self.view)

    def keyPressEvent(self, e):
        self.attackUnit(e)
        self.setFacingHero(e)
        # self.moveUnit(e)
        self.tabUnit(e)

    def wheelEvent(self, e):
        """ Метод перехватывает собитие мышки скролл, скролл больше 0 зумм +,
        скролл меньше нуля зумм -
        """
        if e.delta() > 0.0:
            self.zoomIn()
        elif e.delta() < 0.0:
            self.zoomOut()

    def tabUnit(self, e):
        if e.key() == QtCore.Qt.Key_Tab:
            self.screenMenu.updateUnitStack()
            self.manager.nextStep()
            self.manager.setActiveUnit()
            self.units.setActiveUnit(self.manager.getActiveUnit())
            self.units.setUnitStack(self.manager.dun_game.turns_manager.managed)
            self.updateWorld()

    def updateWorld(self):
        cell = None
        for uid, unit in list(self.units.units_bf.items()):
            if not unit.alive:
                print('not live:', unit)
                self.units.removeUnit(uid)
                self.midleLayer.removeUnitLeyar(uid)
                self.screenMenu.updateUnitStack(uid)
            else:
                cell = self.manager.dun_game.battlefield.unit_locations.setdefault(unit, None)
                if not cell is None:
                    pos = (self.units.units_at[uid].worldPos.x(), self.units.units_at[uid].worldPos.y())
                    self.units.units_at[uid].setWorldPos(cell.x - 4, cell.y - 4)
                    self.units.updateLocations(self.units.units_at[uid], pos)
        self.midleLayer.updateSupport()
        for k, v in self.manager.getUnitFacings().items():
            self.setFacing(k, v)

    def attackUnit(self, e):
        if e.key() == QtCore.Qt.Key_E:
            if self.units.units_location.get(self.last_point):
                self.manager.attackHero(self.last_point)
                self.updateWorld()
            else:
                self.screenMenu.showNotify('Empty')

    def setFacingHero(self, e):
        """
        NORTH = (0 + 1j)
        SOUTH = (0 - 1j)
        WEST = (-1 + 0j)
        EAST = (1 + 0j)
        """
        if e.key() == QtCore.Qt.Key_W:
            self.manager.setFacingHero((0 - 1j))
            self.setFacing(self.manager.dun_game.the_hero, (0 - 1j))
            # print('up')
        if e.key() == QtCore.Qt.Key_S:
            self.manager.setFacingHero((0 + 1j))
            self.setFacing(self.manager.dun_game.the_hero, (0 + 1j))
            # print('down')
        if e.key() == QtCore.Qt.Key_D:
            self.manager.setFacingHero((1 + 0j))
            self.setFacing(self.manager.dun_game.the_hero, (1 + 0j))
            # print('left')
        if e.key() == QtCore.Qt.Key_A:
            self.manager.setFacingHero((-1 + 0j))
            self.setFacing(self.manager.dun_game.the_hero, (-1 + 0j))
            # print('right')
        # self.midleLayer.updateSupport()

    def moveUnit(self, e):
        """ Управление двжением героя
        """
        if e.key() == QtCore.Qt.Key_W:
            y = self.units.active_unit.worldPos.y() - 1
            if y >= - self.world.worldHalfSize[0]:
                self.units.collisionHeorOfUnits(y = y)
                self.units.active_unit.setDirection(0, -1)
            # print('up')
        if e.key() == QtCore.Qt.Key_S:
            y = self.units.active_unit.worldPos.y() + 1
            if y <  self.world.worldHalfSize[0]:
                self.units.collisionHeorOfUnits(y = y)
                self.units.active_unit.setDirection(0, 1)
            # print('down')
        if e.key() == QtCore.Qt.Key_A:
            x = self.units.active_unit.worldPos.x() - 1
            if x >=  -self.world.worldHalfSize[1]:
                self.units.collisionHeorOfUnits(x = x)
                self.units.active_unit.setDirection(-1, 0)
            # print('left')
        if e.key() == QtCore.Qt.Key_D:
            x = self.units.active_unit.worldPos.x() + 1
            if x < self.world.worldHalfSize[1]:
                self.units.collisionHeorOfUnits(x = x)
                self.units.active_unit.setDirection(1, 0)
            # print('right')
        self.midleLayer.updateSupport()

    def zoomIn(self):
        # self.view.scale(1.1, 1.1)
        # print(self.view.transform())
        self.tr.scale(1.1, 1.1)
        # print(self.tr)
        self.world.setTransform(self.tr)
        self.midleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def zoomOut(self):
        # self.view.scale(1/1.1, 1/1.1)
        # print(self.view.transform())
        self.tr.scale(1/1.1, 1/1.1)
        self.world.setTransform(self.tr)
        self.midleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def moveScene(self, rect, x, y):
        rect.translate(-10, 0)
        self.scene.setSceneRect(rect)
        self.screenMenu.setDefaultPos()

    def translateScene(self, e):
        """Данный метод обеспечивает перемещение сцены внутри представления
         метод проверяет приблизился ли курсор к краю представления
        """
        # if self.mymap.collidesWithItem(self.cursor):
        rect = self.scene.sceneRect()
        if e.x() - 5.0 < 5.0:
            rect.translate(-10, 0)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setX(self.screenMenu.x() - 10)
        if e.x() + 5.0 > self.view.viewport().width() - 5.0:
            rect.translate(10, 0)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setX(self.screenMenu.x() + 10)
        if e.y() - 5.0 < 5.0:
            rect.translate(0, -10)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setY(self.screenMenu.y() - 10)
        if e.y() + 5.0 > self.view.viewport().height() - 5.0:
            rect.translate(0, 10)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setY(self.screenMenu.y() + 10)

    def setFacing(self, unit, direction):
        """
        NORTH = (0 + 1j)
        WEST = (-1 + 0j)
        SOUTH = (0 - 1j)
        EAST = (1 + 0j)
        """
        if direction == (0 + 1j):
            self.units.units_at[unit.uid].setDirection(0, 1)
        elif direction == (0 - 1j):
            self.units.units_at[unit.uid].setDirection(0, -1)
        elif direction == (1 + 0j):
            self.units.units_at[unit.uid].setDirection(1, 0)
        elif direction == (-1 + 0j):
            self.units.units_at[unit.uid].setDirection(-1, 0)



    def itemSelect(self, newPos):
        # last_point = 0, 0
        if newPos.x() < 0:
            x = int((newPos.x() / self.tr.m11()) / self.gameconfig.unit_size[0]) - 1
        else:
            x = int((newPos.x() / self.tr.m11()) / self.gameconfig.unit_size[0])
        if newPos.y() < 0:
            y = int((newPos.y() / self.tr.m11()) / self.gameconfig.unit_size[1]) - 1
        else:
            y = int((newPos.y() / self.tr.m11()) / self.gameconfig.unit_size[1])
        if x < self.gameconfig.world_a_size[0] and x >= -self.gameconfig.world_a_size[0] and y < self.gameconfig.world_a_size[1] and y >= -self.gameconfig.world_a_size[1]:
            self.last_point = x, y
        # setUp
        self.midleLayer.showToolTip(newPos.x(), newPos.y(), self.last_point)
        self.midleLayer.showSelectItem(self.last_point)
        # x, y = GameMath.getTranslate(self.units.active_unit.worldPos.x(),
        #                             self.units.active_unit.worldPos.y(),
        #                             x, y)
        # dirPos = GameMath.get_direction(x, y)
        # if not dirPos is None:
        #     self.units.active_unit.setDirection(dirPos[0], dirPos[1])
        # self.item.setX(x * 32)
        # self.item.setY(y * 32)
