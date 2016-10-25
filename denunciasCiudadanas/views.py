from django.shortcuts import render
from rest_framework import viewsets
from denunciasCiudadanas.models import Denuncia, Cuenta
from denunciasCiudadanas.serializers import DenunciaSerializer, CuentaSerializer
from rest_framework import permissions
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json


class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

@csrf_exempt
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    nextt=""
    if request.GET:
        nextt=request.GET['next']
        
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponse(json.dumps(state))
                
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return HttpResponse(json.dumps(state))

@csrf_exempt
def check_login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'result': {'logged': True}, 'username':request.user.username}),
                        content_type="application/json")
    else:
        return HttpResponse(json.dumps({'result': {'logged': False}}),
                        content_type="application/json")

@csrf_exempt
def logout_user(request):
    logout(request)
    return HttpResponse("Ha cerrado sesion con exito")

@csrf_exempt
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print "returning FORWARDED_FOR"
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        print "returning REAL_IP"
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        print "returning REMOTE_ADDR"
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip)

def get_ip_info(request):
  ip=get_client_ip(request)
  url='http://ip-api.com/json/'
  if ip:
    return json.load(urlopen(url+ip))
  else:
    return None

