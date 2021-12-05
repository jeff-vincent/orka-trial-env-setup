top_lines = []
botom_lines = []

data = {
	'ORKA_USER': 'email@email.com',
	'ORKA_PASS': 'password'
}



with open('profile.template', 'r') as template:
	with open('profile', 'w') as profile:
		for line in template:
			if 'export' in line:
				top_lines.append(line)
			else:
				botom_lines.append(line)
		for line in top_lines:
			profile.write(line)
		for key, value in data.items():
			profile.write(f"export {key}={value}\n")
		for line in botom_lines:
			profile.write(line)
