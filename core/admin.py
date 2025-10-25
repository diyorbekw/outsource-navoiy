from django.contrib import admin
from .models import (
    Client, FAQ, Blog, Risk, OneStopShopProgram, 
    OutSourcingService, Contact, SuccessNumber, 
    SpecialCategories, SpecialService
)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'full_name', 'rating')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'minutes_to_read', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

class RiskAdmin(admin.ModelAdmin):
    list_display = ('percent', 'content')

class OneStopShopProgramAdmin(admin.ModelAdmin):
    list_display = ('title',)

class OutSourcingServiceAdmin(admin.ModelAdmin):
    list_display = ('content',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name')

class SuccessNumberAdmin(admin.ModelAdmin):
    list_display = ('resident_companies', 'export_revenue', 'export_destinations', 'skilled_specialists')

class SpecialCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SpecialServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'content')
    list_filter = ('category',)

admin.site.register(Client, ClientAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Risk, RiskAdmin)
admin.site.register(OneStopShopProgram, OneStopShopProgramAdmin)
admin.site.register(OutSourcingService, OutSourcingServiceAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(SuccessNumber, SuccessNumberAdmin)
admin.site.register(SpecialCategories, SpecialCategoriesAdmin)
admin.site.register(SpecialService, SpecialServiceAdmin)