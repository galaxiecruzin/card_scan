import sys
# from PySide import QtCore
from PySide import QtCore, QtGui
from mainwindow import Ui_MainWindow


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set Image
        myPixmap = QtGui.QPixmap('./phototest/ancient-stirrings.jpg')
        myScaledPixmap = myPixmap.scaled(self.ui.preview.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.preview.setPixmap(myScaledPixmap)

        # Set Status
        self.ui.status.setText("Identified")

        # Set Card Name
        self.ui.card_name.setText("Ancient Stirrings")

        # Load combo options for expansion
        # self.ui.expansion

        # Load combo options for conditions
        # self.ui.condition


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
