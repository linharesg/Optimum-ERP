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
    """
    Exibe uma lista de todos os usuários cadastrados.

    Returns:
        HttpResponse: Renderiza a página HTML com a lista de usuários.
    """
    users = User.objects.all().order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'users/index.html', context)


class EmployeeCreateView(CreateView):
    """
    View para criar um novo usuário (funcionário).

    Atributos:
        model (Model): O modelo do banco de dados para criar o usuário.
        form_class (Form): O formulário para criar o usuário.
        template_name (str): O nome do template HTML para renderizar a página.
        success_url (str): A URL para redirecionar após a criação bem-sucedida do usuário.
    """
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:index")


def update(request, name):
    """
    View para atualizar as informações de um usuário existente.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        name (str): O nome do usuário a ser atualizado.

    Returns:
        HttpResponse: Renderiza o formulário de atualização do usuário.
    """
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
    """
    View para excluir um usuário existente.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        id (int): O ID do usuário a ser excluído.

    Returns:
        HttpResponseRedirect: Redireciona para a página de listagem de usuários após a exclusão.
    """
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect("users:index")


class UserLoginView(LoginView):
    """
    View para login de usuários.

    Atributos:
        template_name (str): O nome do template HTML para renderizar a página de login.
        redirect_authenticated_user (bool): Define se os usuários autenticados serão redirecionados automaticamente.
        next_page (str): A URL para redirecionar após o login bem-sucedido.
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = "products:index"
    
    
class UserLogoutView(LogoutView):
    """
    View para logout de usuários.

    Atributos:
        next_page (str): A URL para redirecionar após o logout bem-sucedido.
    """
    next_page = "users:login"