from django.contrib import admin
from .models import (
    Client, FAQ, Blog, Risk, OneStopShopProgram, 
    OutSourcingService, Contact, SuccessNumber, 
    SpecialCategories, SpecialService, Education,
    InvestorProgram, Statistics, Tax
)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'full_name', 'rating')
    search_fields = ('company_name', 'full_name')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question', 'answer')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'minutes_to_read', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'content', 'creator')

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('percent', 'content')
    search_fields = ('content',)

@admin.register(OneStopShopProgram)
class OneStopShopProgramAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')

@admin.register(OutSourcingService)
class OutSourcingServiceAdmin(admin.ModelAdmin):
    list_display = ('content',)
    search_fields = ('content',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'phone_number')
    list_filter = ('company_name',)
    search_fields = ('first_name', 'last_name', 'email', 'company_name')

@admin.register(SuccessNumber)
class SuccessNumberAdmin(admin.ModelAdmin):
    list_display = ('resident_companies', 'export_revenue', 'export_destinations', 'skilled_specialists')

@admin.register(SpecialCategories)
class SpecialCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(SpecialService)
class SpecialServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'content')
    list_filter = ('category',)
    search_fields = ('content', 'category__title')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(InvestorProgram)
class InvestorProgramAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')

@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('employed_professionals', 'companies', 'professionals_count', 'coverage')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('corporate_taxes', 'property_and_land_taxes', 'tax_on_dividends', 
                   'billion_turnover_tax', 'social_tax', 'vat_on_imported_services')