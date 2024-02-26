from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def index(request):
    users = User.objects.all().order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'users/index.html', context)


class EmployeeCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:index")


def update(request, name):
    user = User.objects.get(name=name)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("users:index")
        else:
            context = {
                "form": form,
            }
            return render(request, "update.html", context)
        
    else:
        form = UserForm(instance=user)
        context = {
            "form": form,
        }
    return render(request, 'users/update.html', context)


def delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect("users:index")


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = "products:index"
    
    
class UserLogoutView(LogoutView):
    next_page = "users:login"