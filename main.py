import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd

class Square(QMainWindow):
    def __init__(self):
        super(Square, self).__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Square")
        self.image = QPixmap()
        self.resize(800, 500)
        self.center()
        self.show()

        self.createActions()
        self.createMenuBar()
        self.connectActions()

        self.begin = QPoint()
        self.end = QPoint()
        self.centers = []

    #Функция центровки окна

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #Открытие файла
    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self,"Open File",None,"Image (*.jpg)")[0]
        self.image = QPixmap(file_name)
        self.resize(self.image.width(), self.image.height())
        self.center()
        self.update()

    #Сохранение картинки
    def saveFile(self):

        # with open('coord3.txt', 'w') as f:
        #     for element in self.centers:
        #         f.writelines(element + '\n')

        if self.image is None:
            return
        fileName = QFileDialog.getSaveFileName(self, "Сохранить", filter="Image Files (*.png *.jpg *.bmp)")[0]
        if fileName is None or len(fileName) == 0:
            return
        self.image.save(fileName)

        df = pd.DataFrame(self.centers)
        df.to_csv('res.csv', header=False, index=False)
        # textfile = open("coord.txt", mode='w')
        # print(self.centers)
        # for element in self.centers:

        # for element in self.centers:
        #     print(element)

    #Меню окна
    def connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)

    def createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save...", self)
        self.exitAction = QAction("&Exit", self)

    def createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

    #Рисование фигур

    def paintEvent(self, event):
        qp = QPainter(self)
        br = QBrush(QColor(0, 255, 0, 50))
        qp.setBrush(br)
        qp.setPen(QPen(Qt.darkCyan, 3, Qt.SolidLine))
        qp.drawPixmap(QPoint(), self.image)
        if not self.begin.isNull() and not self.end.isNull():
            qp.drawRect(QRect(self.begin, self.end).normalized())
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.end = event.pos()
            self.update()


    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            rect = QRect(self.begin, self.end)
            self.begin = event.pos()
            self.end = event.pos()
            qp = QPainter(self.image)
            br = QBrush(QColor(0, 0, 255, 30))
            qp.setBrush(br)
            qp.setPen(QPen(Qt.green, 3, Qt.SolidLine))
            self.centers.append((rect.center().x(), rect.center().y()))
            qp.drawRect(rect.normalized())
            self.begin, self.end = QPoint(), QPoint()
            self.update()



def window():
    app = QApplication(sys.argv)
    win = Square()
    win.show()
    sys.exit(app.exec_())


window()