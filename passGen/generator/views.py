from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.

def home(request):
    return render(request,'generator/home.html',{})

def password(request):
    character = list('abdefghijklmnopqrstuvwxyz')

    if request.GET.get('caps'):
        character.extend(list('ABCDEFGHOJKLMNOPQRSTUVWXYZ'))
    if request.GET.get('nums'):
        character.extend(list('1234567890'))
    if request.GET.get('special'):
        character.extend(list(',.[]{}*!#$%&/()=?¡'))
    
    length = int(request.GET.get('length','12'))
    thepassword = ''

    for x in range(length):
        thepassword += random.choice(character)
    
    return render(request,'generator/password.html',{'password':thepassword})