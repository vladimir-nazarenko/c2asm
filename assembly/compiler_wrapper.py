import enum
import random
import re
import logging
from subprocess import check_output, STDOUT, CalledProcessError
from os import remove, makedirs, removedirs
from os.path import isfile

logger = logging.getLogger("compiler_wrapper")
logger.setLevel(logging.DEBUG)


class Compiler(enum.Enum):
	GCC49 = 1
	GCC54 = 2
	GCC63 = 3
	CLANG = 4

	def compiler_command(self):
		if self.name.startswith("GCC"):
			return "g++ -fdiagnostics-color=never"
		elif self == Compiler.CLANG:
			return "clang"
		else:
			raise RuntimeError("Invalid compiler")

	def docker_image(self):
		if self.name.startswith("GCC"):
			return "gcc" + ":" + self.name[3] + "." + self.name[4]
		elif self == Compiler.CLANG:
			return "rsmmr/clang"
		else:
			raise RuntimeError("Invalid compiler")


def validate_optimization_level(optimization_level):
	return re.match("-O[0123]", optimization_level)


def validate_code(code):
	return len(code) < 10000


def validate_compiler(compiler):
	return True

string_to_compiler = {"GCC 5.4": Compiler.GCC54, "GCC 4.9": Compiler.GCC49,
					  "GCC 6.3": Compiler.GCC63, "CLANG": Compiler.CLANG}


def get_compiler_for_string(compiler_name):
	return string_to_compiler[compiler_name]


def get_bash_command_for_compiler_execution(compiler, optimization_level, filename, output_dir):
	return " ".join([
		"docker run",
		"-v `pwd`/{0}:/{0}".format(filename),
		"-v `pwd`/{0}:/out".format(output_dir),
		"--rm -it",
		compiler.docker_image(),
		"{0} /{1} -S -O{2} -o /out/{1}.s".format(compiler.compiler_command(), filename, optimization_level[-1])])


def compile_code(code, optimization_level, compiler_name):
	# validate
	if not validate_optimization_level(optimization_level) or not validate_code(code) or not validate_compiler(
			compiler_name):
		logger.critical("Couldn't validate the input")
		return "Invalid input"

	compiler = get_compiler_for_string(compiler_name)

	logger.debug("Started compilation procedures")

	# compile
	file_id = str(random.randint(0, 1e9))
	input_file_name = file_id + ".cpp"

	logger.info("Writing the input into " + input_file_name)

	with open(input_file_name, "w") as out:
		out.write(code)
	makedirs(file_id)

	output_file_name = file_id + "/" + input_file_name + ".s"

	try:
		output = check_output(
			get_bash_command_for_compiler_execution(compiler, optimization_level, input_file_name, file_id),
							  stderr=STDOUT,
							  shell=True)
	except CalledProcessError as e:
		output = "Compilation failed with following output:\n" + str(e.output.decode("ascii", "ignore"))
	finally:
		remove(input_file_name)

	if isfile(output_file_name):
		with open(output_file_name) as assembly_file:
			content = assembly_file.read()
		remove(output_file_name)
	elif output == "":
		content = "Command was successful with no output"
		logger.critical("Logical error in the compiler wrapper")
	else:
		content = output

	removedirs(file_id)

	return content
