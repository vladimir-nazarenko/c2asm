import random
import re
from subprocess import check_output, STDOUT, CalledProcessError
from os import remove
from os.path import isfile


def validate_optimization_level(optimization_level):
	return re.match("-O[0123]", optimization_level)


def validate_code(code):
	return len(code) < 10000


def compile_code(code, optimization_level):
	# validate
	if not validate_optimization_level(optimization_level) or not validate_code(code):
		return "Invalid input"

	# compile
	file_id = str(random.randint(0, 1e9))
	input_file_name = file_id + ".cpp"
	with open(input_file_name, "w") as out:
		out.write(code)
	try:
		output = check_output(" ".join(["g++", "-S", optimization_level, input_file_name, "-o", file_id]),
							  stderr=STDOUT,
							  shell=True)
	except CalledProcessError as e:
		output = "Compilation failed with following output:\n" + e.output

	if isfile(file_id):
		with open(file_id) as assembly_file:
			content = assembly_file.read()
		remove(file_id)
	else:
		content = output

	# clean up
	remove(input_file_name)

	return content
