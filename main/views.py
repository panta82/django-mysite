from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def homepage(request: HttpRequest):
	return HttpResponse("Test")
