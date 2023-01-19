"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from django.urls import path,include
from tree.views import (PasswordResetByUser, homeTree,nodeChild,
    addNewNode, updateNode, confirmPasswordforNode, PasswordResetforNode,
    UserListView, searchUser,deleteUser,PasswordResetforUser,confirmPasswordforUser,
    deleteUserconfirm, userActive,userActiveconfirm ,Activitylist ,confirmreceivedforUser,
    receivedforUser ,Nonereceived ,AddEmployee, Employee  ,displayEmployee,displayseller,addChance)
from blog.views import home as homeblog
from blog.views import (CarouselCreateView,CarouselUpdateView,
    CarouselDeleteView ,FeaturettsCreateView,FeaturettsUpdateView,
    FeaturettsDeleteView,MarketingCreateView,MarketingUpdateView,
MarketingDeleteView,TickerCreateView, TickerUpdateView, TickerDeleteView)
from django.conf import settings
from django.conf.urls.static import static
from blog.forms import   UserloginForm
from tree.accountViews import( searchAccountsLog, AccountsLoglistView,
 changNodePass, clacAllNode,NodesLogList,lookupbalance,
  resetsystem,prepClacAllNode,systemconfirm ,
  Nodebalanc,balancelogin,transaction ,transactionRoot ,requesttransactionRoot)
from tree.autoviews import autocompleteFriend,autocompleteBalanceToFriend, autoActivity, readActivity
from tree.backup   import  export_as_csv, export_as_xls, GenerateUsers


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeblog,name='homeblog'),
    path('Node/', homeTree,name='homeTree'),
    path('nodeChild/', nodeChild,name='nodeChild'),
    path('addNewNode/', addNewNode,name='addNewNode'),
    path('updateNode/<int:id>/', updateNode,name='updateNode'),
    path('deleteUser/<int:id>/', deleteUser,name='deleteUser'),
    path('deleteUserconfirm/<int:id>/', deleteUserconfirm,name='deleteUserconfirm'),
    path('userActive/<int:id>/', userActive,name='userActive'),
    path('userActiveconfirm/<int:id>/', userActiveconfirm,name='userActiveconfirm'),
     path('PasswordResetByUser/', PasswordResetByUser.as_view()  , name='PasswordResetByUser'),
     path('confirmPasswordforUser/<int:id>/', confirmPasswordforUser   , name='confirmPasswordforUser'),
     path('PasswordResetforUser/<int:id>/', PasswordResetforUser   , name='PasswordResetforUser'),
    

    path('confirmPasswordforNode/<int:id>/', confirmPasswordforNode   , name='confirmPasswordforNode'),
     path('PasswordResetforNode/<int:id>/', PasswordResetforNode   , name='PasswordResetforNode'),
    
     path('confirmreceivedforUser/<int:id>/', confirmreceivedforUser   , name='confirmreceivedforUser'),
     path('receivedforUser/<int:id>/', receivedforUser   , name='receivedforUser'),
   

    path('ajax_calls/Freind/', autocompleteFriend, name='autocompleteFriend'),
    path('ajax_calls/ToFreind/', autocompleteBalanceToFriend, name='autocompleteBalanceToFriend'),
    path('ajax_calls/Activity/', autoActivity, name='autoActivity'),
    path('Activitylist/', Activitylist, name='Activitylist'),
    path('readActivity/', readActivity, name='readActivity'),
 

    path('Nodebalanc/', Nodebalanc,name='Nodebalanc'),
    path('balancelogin/', balancelogin,name='balancelogin'),
    path('transaction/', transaction,name='transaction'),
    path('transactionRoot/', transactionRoot,name='transactionRoot'),
    path('RtransactionRoot/<int:id>/<int:amount>/', requesttransactionRoot,name='requesttransactionRoot'),
    
    path('changNodePass/', changNodePass,name='changNodePass'),
    path('AccountsLoglistView/', AccountsLoglistView,name='AccountsLoglistView'),
    path('searchAccountsLog/', searchAccountsLog,name='searchAccountsLog'),
    
    path('resetsystem/', resetsystem,name='resetsystem'),
    path('systemconfirm/', systemconfirm,name='systemconfirm'),
    

    path('UserListView/', UserListView,name='UserListView'),
    path('searchUser/', searchUser,name='searchUser'),
    path('Nonereceived/', Nonereceived,name='Nonereceived'),
    
    path('prepClacAllNode/', prepClacAllNode,name='prepClacAllNode'),
    path('clacAllNode/', clacAllNode,name='clacAllNode'),
    path('NodesLogList/', NodesLogList,name='NodesLogList'),
    path('lookupbalance/<int:id>/', lookupbalance,name='lookupbalance'),



    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                         authentication_form= UserloginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    path('blog/Carousel/new/', CarouselCreateView.as_view(),name='CarouselCreateView'),
    path('blog/Carousel/<int:pk>/Update', CarouselUpdateView.as_view(),name='CarouselUpdateView'),
    path('blog/Carousel/<int:pk>/Delete', CarouselDeleteView.as_view(),name='CarouselDeleteView'),

    path('blog/Featuretts/new/', FeaturettsCreateView.as_view(),name='FeaturettsCreateView'),
    path('blog/Featuretts/<int:pk>/Update', FeaturettsUpdateView.as_view(),name='FeaturettsUpdateView'),
    path('blog/Featuretts/<int:pk>/Delete', FeaturettsDeleteView.as_view(),name='FeaturettsDeleteView'),
    
    path('blog/Marketing/new/', MarketingCreateView.as_view(),name='MarketingCreateView'),
    path('blog/Marketing/<int:pk>/Update', MarketingUpdateView.as_view(),name='MarketingUpdateView'),
    path('blog/Marketing/<int:pk>/Delete', MarketingDeleteView.as_view(),name='MarketingDeleteView'),


    path('blog/Ticker/new/', TickerCreateView.as_view(),name='TickerCreateView'),
    path('blog/Ticker/<int:pk>/Update', TickerUpdateView.as_view(),name='TickerUpdateView'),
    path('blog/Ticker/<int:pk>/Delete', TickerDeleteView.as_view(),name='TickerDeleteView'),
    

    path('exportCsv/', export_as_csv,name='export_as_csv'),
    path('exportXls/', export_as_xls,name='export_as_xls'),
    path('GenerateUsers/<int:cnt>/', GenerateUsers,name='GenerateUsers'),
    

    path('AddEmployee/<int:id>/', AddEmployee,name='AddEmployee'),
    path('Employee/<int:id>/', Employee,name='Employee'),
    path('displayEmployee/', displayEmployee,name='displayEmployee'),
    path('displayseller/', displayseller,name='displayseller'),
    path('addChance/<int:id>/', addChance,name='addChance'),









]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
