from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS = (  #açılan kutuda buranın gelmesini istiyoruz
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=100) #charfield=uzunluk, alan türü
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/') #imagefieldla tipini belirtiyorum daha sonra hangi klasörden yükleneceğini upload to da belirtiyorum.
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField() #id yerine metin değişkeni ile çağırmak istersek buna slug denir
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE) #model.CASCADE bir şey silineceği zaman ona bağlı şeyleri de silmeyi istediğimiz zaman kullanırız.
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    #pythonın görmemiz için bize bir şey döndürmesini istiyoruz
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Content(models.Model):
    STATUS = (  #açılan kutuda buranın gelmesini istiyoruz
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #relation with category table
    title = models.CharField(max_length=100) #charfield=uzunluk, alan türü
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(blank=True, max_length=100) #id yerine metin değişkeni ile çağırmak istersek buna slug denir
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    #pythonın görmemiz için bize bir şey döndürmesini istiyoruz
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Images(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True) #charfield=uzunluk, alan türü, blank=true dersek boş geçmemize izin verir
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


