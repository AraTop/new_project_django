from django.shortcuts import render
from django.urls import reverse_lazy
from users.forms import UserForm, UserProfileForm
from users.models import User
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class RegisterView(CreateView):
   model = User
   form_class = UserForm
   template_name = 'users/users_register.html'
   success_url = '/users/login/'

@method_decorator(login_required, name='dispatch')  
class ProfileView(UpdateView):
   model = User
   form_class = UserProfileForm
   success_url = reverse_lazy("users:profile")

   def get_object(self, queryset=None):
      return self.request.user