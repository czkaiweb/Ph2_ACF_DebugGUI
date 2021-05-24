import sys

from PyQt5.QtWidgets import QApplication

from utils.DebugUI import *

def main():
	app = QApplication(sys.argv)
	ui = DebugUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
