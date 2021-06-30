import sys

from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory
from PyQt5.QtWidgets import QGroupBox, QPushButton, QAbstractButton, QGridLayout, QComboBox, QLineEdit, QTableWidgetItem, QLabel
from PyQt5.QtGui import QPalette, QColor

from utils.DAQEventHandler import *
from utils.DraggableTable import *

class DebugUI(QWidget):
	def __init__(self):
		super(DebugUI, self).__init__()

		self.daq = DAQEventHandler()

		self.mainLayout = QGridLayout()
		self.setLayout(self.mainLayout)

		self.daq_configured = False

		self.initUI()
		self.createMainWindow()
		self.show()

	def initUI(self):
		self.setGeometry(400, 300, 800, 600)
		self.setWindowTitle('Ph2_ACF Debug Tool')

		if sys.platform.startswith("darwin"):
			QApplication.setStyle(QStyleFactory.create('macintosh'))
			QApplication.setPalette(QApplication.style().standardPalette())
		elif sys.platform.startswith("linux") or sys.platform.startswith("win") or sys.platform.startswith("darwin"):
			darkPalette = QPalette()
			darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
			darkPalette.setColor(QPalette.WindowText, Qt.white)
			darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
			darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
			darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
			darkPalette.setColor(QPalette.ToolTipText, Qt.white)
			darkPalette.setColor(QPalette.Text, Qt.white)
			darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
			darkPalette.setColor(QPalette.ButtonText, Qt.white)
			darkPalette.setColor(QPalette.BrightText, Qt.red)
			darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
			darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
			darkPalette.setColor(QPalette.HighlightedText, Qt.black)

			QApplication.setStyle(QStyleFactory.create('Fusion'))
			QApplication.setPalette(darkPalette)
		else:
			print('This GUI supports Win/Linux/MacOS only')

	def configureDAQ(self):
		self.daq_configured = True
		self.configure_button.setDisabled(True)
		self.destroy_button.setDisabled(False)
		self.daq.configureDAQ()

	def destroyDAQ(self):
		self.daq_configured = False
		self.destroy_button.setDisabled(True)
		self.configure_button.setDisabled(False)
		self.daq.destroyDAQ()

	def addCommand(self, cmd_name):
		cmd_address, cmd_value = available_commands[cmd_name]

		item_name = QTableWidgetItem(cmd_name)

		item_address = QTableWidgetItem()
		if cmd_address is None:
			item_address.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			item_address.setBackground(QColor(211, 211, 211))
		else:
			item_address.setText('0x' + str(cmd_address))

		item_value = QTableWidgetItem()
		if cmd_value is None:
			item_value.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			item_value.setBackground(QColor(211, 211, 211))
		else:
			item_value.setText(str(cmd_value))

		self.test_table.insertRow(self.test_table.rowCount())
		self.test_table.setItem(self.test_table.rowCount() - 1, 0, item_name)
		self.test_table.setItem(self.test_table.rowCount() - 1, 1, item_address)
		self.test_table.setItem(self.test_table.rowCount() - 1, 2, item_value)

	def run(self):
		self.daq.commands = [tuple([self.test_table.item(i, j).text() for j in range(3)]) for i in range(self.test_table.rowCount())]
		self.daq.runTest()
		print('Done')

	def createMainWindow(self):
		self.configure_button = QPushButton('Configure DAQ')
		self.configure_button.clicked.connect(self.configureDAQ)

		self.destroy_button = QPushButton('Destroy DAQ')
		self.destroy_button.clicked.connect(self.destroyDAQ)
		self.destroy_button.setDisabled(True)

		self.command_buttons = []
		self.command_buttons.append(QPushButton('Reset FIFO'))
		self.command_buttons[-1].clicked.connect(lambda : self.addCommand('Reset FIFO'))
		self.command_buttons.append(QPushButton('Flush FIFO'))
		self.command_buttons[-1].clicked.connect(lambda : self.addCommand('Flush FIFO'))
		self.command_buttons.append(QPushButton('Read Register'))
		self.command_buttons[-1].clicked.connect(lambda : self.addCommand('Read Register'))
		self.command_buttons.append(QPushButton('Write Register'))
		self.command_buttons[-1].clicked.connect(lambda : self.addCommand('Write Register'))
		self.command_buttons.append(QPushButton('Sleep (us)'))
		self.command_buttons[-1].clicked.connect(lambda : self.addCommand('Sleep (us)'))

		self.test_table = DraggableTable()
		self.test_table.setColumnCount(3)
		self.test_table.setHorizontalHeaderLabels(['Command', 'Address', 'Value'])

		self.exit_button = QPushButton('Exit')
		self.exit_button.clicked.connect(self.close)

		self.run_button = QPushButton('Run')
		self.run_button.clicked.connect(self.run)

		layout = QGridLayout()
		layout.setSpacing(20)
		# row, col, row_span, col_span
		for i, b in enumerate(self.command_buttons):
			layout.addWidget(b, 2, i+1, 1, 1)
		layout.addWidget(self.test_table, 3, 1, 4, 3)
		layout.addWidget(self.configure_button, 7, 1, 1, 1)
		layout.addWidget(self.destroy_button, 7, 2, 1, 1)
		layout.addWidget(self.run_button, 8, 1, 1, 1)
		layout.addWidget(self.exit_button, 8, 5, 1, 1)


		self.GroupBox = QGroupBox('')
		self.GroupBox.setLayout(layout)
		self.mainLayout.addWidget(self.GroupBox, 0, 0)

