import random
from datetime import timezone

from faker import Faker
from django.core.management import BaseCommand, CommandParser

from main.models import Tutorial, TutorialSeries, TutorialCategory


def clean_all_data():
	for Model in [Tutorial, TutorialSeries, TutorialCategory]:
		for item in Model.objects.all():
			item.delete()


class Command(BaseCommand):
	def __init__(self, *args):
		super().__init__(*args)

		self.fake = Faker()

	def add_arguments(self, parser: CommandParser):
		parser.add_argument('--categories', type=int, default=5)
		parser.add_argument('--series', type=int, default=20)
		parser.add_argument('--tutorials', type=int, default=100)

	def generate_categories(self, count):
		results = []
		for i in range(count):
			category = TutorialCategory()
			category.tutorial_category = self.fake.job()
			category.category_summary = self.fake.text(max_nb_chars=200)
			category.category_slug = '-'.join(self.fake.words(nb=random.randint(2, 7)))
			category.save()
			results.append(category)
			self.stdout.write(self.style.NOTICE(f'   Category: {category.tutorial_category}'))
		self.stdout.write(self.style.SUCCESS(f'Generated {count} categories'))
		return results

	def generate_series(self, count, categories):
		results = []
		for i in range(count):
			series = TutorialSeries()
			series.tutorial_series = self.fake.bs()
			series.tutorial_category = random.choice(categories)
			series.series_summary = self.fake.text(max_nb_chars=200)
			series.save()
			results.append(series)
			self.stdout.write(self.style.NOTICE(f'   Series: {series.tutorial_series} (category: {series.tutorial_category.tutorial_category})'))
		self.stdout.write(self.style.SUCCESS(f'Generated {count} series'))
		return results

	def generate_tutorials(self, count, series):
		for i in range(count):
			tutorial = Tutorial()
			tutorial.tutorial_title = self.fake.catch_phrase()
			tutorial.tutorial_content = '<p>' + '</p>\r\n<p>'.join(self.fake.paragraphs(nb=random.randint(10, 50))) + '</p>'
			tutorial.tutorial_series = random.choice(series)
			tutorial.tutorial_published = self.fake.date_time_this_decade(tzinfo=timezone.utc)
			tutorial.tutorial_slug = '-'.join(self.fake.words(nb=random.randint(2, 7)))
			tutorial.save()
			self.stdout.write(self.style.NOTICE(f'   Tutorial: {tutorial.tutorial_title} (series: {tutorial.tutorial_series_id})'))
		self.stdout.write(self.style.SUCCESS(f'Generated {count} tutorials'))

	def handle(self, *args, **options):
		clean_all_data()
		self.stdout.write(self.style.SUCCESS(f'Cleaned all old data'))

		categories = self.generate_categories(options['categories'])
		series = self.generate_series(options['series'], categories)
		self.generate_tutorials(options['tutorials'], series)
		self.stdout.write(self.style.SUCCESS(f'Generated new data'))





