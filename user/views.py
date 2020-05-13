from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from content.models import Menu, Content, ContentForm
from home.models import UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    menu = Menu.objects.all()
    current_user = request.user  # Access User Session Information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'menu': menu,
        'profile': profile,
    }
    return render(request, 'user_profile.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profiliniz başarı ile güncellendi !')
            return redirect('/user')

    else:
        menu = Menu.objects.all()
        current_user = request.user  # Access user session information
        user_form = UserUpdateForm(instance=request.user)  # userla ilişki kursun diyorum
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user =>yani user tablosundaki userprofileı onetoone ilişkisine göre getir diyorum
    context = {
        'menu': menu,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # important
            messages.success(request, 'Şifreniz başarılı bir şekilde değiştirildi !')
            return HttpResponseRedirect("/user")
        else:
            messages.error(request, 'Hata ! Lütfen kontrol ederek tekrar deneyiniz.<br>' + str(
                form.errors))  # bunu buraya yazabilmemiz için stringe çevirmemiz lazım on yüzden str yazıyoruz
            return HttpResponseRedirect('/user/password')

    else:
        menu = Menu.objects.all()
        form = PasswordChangeForm(request.user)  # sadece mevcut kullancının bilgilerini al getir
        return render(request, 'change_password.html', {
            'form': form, 'menu': menu
        })


def comments(request):
    return HttpResponse("yorumlar")


def deletecomment(request):
    return HttpResponse("yorumlar")


@login_required(login_url='/login')  # check login, login olup olmadığını kontrol ediyorum
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)  # fileupload varsa request.FILES yapmazsak formumuz çalışmaz
        if form.is_valid():
            current_user = request.user
            data = Content()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()  # veritabanına kaydet
            messages.success(request, 'İçeriğiniz başarılı bir şekilde eklendi !')
            return HttpResponseRedirect("/user/contents")
        else:
            messages.error(request, 'İçerik Form Hatası : ' + str(
                form.errors))  # bunu buraya yazabilmemiz için stringe çevirmemiz lazım on yüzden str yazıyoruz
            return HttpResponseRedirect('/user/addcontent')
    else:
        menu = Menu.objects.all()
        form = ContentForm()  # content form ile ilişki kuruyorum
        context = {
            'form': form,
            'menu': menu
        }
        return render(request, 'user_addcontent.html', context)





@login_required(login_url='/login')  # check login, login olup olmadığını kontrol ediyorum
def contents(request):
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)  # mevcut userın contentlerini çağırıyorum
    context = {
        'menu': menu,
        'contents': contents,
    }
    return render(request, 'user_contents.html', context)




@login_required(login_url='/login')  # check login, login olup olmadığını kontrol ediyorum
def contentedit(request):
    content = Content.objects.get(id=id) #mevcut içeriğin id'sini gönderiyorum
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)  # fileupload varsa request.FILES yapmazsak formumuz çalışmaz
        if form.is_valid():
            form.save()  # veritabanına kaydet
            messages.success(request, 'İçeriğiniz başarılı bir şekilde güncellendi !')
            return HttpResponseRedirect("/user/contents")
        else:
            messages.error(request, 'İçerik Form Hatası : ' + str(form.errors))  # bunu buraya yazabilmemiz için stringe çevirmemiz lazım on yüzden str yazıyoruz
            return HttpResponseRedirect('/user/contentedit/'+str(id)) #id'yi tekrar oluşturmam lazım
    else:
        menu = Menu.objects.all()
        form = ContentForm(instance=content)  # content form ile ilişki kuruyorum, sorgulanan contentle formu dolduruyorum
        context = {
            'form': form,
            'menu': menu
        }
        return render(request, 'user_addcontent.html', context)



@login_required(login_url='/login')  # check login, login olup olmadığını kontrol ediyorum
def contentdelete(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'İçerik silindi...')
    return HttpResponseRedirect("/user/contents")
