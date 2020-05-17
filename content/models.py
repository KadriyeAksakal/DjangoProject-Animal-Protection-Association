from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.forms import TextInput, Select, FileInput



class Menu(MPTTModel):
    STATUS = (  # açılan kutuda buranın gelmesini istiyoruz
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE) #model.CASCADE bir şey silineceği zaman ona bağlı şeyleri de silmeyi istediğimiz zaman kullanırız.
    title = models.CharField(max_length=100, unique=True) #charfield=uzunluk, alan türü
    link = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(
            full_path[::-1])  # bunun amacı alt kategori olduğu sürece buluyor ve istediğimiz sıra ile bize getiriyor



TYPE = ( #global olarak çağırabilmek için dışarı aldım
        ('menu', 'menu'),
        ('haber', 'haber'),
        ('etkinlik', 'etkinlik'),
        ('duyuru', 'duyuru'),
    )

class Content(models.Model):
    STATUS = (  #açılan kutuda buranın gelmesini istiyoruz
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) #usera içerik ekleme yetkisi verdiğimiz için bunu yazıyoruz
    menu = models.OneToOneField(Menu, null=True, blank=True, on_delete=models.CASCADE) #relation with menu table
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

    def get_absolute_url(self):
        return reverse('content_detail', kwargs={'slug': self.slug})  #otomatik slug olusturma




class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['type', 'title', 'slug', 'keywords', 'description', 'image', 'detail']  # bu elemanlar gözükecek
        widgets = {
            'type': Select(attrs={'class': 'input', 'placeholder': 'type'}, choices=TYPE),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'detail': CKEditorWidget(),  #ckeditor input, widget içerisinde kullandığım için böyle yazıyorum
        }

class Images(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True) #charfield=uzunluk, alan türü, blank=true dersek boş geçmemize izin verir
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ContentImageForm(ModelForm):   #eğer bir validation yani kontrol yapmak için kullanmak istersek ya da çağırmak istersek diye form yaptık
    class Meta:
        model =Images
        fields = ['title', 'image']


class Comment(models.Model):
    STATUS = (  # açılan kutuda buranın gelmesini istiyoruz
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment']











