from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import CommentForm, Comment


def index(request):
      return HttpResponse(" Content Page")

@login_required(login_url='/login') #check login
def addcomment(request, id):

      url = request.META.get('HTTP_REFERER')  # get last url
      if request.method == 'POST': #form post edildiyse
            form = CommentForm(request.POST)
            if form.is_valid():
                  current_user = request.user #Access User Session Information

                  data = Comment() #model ile bağlantı kur
                  data.user_id = current_user.id
                  data.content_id = id
                  data.subject = form.cleaned_data['subject']
                  data.comment = form.cleaned_data['comment']
                  data.ip = request.META.get('REMOTE_ADDR') #Client computer ip address
                  data.save()  #veritabanına  kaydet
                  messages.success(request, 'Yorumunuz başarı ile gönderilmiştir. Teşekkür ederiz!')
                  return HttpResponseRedirect(url)

            messages.warning(request, 'Yorumunuz kaydedilmedi. Lütfen konrol ediniz.')
            return  HttpResponse('Kaydedilme İşlemi Gerçekleşmedi')
