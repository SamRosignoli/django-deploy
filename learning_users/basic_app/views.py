from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
#requires a user to be logged in to view a page
from django.contrib.auth.decorators import login_required

def index(request):
  return render(request, 'basic_app/index.html')

def register(request):
  registered = False
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      # we do not want to commit to the database yet
      # because there might be errors trying to override the user above
      profile = profile_form.save(commit=False)
      profile.user = user

      #request.FILES gest files uploaded in the request, including images, pdf, csv etc
      if 'profile_pic' in request.FILES:
        profile.profile_pic = request.FILES['profile_pic']

      profile.save()
      registered = True
    else:
      print(user_form.errors, profile_form.errors)
  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()

  context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
  return render(request, 'basic_app/registration.html', context)


def user_login(request):
  if request.method == 'POST':
    #the name of the input
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user:
      if user.is_active:
        login(request, user)
        #go back to the home page
        return HttpResponseRedirect(reverse('index'))
      else:
        return HttpResponse('Account not active')
    else:
      print('Someone tried to login and failed')
      print('Username ' + username)
      return HttpResponse('Invalid login details supplied!')
  else:
    return render(request, 'basic_app/login.html', {})


#requires user to be logged in
@login_required
def special(request):
  return render(request, 'basic_app/special.html', {})


#requires user to be logged in
@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))