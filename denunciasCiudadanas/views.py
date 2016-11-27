from django.shortcuts import render
from rest_framework import viewsets
from denunciasCiudadanas.models import Denuncia, Cuenta, Municipio, Departamento
from denunciasCiudadanas.serializers import DepMunSerializer, DepartamentoSerializer, MunicipioSerializer, DenunciaSerializer, CuentaSerializer, FiltroDenunciaSerializer
from rest_framework import permissions
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from denunciasCiudadanas.twoStepVer import RegistrationView, ActivationView
from django.contrib.auth.decorators import login_required
from denunciasCiudadanas.email import send_email
import urllib2
import json
import jwt

class DenunciaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DenunciaSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        user=self.request.user
        if user.is_authenticated():
            cuenta=Cuenta.objects.get(usuario=user)
            if cuenta.tipo=='1':
                return Denuncia.objects.exclude(estado='DE')
            else:
                return Denuncia.objects.filter(cuenta=cuenta)
        else:
            token=self.request.POST.get('token')
            if token is None:
                return None
            else: #USAR EL TOKEN
                decoded=jwt.decode(token, verify=False)
                user=User.objects.get(id=int(decoded['user_id']))
                cuenta=Cuenta.objects.get(usuario=user)
                if cuenta.tipo=='1':
                    return Denuncia.objects.exclude(estado='DE')
                else:
                    return Denuncia.objects.filter(cuenta=cuenta)
            

class CuentaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CuentaSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        user=self.request.user
        if user.is_authenticated():
            return Cuenta.objects.filter(usuario=user)
        else:
            token=self.request.POST.get('token')
            if token is None:
                return None
            else: #USAR EL TOKEN
                decoded=jwt.decode(token, verify=False)
                user=User.objects.get(id=int(decoded['user_id']))
                return Cuenta.objects.filter(usuario=user)

class FiltroViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FiltroDenunciaSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        user=self.request.user
        if user.is_authenticated():
            cuenta=Cuenta.objects.get(usuario=user)
            if cuenta.tipo=='1':
                categoria=self.request.GET.get('categoria')
                estado=self.request.GET.get('estado')
                return Denuncia.objects.filter(categoria=categoria, estado=estado)
            else:
                return None
        else:
            token=self.request.POST.get('token')
            if token is None:
                return None
            else: #USAR EL TOKEN
                decoded=jwt.decode(token, verify=False)
                user=User.objects.get(id=int(decoded['user_id']))
                cuenta=Cuenta.objects.get(usuario=user)
                if cuenta.tipo=='1':
                    categoria=self.request.GET.get('categoria')
                    estado=self.request.GET.get('estado')
                    return Denuncia.objects.filter(categoria=categoria, estado=estado)
                else:
                    return None

class MunicipioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MunicipioSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        user=self.request.user
        if user.is_authenticated():
            cuenta=Cuenta.objects.get(usuario=user)
            if cuenta.tipo=='1':
                #categoria=self.request.GET.get('categoria')
                departamento=int(self.request.GET.get('departamento','0'))
                return Municipio.objects.filter(departamento_id=departamento)
            else:
                return None
        else:
            token=self.request.POST.get('token')
            if token is None:
                return None
            else: #USAR EL TOKEN
                decoded=jwt.decode(token, verify=False)
                user=User.objects.get(id=int(decoded['user_id']))
                cuenta=Cuenta.objects.get(usuario=user)
                if cuenta.tipo=='1':
                    #categoria=self.request.GET.get('categoria')
                    departamento=int(self.request.GET.get('departamento','0'))
                    return Municipio.objects.filter(departamento_id=departamento)
                else:
                    return None

class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DepartamentoSerializer
    permission_classes = (permissions.AllowAny,)
    queryset=Departamento.objects.all()

class DepMunViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DepMunSerializer
    permission_classes = (permissions.AllowAny,)
    queryset=Municipio.objects.all()
    

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
    return str(ip)

def get_ip_info(request):
  ip=get_client_ip(request)
  url='http://ip-api.com/json/'
  return json.load(urllib2.urlopen(url+ip))

