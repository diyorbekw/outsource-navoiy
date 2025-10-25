from rest_framework import serializers
from .models import (
    Client, FAQ, Blog, Risk,
    OneStopShopProgram, OutSourcingService, Contact,
    SuccessNumber, SpecialCategories, SpecialService
)

class ClientSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = '__all__'
    
    def get_profile_photo(self, obj):
        if obj.profile_photo:
            return self.context['request'].build_absolute_uri(obj.profile_photo.url)
        return None

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    content_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
    
    def get_main_image(self, obj):
        if obj.main_image:
            return self.context['request'].build_absolute_uri(obj.main_image.url)
        return None
    
    def get_content_image(self, obj):
        if obj.content_image:
            return self.context['request'].build_absolute_uri(obj.content_image.url)
        return None

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = '__all__'

class OneStopShopProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneStopShopProgram
        fields = '__all__'

class OutSourcingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutSourcingService
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class SuccessNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessNumber
        fields = '__all__'

class SpecialCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialCategories
        fields = '__all__'

class SpecialServiceSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = SpecialService
        fields = '__all__'
    
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None