from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^empleados/', views.EmpleadoListView.as_view())
]
