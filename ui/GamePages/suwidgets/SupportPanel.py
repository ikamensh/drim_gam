from PySide2 import QtWidgets
from ui.GamePages.suwidgets.GameButton import GameButton


class SupportPanel(QtWidgets.QWidget):
    def __init__(self, page, gameconfig, parent=None):
        super(SupportPanel, self).__init__(parent)
        self.page = page
        self.cfg = gameconfig
        self.w = 80
        self.h = self.w * 1
        self.setFixedSize(self.w, self.h)
        self.widget_x = self.cfg.dev_size[0] - self.w
        self.widget_y = 0
        self.move(self.widget_x, self.widget_y)
        self.setUpStyles()

    def setUpStyles(self):
        pic_path = self.cfg.pic_file_paths.get('scroll_background.png')
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        # if pic_path:
        #     self.setStyleSheet("background-image: url('" + pic_path + "');")

        self.up_chest = None
        self.down_chest = None
        pic_path = self.cfg.pic_file_paths.get('chest_0.png')
        if pic_path:
            self.down_chest = "background-image: url('" + pic_path + "');"
        pic_path = self.cfg.pic_file_paths.get('chest_1.png')
        if pic_path:
            self.up_chest = "background-image: url('" + pic_path + "');"

    def setUpWidgets(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setMargin(8)
        button = GameButton(self)
        button.hovered.connect(self.up_chest_btn)
        button.hover_out.connect(self.down_chest_btn)
        button.clicked.connect(self.open_inventary)
        if self.down_chest:
            button.setStyleSheet(self.down_chest)
        button.setFixedSize(64, 64)
        layout.addWidget(button)
        self.setLayout(layout)

    def up_chest_btn(self, btn):
        if self.up_chest:
            btn.setStyleSheet(self.up_chest)

    def down_chest_btn(self, btn):
        if self.down_chest:
            btn.setStyleSheet(self.down_chest)

    def open_inventary(self):
        pass