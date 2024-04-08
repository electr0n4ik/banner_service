from rest_framework import serializers


# class BannerViewSerializer(serializers.Serializer):
#     class Meta:
#         fields = '__all__'
class BannerViewSerializer(serializers.Serializer):
    banner_id = serializers.IntegerField(read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(read_only=True))
    feature_id = serializers.IntegerField(read_only=True)
    content = serializers.JSONField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_banner_id(self, context):
        # Получаем данные из контекста
        banner_id = context.get('banner_id')
        return banner_id
    
    def to_representation(self, instance):
        # Получаем данные из контекста
        context = self.context
        banner_id = self.get_banner_id(context)

        # Сериализуем данные
        data = super().to_representation(instance)
        data['banner_id'] = banner_id
        return data