@csrf_exempt
def registrar_usuario(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email=request.POST.get('email')
        dui=request.POST.get('dui')
        try:
            #if not Cuenta.objects.get(dui=dui):
            #    raise ValueError
            usuario=User.objects.create_user(username=username,
                                     first_name=first_name, last_name=last_name,
                                     email=email,password=password,
                                     is_active=False)
            cuenta=Cuenta(usuario=usuario, tipo='2', dui=dui)
            cuenta.full_clean()
            cuenta.save()
            reg=RegistrationView()
            mensaje=RegistrationView.send_activation_email(reg,usuario)+" Revise su correo electronico para verificar su cuenta."
        except:
            mensaje="Ese nombre de usuario y/o DUI ya existen."
    else:
        mensaje="No se encontro POST data."
    return HttpResponse(json.dumps(mensaje))

@csrf_exempt
def verificar_usuario(request):
    if request.POST:
        act=ActivationView()
        activation_key=request.POST.get('activation_key')
        usuario=ActivationView.activate(act,activation_key=activation_key)
        if usuario is not None:
            mensaje="Ya puede iniciar sesion."
        else:
            mensaje="Su codigo es incorrecto o ya ha expirado."
    else:
        mensaje="No se encontro POST data."
    return HttpResponse(json.dumps(mensaje))

@csrf_exempt
def crear_denuncia(request): 
    if request.POST and request.user.is_authenticated():
        ip_info=get_ip_info(request)
        lat=str(ip_info['lat'])
        lon=str(ip_info['lon'])
        titulo=request.POST.get('titulo')
        descripcion=request.POST.get('descripcion')
        dep=request.POST.get('departamento')
        mun=request.POST.get('municipio')
        direccion=request.POST.get('direccion')
        municipio=Municipio.objects.get(id=int(mun))
        ubicacionGeo=Departamento.objects.get(id=int(dep)).nombre + ", " + municipio.nombre + ", " + direccion
        ubicacionGeoRef="("+lat+","+lon+")"
        categoria=request.POST.get('categoria')
        if request.POST.get('prueba'):
            prueba=request.POST.get('prueba')
        else:
            prueba=None

        try:
            usuario=request.user
            cuenta=Cuenta.objects.get(usuario=usuario)
            denuncia=Denuncia(titulo=titulo, descripcion=descripcion,
                              cuenta=cuenta, ubicacionGeo=ubicacionGeo,
                              ubicacionGeoRef=ubicacionGeoRef, municipio=municipio,
                              prueba=prueba, categoria=categoria)
            denuncia.full_clean()
            denuncia.save()
            municipio.cuentaDenuncia+=1
            municipio.save()
            mensaje=send_email(usuario.email, "Su denuncia fue recibida y ha sido guardada con extio, si su denuncia es aceptada se le notificara en mensajes posteriores.")
        except:
            mensaje="Algo salio mal, asegurese de enviar los datos correctos: titulo, descripcion, departamento, muncipio, direccion, categoria y prueba."
    else:
        token=request.POST.get('token')
        if token is None:
            mensaje="No se encontro POST data, asegurese de iniciar sesion."
        else: #USAR EL TOKEN
            ip_info=get_ip_info(request)
            lat=str(ip_info['lat'])
            lon=str(ip_info['lon'])
            titulo=request.POST.get('titulo')
            descripcion=request.POST.get('descripcion')
            dep=request.POST.get('departamento')
            mun=request.POST.get('municipio')
            direccion=request.POST.get('direccion')
            municipio=Municipio.objects.get(id=int(mun))
            ubicacionGeo=Departamento.objects.get(id=int(dep)).nombre + ", " + municipio.nombre + ", " + direccion
            ubicacionGeoRef="("+lat+","+lon+")"
            categoria=request.POST.get('categoria')
            prueba=request.POST.get('prueba')
            try:
                decoded=jwt.decode(token, verify=False)
                usuario=User.objects.get(id=int(decoded['user_id']))
                cuenta=Cuenta.objects.get(usuario=usuario)
                denuncia=Denuncia(titulo=titulo, descripcion=descripcion,
                                  cuenta=cuenta, ubicacionGeo=ubicacionGeo,
                                  ubicacionGeoRef=ubicacionGeoRef, municipio=municipio,
                                  prueba=prueba, categoria=categoria)
                denuncia.full_clean()
                denuncia.save()
                municipio.cuentaDenuncia+=1
                municipio.save()
                mensaje=send_email(usuario.email, "Su denuncia fue recibida y ha sido guardada con extio, si su denuncia es aceptada se le notificara en mensajes posteriores.")
            except:
                mensaje="Algo salio mal, asegurese de enviar los datos correctos, puede ser que el token haya sido incorrecto."
            #mensaje="No se encontro POST data, asegurese de iniciar sesion."
    return HttpResponse(json.dumps(mensaje))

@csrf_exempt
def cambiar_estado(request):
    usuario=request.user
    if request.POST and usuario.is_authenticated():
        cuenta=Cuenta.objects.get(usuario=usuario)
        if cuenta.tipo=='1':
            try:
                idDenuncia=int(request.POST.get('id'))
                estado=request.POST.get('estado')
                denuncia=Denuncia.objects.get(id=idDenuncia)
                denuncia.estado=estado
                denuncia.full_clean()
                denuncia.save()            
                mensaje=send_email(denuncia.cuenta.usuario.email, "Su denuncia ha cambiado de estado, revise su cuenta para saber mas al respecto.")
            except:
                mensaje="Puede ser que no se haya encontrado el id o el estado en el POST, tambien es posible que no exista ese id de denuncia o que el estado enviado no sea valido."
        else:
            mensaje="Debe ser investigador para cambiar estados"
    else:
        token=request.POST.get('token')
        if token is None:
            mensaje="No se encontro token"
        else: #USAR EL TOKEN
            decoded=jwt.decode(token, verify=False)
            usuario=User.objects.get(id=int(decoded['user_id']))
            cuenta=Cuenta.objects.get(usuario=usuario)
            if cuenta.tipo=='1':
                try:
                    idDenuncia=int(request.POST.get('id'))
                    estado=request.POST.get('estado')
                    denuncia=Denuncia.objects.get(id=idDenuncia)
                    denuncia.estado=estado
                    denuncia.full_clean()
                    denuncia.save()            
                    mensaje=send_email(denuncia.cuenta.usuario.email, "Su denuncia ha cambiado de estado, revise su cuenta para saber mas al respecto.")
                except:
                    mensaje="Puede ser que no se haya encontrado el id o el estado en el POST, tambien es posible que no exista ese id de denuncia o que el estado enviado no sea valido."
            else:
                mensaje="Debe ser investigador para cambiar estados"
            #mensaje="Debe estar logeado como investigador."
    return HttpResponse(json.dumps(mensaje))
