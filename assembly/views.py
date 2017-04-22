# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .compiler_wrapper import compile_code
import logging

logger = logging.getLogger("views")


# Create your views here.
# def index(request):
# 	return render(request, "index.html", context={})


def assembly(request):
	if not request.is_ajax():
		logger.critical("Not an ajax request")
		return HttpResponseForbidden('<h1>No Page Here</h1>')
	logger.info("Starting serving the request")
	source = request.GET["code"]
	compiler_name = request.GET["compiler"]
	optimization_level = request.GET["optimization_level"]
	compiled = compile_code(source, optimization_level, compiler_name)
	return HttpResponse(compiled)
