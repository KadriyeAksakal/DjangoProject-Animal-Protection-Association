from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Content, Category, Images
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
  setting = Setting.objects.get(pk=1)
  sliderdata = Content.objects.all()[:4]  #tüm verileri getiriyoruz, 4 tanesini gösteriyorum
  category = Category.objects.all()
  daycontents = Content.objects.all()[:4]
  lastcontents = Content.objects.all().order_by('-id')[:4]
  randomcontents = Content.objects.all().order_by('?')[:4]   #? random olarak getirir
  context = {'setting': setting,
             'category': category,
             'page': 'home',
             'sliderdata': sliderdata,  #sliderdatayı contexte ekliyor
             'daycontents': daycontents,
             'lastcontents': lastcontents,
             'randomcontents': randomcontents}
  return render(request, 'index.html', context)

def hakkimizda(request):
  setting = Setting.objects.get(pk=1)
  context = {'setting': setting}
  return render(request, 'hakkimizda.html', context)

def referanslar(request):
  setting = Setting.objects.get(pk=1)
  context = {'setting': setting}
  return render(request, 'referanslarimiz.html', context)

def iletisim(request):

  if request.method == 'POST': #form post edildiyse
    form = ContactFormu(request.POST)
    if form.is_valid():
      data = ContactFormMessage() #model ile bağlantı kur
      data.name = form.cleaned_data['name'] #fromdan bilgiyi al
      data.email = form.cleaned_data['email']
      data.subject = form.cleaned_data['subject']
      data.message = form.cleaned_data['message']
      data.ip = request.META.get('REMOTE_ADDR')  #GÖNDERENİN İP ADRESİNİ ALIYORUM, remote_addr olarak alıp ipye atıyorum
      data.save() #veritabanına kaydet
      messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz")   #tek kullanımlık mesaj alanı
      return HttpResponseRedirect('/iletisim')

  setting = Setting.objects.get(pk=1)
  form = ContactFormu()
  context = {'setting': setting, 'form': form}
  return render(request, 'iletisim.html', context)


def category_contents(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    contents = Content.objects.filter(category_id=id)
    context = {'contents': contents,
               'category': category,
               'categorydata': categorydata,
               }
    return render(request, 'contents.html', context)

def contents_detail(request, id, slug):
    category = Category.objects.all()
    content = Content.objects.get(pk=id)
    images = Images.objects.filter(content_id=id)
    context = {'content': content,
               'category': category,
               'images': images,
               }
    return render(request, 'contents_detail.html', context)