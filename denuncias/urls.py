# -*- coding: utf-8 -*-
"""denuncias URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from denunciasCiudadanas.views import DenunciaActualViewSet, DepMunViewSet, DepartamentoViewSet, MunicipioViewSet, FiltroViewSet, CuentaViewSet, DenunciaViewSet, check_login, login_user, registrar_usuario, verificar_usuario, crear_denuncia, cambiar_estado
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()
router.register(prefix='cuentas', viewset=CuentaViewSet, base_name='micuenta')
router.register(prefix='denuncias', viewset=DenunciaViewSet, base_name='propietario')
router.register(prefix='filtro', viewset=FiltroViewSet, base_name='filtroInvestigador')
router.register(prefix='estadisticas', viewset=MunicipioViewSet, base_name='municipios')
router.register(prefix='denuncia', viewset=DenunciaActualViewSet, base_name='denunciaactual')
router.register(prefix='departamentos', viewset=DepartamentoViewSet)
router.register(prefix='municipios', viewset=DepMunViewSet)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^login/', login_user),
    url(r'^check_login/', check_login),
    url(r'^registrarse/', registrar_usuario),
    url(r'^verificar_usuario/', verificar_usuario),
    url(r'^crear_denuncia/', crear_denuncia),
    url(r'^cambiar_estado/', cambiar_estado),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
