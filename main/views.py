from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from main.forms import NewUserForm
from main.models import Tutorial


def handle_form_errors(request, form):
	for key in form.errors:
		for err in form.errors[key]:
			messages.error(request, f'{key}: {err}' if key != '__all__' else err)


def homepage(request: HttpRequest):
	return render(request, 'main/home.html', {
		'tutorials': Tutorial.objects.all()
	})


def register(request: HttpRequest):
	if request.method == 'POST':
		form = NewUserForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'New account created: {username}')
			login(request, user)
			return redirect('main:homepage')

		handle_form_errors(request, form)

	form = NewUserForm
	return render(request, 'main/register.html', {"form": form})


def logout_request(request: HttpRequest):
	logout(request)
	messages.info(request, 'Logged out')
	return redirect('main:homepage')


def login_request(request: HttpRequest):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			messages.info(request, f'Welcome back, {user.username}!')
			return redirect('main:homepage')

		handle_form_errors(request, form)

	form = AuthenticationForm()
	return render(request, 'main/login.html', {'form': form})