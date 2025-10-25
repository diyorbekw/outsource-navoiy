from django.db import models
from ckeditor.fields import RichTextField

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile_photos/')
    description = models.TextField()
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
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=120)
    content = RichTextField()
    creator = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='blog_main_images/')
    content_image = models.ImageField(upload_to='blog_content_images/')
    minutes_to_read = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ['-created_at']

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
    content = models.CharField(max_length=400)
    image = models.ImageField(upload_to='special_services/')

    def __str__(self):
        return f"{self.category.title} - {self.content}"
    
    class Meta:
        verbose_name = "Special Service"
        verbose_name_plural = "Special Services"