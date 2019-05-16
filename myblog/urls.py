from django.urls import path
from .views import stub_view, list_view, detail_view
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', include('myblog.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
]
