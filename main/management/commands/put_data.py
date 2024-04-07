import random
import time
from django.core.management.base import BaseCommand
from django.db import connection
from main.models import Feature, Banner, Tag, BannerTag


class Command(BaseCommand):
    "python manage.py put_data --n_features=1000 --clear"
    help = 'Создает записи в соответствии с предоставленными параметрами'

    def add_arguments(self, parser):
        parser.add_argument('--n_features', type=int, 
                            default=1000, help='Количество создаваемых фич')
        parser.add_argument('--clear', action='store_true', 
                            help='Очистить существующие записи перед созданием')

    def clear_existing_data(self):
        BannerTag.objects.all().delete()
        Banner.objects.all().delete()
        Feature.objects.all().delete()
        Tag.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE main_feature_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE main_banner_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE main_tag_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE main_bannertag_id_seq RESTART WITH 1")

    def handle(self, *args, **kwargs):
        start_time = time.time()
        if kwargs['clear']:
            self.clear_existing_data()

        n_features = kwargs['n_features']

        for i in range(1, n_features + 1):
            Feature.objects.get_or_create(feature_id=i)

        for _ in range(1, int(n_features * 1.2) + 1):
            feature_id = random.randint(1, Feature.objects.count())
            feature = Feature.objects.get(feature_id=feature_id)
            Banner.objects.get_or_create(feature=feature)

        for i in range(1, int(n_features * 1.2) + 1):
            Tag.objects.get_or_create(tag_id=i)

        banners = Banner.objects.all().select_related('feature')
        for banner in banners:
            num_tags = random.randint(1, 3)
            for _ in range(num_tags):
                rand_tag = random.randint(1, Tag.objects.count())
                tag = Tag.objects.get(tag_id=rand_tag)
                BannerTag.objects.get_or_create(banner=banner, tag=tag)

        end_time = time.time()
        elapsed_time = end_time - start_time

        self.stdout.write(self.style.SUCCESS(
            f'Успешно созданы записи за {elapsed_time:.2f} секунд'))
