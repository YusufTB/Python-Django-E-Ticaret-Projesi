from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Select, FileInput
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS=(
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=200)
    keywords=models.CharField(blank=True,max_length=200)
    description = models.CharField(blank=True,max_length=200)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField()
    parent=TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path= [self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True,max_length=200)
    description = models.CharField(blank=True,max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    detail=RichTextUploadingField()
    slug = models.SlugField(blank=True,max_length=150)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description='Image'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'slug', 'keywords', 'description', 'image', 'detail']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}),
            'slug': TextInput(attrs={'class': 'form-control', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
            'category': Select(attrs={'class': 'form-control', 'placeholder': 'type'}, choices=Category.objects.all()),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'image'}),
            'detail': CKEditorWidget(),
        }

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description='Image'

class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(blank=True,max_length=50)
    comment = models.TextField(blank=True,max_length=200)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip=models.CharField(blank=True,max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject','comment']

