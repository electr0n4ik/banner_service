import random
import time
from django.core.management.base import BaseCommand
from main.models import Feature, Banner, Tag, BannerTag


class Command(BaseCommand):
    help = 'Создает записи в соответствии с предоставленными параметрами'

    def add_arguments(self, parser):
        parser.add_argument('--n_features', type=int, 
                            default=1000, help='Количество создаваемых фич')

    def handle(self, *args, **kwargs):
        start_time = time.time()
        n_features = kwargs['n_features']
        
        # Создаем фичи
        for i in range(n_features):
            feature, _ = Feature.objects.get_or_create(feature_id=i + 1)

        # Создаем баннеры
        n_banners = int(n_features * 1.2)  # Больше на 20%
        for i in range(n_banners):
            feature_id = random.randint(1, n_features)
            feature = Feature.objects.get(feature_id=feature_id)
            banner, _ = Banner.objects.get_or_create(feature=feature)

        # Создаем теги
        n_tags = int(n_features * 1.2)  # Больше на 20%
        for i in range(n_tags):
            tag_id = random.randint(1, n_tags)
            tag, _ = Tag.objects.get_or_create(tag_id=tag_id)

        # Создаем связи BannerTag
        for banner in Banner.objects.all():
            num_tags = random.randint(1, 3)  # Не более 3 тегов на баннере
            for _ in range(num_tags):
                rand_tag = random.randint(1, n_tags)
                tag = Tag.objects.get(tag_id=rand_tag)
                BannerTag.objects.get_or_create(banner=banner, tag=tag)

        end_time = time.time()
        elapsed_time = end_time - start_time

        self.stdout.write(self.style.SUCCESS(
            f'Успешно созданы записи за {elapsed_time:.2f} секунд'))
