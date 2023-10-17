from openday.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.db import IntegrityError
from django.contrib.auth.views import PasswordChangeView

# Create your views here.
def index(request):
   novita = News.objects.all()
   return render(request,"openday/index.html",{'novita':novita})
