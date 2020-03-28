from django.contrib import admin

# Register your models here.
from content.models import Category, Content, Images

class ContentImageInline(admin.TabularInline): #image tablosundan 5 tane eklenecek alan oluştur
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
   # fields = ['title', 'status'] #dikkate alacağımız kısımları yazarız buraya
     list_display = ['title', 'status', 'image_tag']   #göstermek istediklerimizi yazarız buraya
     list_filter = ['status'] #belirli bir şeye göre filtrelemek istersek
     readonly_fields = ('image_tag',)

class ContentAdmin(admin.ModelAdmin):
   # fields = ['title', 'status'] #dikkate alacağımız kısımları yazarız buraya
     list_display = ['title', 'category', 'detail', 'image_tag', 'status']   #göstermek istediklerimizi yazarız buraya
     list_filter = ['status', 'category'] #belirli bir şeye göre filtrelemek istersek
     inlines = [ContentImageInline] #buraya eklediğimizdesadece ilgili content ile ilgili imageler eklenir
     readonly_fields = ('image_tag',)

class ImagesAdmin(admin.ModelAdmin):
   # fields = ['title', 'status'] #dikkate alacağımız kısımları yazarız buraya
     list_display = ['title', 'content', 'image_tag']   #göstermek istediklerimizi yazarız buraya
     readonly_fields = ('image_tag',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Images, ImagesAdmin)


