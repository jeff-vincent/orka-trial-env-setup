class SetEnv:

	def __init__(self):
		self.env_data = {}

	def parse_env_data(self):
		# TODO: parse the IP Plan etc.
		self.env_data = {
			'ORKA_USER': 'email@email.com',
			'ORKA_PASS': 'password'
		}

	def write_profile(self):
		top_lines = []
		bottom_lines = []
		with open('profile.template', 'r') as template:
			with open('/etc/profile', 'w') as profile:
				for line in template:
					if 'export' in line:
						top_lines.append(line)
					else:
						bottom_lines.append(line)
				for line in top_lines:
					profile.write(line)
				for key, value in self.env_data.items():
					profile.write(f"export {key}={value}\n")
				for line in botom_lines:
					profile.write(line)


def main(set_env):
	set_env.parse_env_data()
	set_env.write_profile()


if __name__ == '__main__':
	set_env = SetEnv()
	main(set_env)

