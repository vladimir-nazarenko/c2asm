from django.shortcuts import render
from django.http import HttpResponse, request
from subprocess import call

# Create your views here.
def index(request):
	sources_path = "/home/developer/cpp_snippets/"
	output_path = "/home/developer/generated_assembly/"
	if "code" in request.GET:
		file_name = "user_file.cpp"
		with open(sources_path + file_name, "w") as out:
			out.write(request.GET["code"])
	else:
		file_name = "main.cpp"
	call(["g++", "-S", sources_path + file_name, "-o", output_path + file_name])
	with open(output_path + file_name) as assembly:
		content = assembly.read()
	return HttpResponse(content)
