from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Content, Images, Menu, Comment
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    sliderdata = Content.objects.all().order_by('-id')[:4]  # tüm verileri getiriyoruz, 4 tanesini gösteriyorum
    activitydata = Content.objects.filter(type='etkinlik').order_by('-id')[:3]
    announcementdata = Content.objects.filter(type='duyuru').order_by('?')[:3]
    categoriesdata = Content.objects.filter(type='kategori').order_by('?')[:3]  # ? random olarak getirir
    context = {'setting': setting,
               'page': 'home',
               'sliderdata': sliderdata,
               'activitydata': activitydata,
               'announcementdata': announcementdata,
               'categoriesdata': categoriesdata,
               'menu': menu,

               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    context = {'setting': setting, 'menu': menu}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    context = {'setting': setting, 'menu': menu}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # fromdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get(
                'REMOTE_ADDR')  # GÖNDERENİN İP ADRESİNİ ALIYORUM, remote_addr olarak alıp ipye atıyorum
            data.save()  # veritabanına kaydet
            messages.success(request,
                             "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz")  # tek kullanımlık mesaj alanı
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    menu = Menu.objects.all()
    context = {'setting': setting, 'form': form, 'menu': menu}
    return render(request, 'iletisim.html', context)


def menu(request, id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/' + str(content.id) + '/menu'  # menu hangi içerikteyse git onu bul ve calıstır
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "Hata ! İlgili içerik bulunamadı ")
        link = '/error'
        return HttpResponseRedirect(link)



def contentdetail(request, id, slug):
    comments = Comment.objects.filter(content_id=id, status='True')
    menu = Menu.objects.all()
    content = Content.objects.get(pk=id)
    try:

        images = Images.objects.filter(content_id=id)
        context = {
            'content': content,
            'images': images,
            'menu': menu,
            'comments': comments,

        }
        return render(request, 'contents_detail.html', context)
    except:
        messages.warning(request, "Hata ! İlgili içerik bulunamadı ")
        link = '/error'
        return HttpResponseRedirect(link)


def error(request):
    menu = Menu.objects.all()
    context = {
        'menu': menu,

    }
    return render(request, 'error_page.html', context)


def content_search(request):
    if request.method == 'POST':  #check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            content = Content.objects.all()
            menu= Menu.objects.all()
            query = form.cleaned_data['query']  #formdan bilgiyi al
            contents = Content.objects.filter(title__icontains=query) #Select * from content where title like %query%    #icontains=büyük küçük harf dikkate alma demek
            context = {
                'content': content,
                'menu': menu,
                'contents': contents,
                }
            return render(request, 'contents_search.html', context)

    return HttpResponseRedirect('/')