import random
import time
from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError
from main.models import Banner, BannerVersion


class Command(BaseCommand):
    "python manage.py put_data --n_features=1000 --clear"
    help = 'Создает записи в соответствии с предоставленными параметрами'

    def add_arguments(self, parser):
        parser.add_argument('--n_features', type=int, 
                            default=1000, help='Количество создаваемых фич')
        parser.add_argument('--clear', action='store_true', 
                            help='Очистить существующие записи перед созданием')

    def clear_existing_data(self):
        BannerVersion.objects.all().delete()
        Banner.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE main_banner_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE main_bannerversion_id_seq \
RESTART WITH 1")

    def handle(self, *args, **kwargs):
        start_time = time.time()
        if kwargs['clear']:
            self.clear_existing_data()

        n_features = kwargs['n_features']

        tag_ids_array = [i for i in range(1, int(n_features * 0.8) + 1)]
        random_indexes = random.sample(range(len(tag_ids_array)), 
                                       min(3, len(tag_ids_array)))
        selected_tags = [tag_ids_array[i] for i in random_indexes]
        total_tags = 0
        for _ in range(n_features):

            while True:
                try:
                    num_tags = random.randint(1, min(3, len(tag_ids_array)))
                    total_tags += num_tags
                    selected_tags = random.sample(tag_ids_array, num_tags)
                    
                    banner = Banner.objects.create(feature_id=random.randint(
                        1, 10**4), tag_ids=selected_tags)
                    break
                except IntegrityError:
                    pass


        end_time = time.time()
        elapsed_time = end_time - start_time

        self.stdout.write(self.style.SUCCESS(
            f'Успешно созданы записи за {elapsed_time:.2f} секунд, '
            f'Количество созданных фич: {n_features}, '
            f'количество тегов: {total_tags}, '
            f'общее количество записей: {n_features + total_tags}'))
        