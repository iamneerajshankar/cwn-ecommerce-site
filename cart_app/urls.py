from django.urls import path
from cart_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from cart_app.forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('plus-to-cart/', views.plus_to_cart, name='plus-to-cart'),
    path('minus-from-cart/', views.minus_from_cart, name='minus-from-cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='cart_app/change-password.html'
     , form_class=MyPasswordChangeForm, success_url='/change-password-done/'), name='change-password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='cart_app/change-password-done.html'), name='change-password-done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='cart_app/password-reset.html'), name='reset-password'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='cart_app/password-reset-confirm.html', form_class=MySetPasswordForm),
         name='password_reset_confirm'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='cart_app/password-reset-done.html'), name='password_reset_done'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='cart_app/password-reset-complete.html'), name='password_reset_complete'),



    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='cart_app/login.html', authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    path('checkout/', views.checkout, name='checkout'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
