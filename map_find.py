import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog, QLineEdit

SCREEN_SIZE = [600, 500]
# 37.530887 55.703118


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinate = self.get_coord()
        self.REQUEST = f"http://static-maps.yandex.ru/1.x/?ll={self.coordinate[0]},{self.coordinate[1]}&spn=0.002,0.002&l=map"
        self.getImage(self.REQUEST)
        self.initUI()

    def get_coord(self):
        coor, okBtnPressed = QInputDialog.getText(self, "Координаты",
                                               "Введите координаты через пробел")
        if okBtnPressed:
            if __name__ == '__main__':
                coor = coor.split()
                return coor

    def getImage(self, req):
        map_request = req
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.name_label = QLabel(self)
        self.name_label.setText("Поиск: ")
        self.name_label.move(260, 470)

        self.name_input = QLineEdit(self)
        self.name_input.move(300, 470)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
