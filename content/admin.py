from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

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
     list_filter = ['status'] #belirli bir şeye göre filtrelemek istersek
     inlines = [ContentImageInline] #buraya eklediğimizdesadece ilgili content ile ilgili imageler eklenir
     readonly_fields = ('image_tag',)

class ImagesAdmin(admin.ModelAdmin):
   # fields = ['title', 'status'] #dikkate alacağımız kısımları yazarız buraya
     list_display = ['title', 'content', 'image_tag']   #göstermek istediklerimizi yazarız buraya
     readonly_fields = ('image_tag',)


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_contents_count', 'related_contents_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Content,
                'category',
                'contents_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
                 qs,
                 Content,
                 'category',
                 'contents_count',
                 cumulative=False)
        return qs

    def related_contents_count(self, instance):
        return instance.contents_count
    related_contents_count.short_description = 'Related contents (for this specific category)'

    def related_contents_cumulative_count(self, instance):
        return instance.contents_cumulative_count
    related_contents_cumulative_count.short_description = 'Related contents (in tree)'


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Content, ContentAdmin)
admin.site.register(Images, ImagesAdmin)


