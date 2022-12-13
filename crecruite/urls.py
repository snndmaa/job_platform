"""crecruite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('account.urls')),
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('paidpost', views.paid_post, name='paidpost'),
    path('freepost', views.free_post, name='freepost'),
    path('post/<int:post_id>', views.postDetail, name='postDetail'),
    path('postComment/<int:post_id>', views.postComment, name='postComment'),
    path('addCompany', views.add_company, name='addcompany'),
    path('manageCompanies', views.manageCompanies, name='managecompanies'),
    path('manageInvoice', views.manageInvoice, name='manageinvoice'),
    path('invoice/<int:inv_id>', views.invoiceItem, name='invoiceItem'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('userinfo', views.personalInfo, name='userinfo'),
    path('edituser', views.editPersonalInfo, name='edituser'),
    path('buycredit', views.buyCredit, name='buycredit'),
    path('creditinvoice/<int:amount>', views.creditInvoice, name='creditinvoice'),
    path('paystatus/<int:amount>', views.payStatus, name='paystatus'),
    path('success', views.paySuccess, name='paysuccess'),

    #BLOCKS
    path('blockfilt/<str:field>', views.blockFilt, name='blockfilt'),
    path('featured', views.featuredBlock, name='featuredblock'),
    path('today', views.todayBlock, name='todayblock'),
    path('yesterday', views.yesterdayBlock, name='yesterdayblock'),
    path('field/<int:field>', views.fieldBlock, name='fieldblock'),
    path('role/<int:role>', views.roleBlock, name='roleblock'),
    path('industry/<int:industry>', views.industryBlock, name='industryblock'),
    path('subject/<int:subject>', views.subjectBlock, name='subjectblock'),
    path('state/<int:state>', views.stateBlock, name='stateblock'),
    path('region/<int:region>', views.regionBlock, name='regionblock'),
    path('close', views.closeBlock, name='closeblock'),
    path('changepassword', views.changePassword, name='changepassword'),
    path('test', views.test, name='test')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)