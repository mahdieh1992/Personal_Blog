from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import CustomUser
from .forms import RegisterForm,LoginForm
from django.views.generic import FormView,TemplateView,View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
# Create your views here.


class RegisterUser(FormView):
    """
        view for sign up users
        if users information valid register user
    """
    template_name='account/Register.html'
    form_class=RegisterForm
    success_url=reverse_lazy('account:login')
 
    def form_valid(self, form):
        password=self.request.POST['password']
        user=form.save(commit=False)
        user.set_password=(password)
        user.is_active=True
        user.save()
        return super().form_valid(form)



    

class LoginUser(View):
    template_name="account/login.html"
    def get(self,request):
        form=LoginForm
        return render(request,self.template_name,{
            'form':form
        })
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
            if user:
                login(request,user)
                return redirect("Home:main")
            form.add_error("email","user does not exists")
        return render(request,self.template_name,{
            'form':form
        })    
