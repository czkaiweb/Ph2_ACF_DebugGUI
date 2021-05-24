available_commands = {
	# command name : (default address, default value)
	'Reset FIFO' : (None, None),
	'Flush FIFO' : (None, None),
	'Read Register' : (0x0, None),
	'Write Register' : (0x0, 0),
	'Sleep (us)' : (None, 50)
}

class Message:
	def __init__(self, op_code, data):
		self.op_code = op_code
		self.data = data

class DAQEventHandler:
	def __init__(self):
		self.isConfigured = False
		self.commands = []

	def configureDAQ(self):
		self.isConfigured = True
		print('configureDAQ() ...')

	def destroyDAQ(self):
		self.isConfigured = False
		print('destroyDAQ() ...')

	def runTest(self):
		if not self.isConfigured:
			print('DAQEventHander: not configured!')
			return
		for cmd_name, cmd_address, cmd_value in self.commands:
			if cmd_name == 'Reset FIFO':
				print('Reset FIFO!')
			elif cmd_name == 'Flush FIFO':
				print('Flush FIFO!')
			elif cmd_name == 'Read Register':
				print('Read register', cmd_address)
			elif cmd_name == 'Write Register':
				print('Write value', cmd_value, 'to register', cmd_address)
			elif cmd_name == 'Sleep (us)':
				print('Sleeping', cmd_value, 'us...')
			else:
				print('Unknown command...')
