from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from main.forms import NewUserForm
from main.models import Tutorial, TutorialCategory, TutorialSeries


def handle_form_errors(request, form):
	for key in form.errors:
		for err in form.errors[key]:
			messages.error(request, f'{key}: {err}' if key != '__all__' else err)


def category_or_tutorial(request: HttpRequest, slug):
	category = TutorialCategory.objects.filter(category_slug=slug).first()
	if category is not None:
		return serve_category(request, category)

	tutorial = Tutorial.objects.filter(tutorial_slug=slug).first()
	if tutorial is not None:
		return serve_tutorial(request, tutorial)

	return HttpResponse('Slug not found')


def serve_category(request: HttpRequest, category: TutorialCategory):
	series_list = TutorialSeries.objects.filter(tutorial_category__category_slug=category.category_slug)
	data = {}
	for s in series_list:
		part_one = Tutorial.objects.filter(tutorial_series=s).earliest('tutorial_published')
		data[s] = part_one

	return render(request, 'main/category.html', {
		'data': data,
		'category': category
	})


def serve_tutorial(request: HttpRequest, tutorial: Tutorial):
	siblings = Tutorial.objects\
		.filter(tutorial_series=tutorial.tutorial_series)\
		.order_by('tutorial_published')
	return render(request, 'main/tutorial.html', {
		'tutorial': tutorial,
		'siblings': siblings
	})


def homepage(request: HttpRequest):
	return render(request, 'main/categories.html', {
		'categories': TutorialCategory.objects.all()
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