from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from content.models import Content, Images, Comment, Menu


class ContentImageInline(admin.TabularInline): #image tablosundan 2 tane eklenecek alan oluştur
    model = Images
    extra = 2


class ContentAdmin(admin.ModelAdmin):
   # fields = ['title', 'status'] #dikkate alacağımız kısımları yazarız buraya
     list_display = ['title', 'detail', 'image_tag', 'status']   #göstermek istediklerimizi yazarız buraya
     list_filter = ['status', 'type'] #belirli bir şeye göre filtrelemek istersek
     inlines = [ContentImageInline] #buraya eklediğimizdesadece ilgili content ile ilgili imageler eklenir
     prepopulated_fields = {'slug': ('title',)}  #otomatik slag olusturması icin



class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'title'
    list_display = ('tree_actions', 'indented_title', 'status')


class CommentAdmin(admin.ModelAdmin):
    list_display= ['subject', 'comment', 'content', 'user', 'status']  # dikkate alacağımız kısımları yazarız buraya
    list_fields = ['status']


admin.site.register(Content, ContentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Menu, MenuAdmin)



