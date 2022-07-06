from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """Регистрация нового пользователя"""

    if request.method != 'POST':
        register_form = UserCreationForm()
    else:
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            login(request, new_user) 
            return redirect('forum_body:index')
    
    context = {'form':register_form}
    return render(request, 'registration/register.html', context)
    
