from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel



class Category(MPTTModel):
    STATUS = (  # açılan kutuda buranın gelmesini istiyoruz
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    TYPE = (
        ('menu', 'menu'),
        ('activity', 'activity'),  # etkinlik
        ('announcement', 'announcement'),  # duyuru
    )
    title = models.CharField(max_length=100) #charfield=uzunluk, alan türü
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/') #imagefieldla tipini belirtiyorum daha sonra hangi klasörden yükleneceğini upload to da belirtiyorum.
    status = models.CharField(max_length=10, choices=STATUS)
    type = models.CharField(max_length=20, choices=TYPE)

    slug = models.SlugField() #id yerine metin değişkeni ile çağırmak istersek buna slug denir
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE) #model.CASCADE bir şey silineceği zaman ona bağlı şeyleri de silmeyi istediğimiz zaman kullanırız.
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']


    #pythonın görmemiz için bize bir şey döndürmesini istiyoruz
    def __str__(self):
        return self.title

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])  #bunun amacı alt kategori olduğu sürece buluyor ve istediğimiz sıra ile bize getiriyor

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Content(models.Model):
    STATUS = (  #açılan kutuda buranın gelmesini istiyoruz
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    TYPE = (
        ('activity', 'activity'),  # etkinlik
        ('announcement', 'announcement'),  # duyuru
        ('categories', 'categories'),  # duyuru

    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE) #relation with category table
    title = models.CharField(max_length=100) #charfield=uzunluk, alan türü
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(blank=True, max_length=100) #id yerine metin değişkeni ile çağırmak istersek buna slug denir
    type = models.CharField(max_length=20, choices=TYPE)
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


