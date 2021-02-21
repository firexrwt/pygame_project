import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from PyQt5 import uic
import json
import pygame

with open('Data/Misc/CustomSprites.json', 'r') as cs:
    csdir = json.load(cs)

Threat_Sprite = pygame.sprite.Group()
Ground_Sprites = pygame.sprite.Group()
Decor_Sprites = pygame.sprite.Group()


class CClass(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Data/Misc/CustomClass.ui', self)
        self.comboBox.addItem('Ground')
        self.comboBox.addItem('Threat')
        self.comboBox.addItem('Decor')
        self.cbgroup = 'Decor'
        self.symbol.maxLength()
        self.otstup = False
        self.ui()

    def ui(self):
        self.add.clicked.connect(self.addSpr)
        self.delete_2.clicked.connect(self.delete)
        self.save.clicked.connect(self.savespr)
        self.buffer.stateChanged.connect(self.changeBState)

    def addSpr(self):
        self.im = QFileDialog().getOpenFileName()

    def changeBState(self):
        self.otstup = not self.otstup

    def delete(self):

        symb = QInputDialog.getText(self, 'Удаление', 'Введите Символ для удаления')
        try:
            del csdir[symb[0]]
            with open('Data/Misc/CustomSprites.json', 'w') as csfile:
                json.dump(csdir, csfile)
        except Exception:
            print('Такого класса нет')


    def savespr(self):
        self.cbgroup = str(self.comboBox.currentText())
        symb = self.symbol.text()
        sprn = self.sprName.text()
        gr = self.cbgroup
        try:
            vel = int(self.Velocity.text())
        except Exception:
            vel = 0
        self.im = '/'.join(self.im[0].split('/')[-3:])
        csdir[symb] = [gr, self.im, vel, sprn, self.otstup]
        print(symb, csdir[symb])
        with open('Data/Misc/CustomSprites.json', 'w') as csfile:
            json.dump(csdir, csfile)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cc = CClass()
    cc.show()
    sys.exit(app.exec())
