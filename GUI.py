import sys
import time

from PyQt6 import QtCore
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import final_project


# This is the pop up window at the end of the simulation
class Pop(QWidget):

    def __init__(self, k):
        # QWidget is its super
        QWidget.__init__(self)
        self.setWindowTitle('Finished!')
        self.setWindowIcon(QIcon('internet_icon.png'))
        self.setGeometry(500, 500, 280, 200)
        self.prompt = QLabel(self)
        self.prompt.setGeometry(40, 10, 300, 60)
        self.prompt.setFont(QFont("Roman times", 14))
        # k is bool type
        if k:
            self.prompt.setText('Simulation ended,\n country A wins!')
            self.prompt.show()
        else:
            self.prompt.setText('Simulation ended,\n country B wins!')
            self.prompt.show()
        # button here to close pop-up window
        self.ok_btn = QPushButton('OK', self)
        self.ok_btn.clicked.connect(self.button_clicked)
        self.ok_btn.setGeometry(105, 150, 60, 40)
        self.ok_btn.show()

    # Destroys the whole window once button is clicked
    def button_clicked(self):
        self.destroy()


class Main(QMainWindow):

    def __init__(self):
        # QMainWindow inits here
        super().__init__()
        # this call init of the 'actual self'
        self.init_ui()

    def init_ui(self):

        # all these alerts are showing that self attributes are not defined in init,
        # if you have them just ignore
        self.q_btn = QPushButton('Start', self)
        self.q_btn.clicked.connect(self.button_clicked)
        self.q_btn.setGeometry(25, 330, 100, 50)
        self.q_btn.show()
        # From here to the next comment is the module I use for a progress bar with its descriptions
        self.p_bar_a_lable = QLabel(self)
        self.p_bar_a_lable.setText('Total Infection rate')
        self.p_bar_a_lable.setGeometry(30, 20, 200, 20)
        self.p_bar_a_lable.show()

        self.p_bar_a = QProgressBar(self)
        self.p_bar_a.setGeometry(30, 40, 500, 20)
        self.p_bar_a.show()
        # Here is the end of one module
        self.p_bar_b_lable = QLabel(self)
        self.p_bar_b_lable.setText('Town01 Infection rate')
        self.p_bar_b_lable.setGeometry(30, 70, 200, 20)
        self.p_bar_b_lable.show()

        self.p_bar_b = QProgressBar(self)
        self.p_bar_b.setGeometry(30, 90, 250, 20)
        self.p_bar_b.show()

        self.p_bar_c_lable = QLabel(self)
        self.p_bar_c_lable.setText('Town02 Infection rate')
        self.p_bar_c_lable.setGeometry(30, 120, 200, 20)
        self.p_bar_c_lable.show()

        self.p_bar_c = QProgressBar(self)
        self.p_bar_c.setGeometry(30, 140, 250, 20)
        self.p_bar_c.show()

        self.p_bar_d_lable = QLabel(self)
        self.p_bar_d_lable.setText('Town03 Infection rate')
        self.p_bar_d_lable.setGeometry(30, 170, 200, 20)
        self.p_bar_d_lable.show()

        self.p_bar_d = QProgressBar(self)
        self.p_bar_d.setGeometry(30, 190, 250, 20)
        self.p_bar_d.show()

        self.p_bar_e_lable = QLabel(self)
        self.p_bar_e_lable.setText('Town04 Infection rate')
        self.p_bar_e_lable.setGeometry(30, 220, 200, 20)
        self.p_bar_e_lable.show()

        self.p_bar_e = QProgressBar(self)
        self.p_bar_e.setGeometry(30, 240, 250, 20)
        self.p_bar_e.show()

        self.p_bar_f_lable = QLabel(self)
        self.p_bar_f_lable.setText('Town05 Infection rate')
        self.p_bar_f_lable.setGeometry(30, 270, 200, 20)
        self.p_bar_f_lable.show()

        self.p_bar_f = QProgressBar(self)
        self.p_bar_f.setGeometry(30, 290, 250, 20)
        self.p_bar_f.show()

        self.p_bar_g_lable = QLabel(self)
        self.p_bar_g_lable.setText('V rate*')
        self.p_bar_g_lable.setGeometry(340, 70, 200, 20)
        self.p_bar_g_lable.show()

        self.p_bar_g = QProgressBar(self)
        self.p_bar_g.setGeometry(340, 100, 30, 210)
        self.p_bar_g.setOrientation(QtCore.Qt.Vertical)
        self.p_bar_g.show()

        self.p_bar_h_lable = QLabel(self)
        self.p_bar_h_lable.setText('Day')
        self.p_bar_h_lable.setGeometry(420, 70, 200, 20)
        self.p_bar_h_lable.show()

        self.p_bar_h = QProgressBar(self)
        self.p_bar_h.setGeometry(420, 100, 30, 210)
        self.p_bar_h.setOrientation(QtCore.Qt.Vertical)
        self.p_bar_h.show()

        self.p_v_lable = QLabel(self)
        self.p_v_lable.setText('*V: Vaccination')
        self.p_v_lable.setGeometry(300, 340, 200, 20)
        self.p_v_lable.show()
        # All the same until here
        # Setting attributes of the window, not too big considering low-resolution machines
        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle('Proj')
        self.setWindowIcon(QIcon('internet_icon.png'))
        self.center()

        self.statusBar()
        # this is actually the pop_up window
        self.pop_1 = None
        # shows everything by here
        self.show()

    # centers function
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # same name but in different classes,
    # so different functions
    def button_clicked(self):
        # makes btn disappear
        self.q_btn.clicked.disconnect()
        self.load()

    # this part started out as a simple i+=1 for loop,
    # and was configured to this in 30 minutes (shows advantage of modularization)
    def load(self):
        # add main calculation here!
        i = 0
        winning = None
        while True:
            if i <= 100:
                data = final_project.main(i)
                # main returns a list 'data', that was added by me
                if data[0] <= 0.9:
                    self.p_bar_a.setValue(100 * data[0])
                else:
                    self.p_bar_a.setValue(90)
                    # make sure it doesn't go over
                    winning = True
                    self.pop_1 = Pop(winning)  # False B wins, True A wins
                    self.pop_1.show()
                    break
                if data[1][0] <= 0.8:
                    self.p_bar_b.setValue(100 * data[1][0])
                else:
                    self.p_bar_b.setValue(80)
                    self.p_bar_b_lable.setText('Town Quarantined')
                if data[1][1] <= 0.8:
                    self.p_bar_c.setValue(100 * data[1][1])
                else:
                    self.p_bar_c.setValue(80)
                    self.p_bar_c_lable.setText('Town Quarantined')
                if data[1][2] <= 0.8:
                    self.p_bar_d.setValue(100 * data[1][2])
                else:
                    self.p_bar_d.setValue(80)
                    self.p_bar_d_lable.setText('Town Quarantined')
                if data[1][3] <= 0.8:
                    self.p_bar_e.setValue(100 * data[1][3])
                else:
                    self.p_bar_e.setValue(80)
                    self.p_bar_e_lable.setText('Town Quarantined')
                if data[1][4] <= 0.8:
                    self.p_bar_f.setValue(100 * data[1][4])
                else:
                    self.p_bar_f.setValue(80)
                    self.p_bar_f_lable.setText('Town Quarantined')
                self.p_bar_g.setValue(100 * data[2])
                self.p_bar_h.setValue(i)
                i += 1
                time.sleep(0.05)
            else:
                self.pop_1 = Pop(winning)  # False B wins, True A wins
                self.pop_1.show()
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_w = Main()
    sys.exit(app.exec_())
