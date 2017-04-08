from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .compiler_wrapper import compile_code


# Create your views here.
def index(request):
	return render(request, "index.html", context={})


def assembly(request):
	if not request.is_ajax():
		return HttpResponseForbidden('<h1>No Page Here</h1>')
	source = request.GET["code"]
	optimization_level = request.GET["optimization_level"]
	compiled = compile_code(source, optimization_level)
	return HttpResponse(compiled)
