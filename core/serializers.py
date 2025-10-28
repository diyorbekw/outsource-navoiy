from rest_framework import serializers
from .models import (
    Client, FAQ, Blog, Risk,
    OneStopShopProgram, OutSourcingService, Contact,
    SuccessNumber, SpecialCategories, SpecialService,
    Education, InvestorProgram, Statistics, Tax
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
    resident_companies = serializers.SerializerMethodField()
    export_revenue = serializers.SerializerMethodField()
    export_destinations = serializers.SerializerMethodField()
    skilled_specialists = serializers.SerializerMethodField()

    class Meta:
        model = SuccessNumber
        fields = [
            'id',
            'resident_companies',
            'export_revenue', 
            'export_destinations',
            'skilled_specialists'
        ]

    def get_resident_companies(self, obj):
        return {
            "label": "RESIDENT COMPANIES",
            "value": obj.resident_companies
        }

    def get_export_revenue(self, obj):
        return {
            "label": "EXPORT REVENUE", 
            "value": obj.export_revenue
        }

    def get_export_destinations(self, obj):
        return {
            "label": "EXPORT DESTINATIONS",
            "value": obj.export_destinations
        }

    def get_skilled_specialists(self, obj):
        return {
            "label": "SKILLED SPECIALISTS",
            "value": obj.skilled_specialists
        }

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

class EducationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Education
        fields = '__all__'
    
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class InvestorProgramSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestorProgram
        fields = '__all__'
    
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'