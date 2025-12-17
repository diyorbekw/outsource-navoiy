from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile_photos/')
    description = models.TextField(max_length=140)
    rating = models.IntegerField()
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        
class Blog(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=120)
    content = RichTextField()
    creator = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='blog_main_images/')
    content_image = models.ImageField(upload_to='blog_content_images/')
    minutes_to_read = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

class Risk(models.Model):
    percent = models.FloatField()
    content = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.percent}% - {self.content}"
    
    class Meta:
        verbose_name = "Risk"
        verbose_name_plural = "Risks"
        
class OneStopShopProgram(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "One Stop Shop Program"
        verbose_name_plural = "One Stop Shop Programs"
        
class OutSourcingService(models.Model):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content
    
    class Meta:
        verbose_name = "Out Sourcing Service"
        verbose_name_plural = "Out Sourcing Services"
        
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    text = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        
class SuccessNumber(models.Model):
    resident_companies = models.IntegerField()
    export_revenue = models.IntegerField()
    export_destinations = models.IntegerField()
    skilled_specialists = models.IntegerField()
    
    def __str__(self):
        return "Success Numbers"
    
    class Meta:
        verbose_name = "Success Number"
        verbose_name_plural = "Success Numbers"
        
class SpecialCategories(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Special Category"
        verbose_name_plural = "Special Categories"
        
class SpecialService(models.Model):
    category = models.ForeignKey(SpecialCategories, on_delete=models.CASCADE)
    content = models.TextField(max_length=400)
    image = models.ImageField(upload_to='special_services/')

    def __str__(self):
        return f"{self.category.title} - {self.content}"
    
    class Meta:
        verbose_name = "Special Service"
        verbose_name_plural = "Special Services"
        
class Education(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='education_images/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Education & Talent Development"
        verbose_name_plural = "Educations & Talent Developments"
        
class InvestorProgram(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='investor_programs/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Investor Program"
        verbose_name_plural = "Investor Programs"
        
class Statistics(models.Model):
    employed_professionals = models.IntegerField()
    companies = models.IntegerField()
    professionals_count = models.IntegerField()
    coverage = models.CharField(max_length=255)
    
    def __str__(self):
        return "Statistics"
    
    class Meta:
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"
        
class Tax(models.Model):
    corporate_taxes = models.FloatField()
    property_and_land_taxes = models.FloatField()
    tax_on_dividends = models.FloatField()
    billion_turnover_tax = models.FloatField()
    social_tax = models.FloatField()
    vat_on_imported_services = models.BooleanField()
    personal_income_tax = models.FloatField()
    value_added_tax = models.FloatField()
    
    def __str__(self):
        return "Tax Information"
    
    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"

class Set(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sets/')
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Set"
        verbose_name_plural = "Sets"
        
class SliderImage(models.Model):
    slider = models.ForeignKey('Slider', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sliders/')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
    
    def __str__(self):
        return f"Slider {self.slider.id} - Image {self.order}"

class Slider(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, help_text="Slider nomi (ixtiyoriy)")
    
    def __str__(self):
        return f"Slider {self.id}" + (f" - {self.name}" if self.name else "")
    
    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"