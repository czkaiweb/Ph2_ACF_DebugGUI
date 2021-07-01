from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import (QPixmap, QTextCursor, QColor)
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
		QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPlainTextEdit,
		QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
		QSlider, QSpinBox, QStyleFactory, QTableView, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit, QTreeWidget, QHBoxLayout,
		QVBoxLayout, QWidget, QMainWindow, QMessageBox, QSplitter)

import os

available_commands = {
	# command name : (default address, default value)
	'Reset FIFO' : (None, None),
	'Flush FIFO' : (None, None),
	'Read Register' : ("", None),
	'Write Register' : ("", ""),
	'Sleep (us)' : (None, 50)
}

class Message:
	def __init__(self, op_code, data):
		self.op_code = op_code
		self.data = data

class DAQEventHandler(QWidget):
	def __init__(self):
		super(DAQEventHandler,self).__init__()
		self.isConfigured = False
		self.commands = []

		self.run_process = QProcess(self)
		self.run_process.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)
		#self.run_process.finished.connect(self.on_finish)

	def runDAQ(self):
		self.run_process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
		self.run_process.setWorkingDirectory(os.environ.get("Ph2_ACF_AREA")+"/test/")
		self.run_process.start("CMSITminiDAQ", ["-f","CMSIT.xml", "-c", "interDebug"])

	def configureDAQ(self):
		self.runDAQ()
		#self.isConfigured = True
		print('configureDAQ() ...')

	def destroyDAQ(self):
		self.isConfigured = False
		print('destroyDAQ() ...')

	def quitTest(self):
		self.run_process.write(bytes("QUIT\n",encoding='utf8'))
		return

	def runTest(self):
		if not self.isConfigured:
			print('DAQEventHander: not configured!')
			self.configureDAQ()
			return

		#for cmd_name, cmd_address, cmd_value in self.commands:
		#	if cmd_name == 'Reset FIFO':
		#		print('Reset FIFO!')
		#	elif cmd_name == 'Flush FIFO':
		#		print('Flush FIFO!')
		#	elif cmd_name == 'Read Register':
		#		print('Read register', cmd_address)
		#	elif cmd_name == 'Write Register':
		#		print('Write value', cmd_value, 'to register', cmd_address)
		#	elif cmd_name == 'Sleep (us)':
		#		print('Sleeping', cmd_value, 'us...')
		#	else:
		#		print('Unknown command...')
		
		if len(self.commands) == 0:
			#self.run_process.write(bytes("QUIT\n",encoding='utf8'))
			#self.run_process.waitForBytesWritten()
			return
			#self.run_process.closeWriteChannel()

		cmd_name, reg_name, reg_value = self.commands.pop(0)
		if cmd_name == 'Reset FIFO':
			print("Reset FIFO...\n")
			self.run_process.write(bytes("RESET;;;\n",encoding='utf8'))
			self.run_process.waitForBytesWritten()
			#self.run_process.closeWriteChannel()
		elif cmd_name == 'Flush FIFO':
			print('Flush FIFO...')
			self.run_process.write(bytes("FLUSH;;;\n",encoding='utf8'))
			self.run_process.waitForBytesWritten()
			#self.run_process.closeWriteChannel()
		elif cmd_name == 'Read Register':
			if reg_name == None:
				print("No register given, continue...")
			else:
				print('Read register:', reg_name)
				self.run_process.write(bytes("READ;{};;\n".format(reg_name),encoding='utf8'))
				self.run_process.waitForBytesWritten()
				#self.run_process.closeWriteChannel()
		elif cmd_name == 'Write Register':
			if reg_name == None or reg_value == None:
				print("No register name or value given, continue...")
			else:
				print('Write value', reg_value, 'to register', reg_name)
				self.run_process.write(bytes("WRITE;{};{};\n".format(reg_name, reg_value),encoding='utf8'))
				self.run_process.waitForBytesWritten()
				#self.run_process.closeWriteChannel()
		elif cmd_name == 'Sleep (us)':
			if reg_value == None:
				print("No sleep time given, continue...")
			else:
				print('Sleeping', reg_value, 'us...')
				self.run_process.write(bytes("SLEEP;;{};\n".format(reg_value),encoding='utf8'))
				self.run_process.waitForBytesWritten()
				#self.run_process.closeWriteChannel()
		else:
			print('Unknown command...')

	@QtCore.pyqtSlot()
	def on_readyReadStandardOutput(self):		
		alltext = self.run_process.readAllStandardOutput().data().decode()
		textline = alltext.split('\n')
		for item in textline:
			print(item)
		for textStr in textline:
			if "Ready to accept debug command" in textStr:
				self.isConfigured = True
				#self.run_process.closeReadChannel()
				self.runTest()

			# Get the output and parse the result
