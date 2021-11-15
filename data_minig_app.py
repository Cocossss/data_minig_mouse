from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pynput.mouse as mouse
import sys
import os
import csv
import pyautogui

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.listener = mouse.Listener(on_click=self.on_click)
        self.picture_id = 0 # to track screenshot's id
        self.coordinates = []
        self.isScreened = False # to track if first screen was created
        self.setWindowTitle('Data minig mouse')
        self.setGeometry(50, 50, 600, 600)

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText('Программа Data minig mouse позволяет отслеживать действия мыши\nПКМ - сделать скриншот экрана')
        self.main_text.move(10, 10)
        self.main_text.setFixedWidth(590)

        self.start_text = QtWidgets.QLabel(self)
        self.start_text.setText('ЛКМ - сохранить координаты курсора мыши в файл')
        self.start_text.move(10, 40)
        self.start_text.setFixedWidth(590)

        self.start_text = QtWidgets.QLabel(self)
        self.start_text.setText('Начать мониторинг:')
        self.start_text.move(10, 80)
        self.start_text.setFixedWidth(200)

        # start button - starts listening the mouse
        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.move(250, 80)
        self.btn_start.setText('start')
        self.btn_start.setFixedWidth(200)
        self.btn_start.clicked.connect(self.start)

        self.stop_text = QtWidgets.QLabel(self)
        self.stop_text.setText('Остановить мониторинг:')
        self.stop_text.move(10, 150)
        self.stop_text.setFixedWidth(200)

        # stop button - stops listening the mouse
        self.btn_stop = QtWidgets.QPushButton(self)
        self.btn_stop.move(250, 150)
        self.btn_stop.setText('stop')
        self.btn_stop.setFixedWidth(200)
        self.btn_stop.clicked.connect(self.stop)

    # called from another thread on each mouse click
    def on_click(self, x, y, button, pressed):
        # if stop button is on click (is disabled) then return false from callback (this is stopping the thread)
        if not self.btn_stop.isEnabled():
            return False

        if button == mouse.Button.left and pressed == True and self.isScreened == True:
            self.coordinates.append(['screen_' + str(self.picture_id-1), x, y])

        elif button == mouse.Button.right and pressed == True:
            self.isScreened = True
            screen_dir = os.path.join(root_dir, 'screenshots')

            if not os.path.join(root_dir, 'screenshots'):
                os.mkdir(screen_dir)

            screenshot = pyautogui.screenshot()
            screenshot.save(os.path.join(screen_dir, 'screen_' + str(self.picture_id) + '.png'))
            self.picture_id += 1

    # works when start button is pushed
    def start(self):
        if not self.listener.is_alive():
            self.listener = mouse.Listener(on_click=self.on_click, daemon=None)
            self.listener.start()
            self.btn_stop.setEnabled(True)

    # works when stop button is pushed
    def stop(self):
        if self.listener.is_alive():
            self.btn_stop.setEnabled(False)

    def closeEvent(self, event):
        # if stop button isn't called then program close the thread automatically
        self.stop()

        # all coordinates are saving in file when program is quiting
        root_dir = os.getcwd()
        filename = os.path.join(root_dir, 'mpc_centers.csv')
        with open(filename, 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.coordinates[:len(self.coordinates)-1])

        reply = QMessageBox.question(self, 'Message', "Вы уверены, что хотите закрыть окно?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def app():
    app = QApplication(sys.argv)

    window = Window()

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    root_dir = os.getcwd()
    filename = os.path.join(root_dir, 'mpc_centers.csv')

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['screen_id','mpc_center_x',' mpc_center_y'])

    app()
