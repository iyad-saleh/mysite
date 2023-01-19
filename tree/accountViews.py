from django.shortcuts import render ,get_object_or_404, redirect
# from .models import Post
# Create your views here.
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from collections import defaultdict
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileUpdateForm, UserRegisterForm,UserUpdateForm,ParentForm ,NodeForm,ChooseForm,ChooseRootForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import  Node, Profile, NodesLog, AccountsLog ,Activity
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse ,reverse_lazy



'''
totalNodes
totalLike
overLike
totalBounce
remainLikeleft
remainLikeright
nodePrice
likePrice
created
totalBlance
BouncePrice
'''
@login_required 
def systemconfirm(request):
    if  request.user.is_superuser: 
        return render(request, 'tree/system_confirm_delete.html')


@login_required 
def resetsystem(request):
    if request.method == 'POST':
        if  request.user.is_superuser:
            users  =User.objects.all().exclude(id=1)
            nodes = Node.objects.all()

            # nodes = nodes.filter(user__id =1)
            logs  = NodesLog.objects.all().exclude(id=1)
            allactiv =  Activity.objects.all()
            for act in allactiv:
                act.delete()
            for log in logs:
                log.delete()
            for node in nodes:
                node.delete()    
            for user in users:
                user.delete()
            AccountsLogs =AccountsLog.objects.all()
            for ALogs in AccountsLogs:
                ALogs.delete()
                
            root = User.objects.filter(id=1).first()
            user1 = User.objects.create(username="eyad",password='ABC123456789')
            user1.set_password('1234')
            user1.save()
            user1.first_name="اياد"
            user1.last_name="صالح"
            Profile.objects.create(user=user1,father="علي")
            user1.save()
            user2 = User.objects.create(username="aymen",password='ABC123456789')
            user2.set_password('1234')
            user2.save()
            Profile.objects.create(user=user2,father="صبورة")
            user2.first_name="ايمن"
            user2.last_name="صبورة"
            user2.save()

            rootNode = Node.objects.create(user=root ,byuser=request.user ) 
            node2 = Node.objects.create(user=user2 ,byuser=request.user  )        
            node1 = Node.objects.create(user=user1  ,byuser=request.user )        
            rootNode.left=node2
            rootNode.right=node1
            rootNode.save()
            return  HttpResponseRedirect(reverse('homeblog'))  



@login_required 
def clacAllNode(request):
    nodes = Node.objects.all().exclude(user__id=1)
    root = Node.objects.get(user__id=1)
    lastChange = NodesLog.objects.latest('created').created
    if not lastChange:
        from datetime import datetime
        lastChange = datetime.now()
    totalNewNodes = nodes.filter(created__gte=lastChange).count() #whether the value is greater than or equal to
     
    # print('totalNewNodes',totalNewNodes)

    newlog = NodesLog.objects.create(totalNodes=totalNewNodes,
                                    likePrice= 2500,BouncePrice=1000,
                                    nodePrice=55000,totalBlance=0 )

    for node in nodes :
        if node.bounce > 0 :
            newlog.totalBounce  += node.bounce 
            node.balance        += newlog.BouncePrice * node.bounce
            for i in range(node.bounce): 
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = newlog.BouncePrice) 
                Activity.objects.create(user=node.user ,title="حصلت على هدية لانضمام وكالة جديدة لك ")
            newlog.totalBlance += newlog.BouncePrice * node.bounce
            node.bounce = 0  
        if  (node.likeleft == 0 and node.likeright > 0) or (node.likeleft >0 and node.likeright == 0) and node.chance > 0:
            if node.likeleft > 0 and  node.likeleft <= node.chance :
                newlog.totalLike += node.likeleft
                node.balance     += node.likeleft   * newlog.likePrice
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.likeleft *  newlog.likePrice))
                newlog.totalBlance += node.likeleft *  newlog.likePrice 
                node.chance      -= node.likeleft
                node.likeleft    =  0 
                node.save() 
            elif node.likeleft > 0 and  node.likeleft > node.chance :
                newlog.totalLike += node.chance
                node.balance     += node.chance   * newlog.likePrice
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.chance *  newlog.likePrice))
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = node.chance *  newlog.likePrice  )
                newlog.totalBlance += node.chance *  newlog.likePrice
                node.likeleft    -=  node.chance
                node.chance       =  0  
                node.save() 
            elif node.likeright > 0 and  node.likeright <= node.chance :
                newlog.totalLike += node.likeright
                node.balance     += node.likeright   * newlog.likePrice
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.likeright *  newlog.likePrice))
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = node.likeright *  newlog.likePrice  )
                newlog.totalBlance += node.likeright *  newlog.likePrice 
                node.chance      -= node.likeright
                node.likeright    =  0 
                node.save()  
            elif node.likeright > 0 and  node.likeright > node.chance :
                newlog.totalLike += node.chance
                node.balance     += node.chance   * newlog.likePrice
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.chance *  newlog.likePrice))
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = node.chance *  newlog.likePrice  )
                newlog.totalBlance += node.chance *  newlog.likePrice
                node.likeright    -=  node.chance    
                node.chance       =  0  
                node.save() 
        elif node.likeleft == node.likeright :
            newlog.totalLike   += node.likeleft*2
            node.balance       += node.likeleft * 2 * newlog.likePrice 
            if node.likeleft * 2 * newlog.likePrice > 0:
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.likeleft * 2 * newlog.likePrice)) 
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = node.likeleft * 2 * newlog.likePrice  )
            newlog.totalBlance += node.likeleft * 2 *  newlog.likePrice 
            node.likeleft      = 0
            node.likeright     = 0

        elif  node.likeleft > node.likeright   :
            newlog.totalLike      += node.likeright*2
            node.likeleft         = node.likeleft - node.likeright
            node.balance          += node.likeright * newlog.likePrice*2
            if node.likeright * newlog.likePrice*2 > 0:
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.likeright * newlog.likePrice*2))
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = node.likeright * 2 * newlog.likePrice  ) 
            newlog.totalBlance    += node.likeright * newlog.likePrice*2
            node.likeright        = 0
            newlog.remainLikeleft += node.likeleft

        elif  node.likeleft < node.likeright   :
            newlog.totalLike    += node.likeleft*2
            node.likeright      = node.likeright - node.likeleft
            node.balance        += node.likeleft * newlog.likePrice*2
            if node.likeleft * newlog.likePrice*2 > 0:
                Activity.objects.create(user=node.user ,title="تم الاضافة الى رصيدك مبلغ "+str(node.likeleft * newlog.likePrice*2))
                # AccountsLog.objects.create(user_from=root.user ,user_to=node.user,amount = node.likeleft * 2 * newlog.likePrice  )  
            newlog.totalBlance  += node.likeleft * newlog.likePrice*2
            node.likeleft        = 0
            newlog.remainLikeright += node.likeright

        newlog.overLike  +=   node.overLikeright  +  node.overLikeleft
        node.overLikeright = 0
        node.overLikeleft = 0
        node.save()
       
    root.balance += totalNewNodes*55000
    AccountsLog.objects.create(user_from=root.user ,user_to=root.user,amount =totalNewNodes*55000 )
    root.save()
    Activity.objects.create(user=root.user ,title="تم تصفية حساب شركة  :"+str(totalNewNodes*55000)) 
    newlog.save()

    return render(request,'accountNode/clacAllNode.html',{'log':newlog})

@login_required 
def prepClacAllNode(request):
    nodes = Node.objects.all().exclude(user__id=1)
    lastChange = NodesLog.objects.latest('created').created
    if not lastChange:
        from datetime import datetime
        lastChange = datetime.now()
    totalNewNodes = nodes.filter(created__gte=lastChange).count() #whether the value is greater than or equal to

    # print('totalNewNodes',totalNewNodes)
    import datetime
    newlog= {

    "messages":"هذه نظرة سريعة الى الحساب القادم ",
            'totalNodes':totalNewNodes,
            'id':"استعلام ",
            'totalBounce':0,
            'totalBlance':0,
            'totalLike':0,
            'remainLikeright':0,
            'remainLikeleft':0,
            'overLike':0,
            'nodePrice':55000,
            "likePrice":2500,
            'BouncePrice':1000,
            'created':lastChange
           } 

    for node in nodes :
        if node.bounce > 0 :
            newlog['totalBounce']  += node.bounce 
            newlog['totalBlance'] += newlog['BouncePrice']*node.bounce 
        if  (node.likeleft == 0 and node.likeright > 0) or (node.likeleft >0 and node.likeright == 0) and node.chance > 0:
            if node.likeleft > 0 and  node.likeleft <= node.chance :
                newlog['totalLike'] += node.likeleft
                newlog['totalBlance'] += node.likeleft *  newlog['likePrice'] 
            elif node.likeleft > 0 and  node.likeleft > node.chance :
                newlog['totalLike'] += node.chance
                newlog['totalBlance'] += node.chance *  newlog['likePrice']
            elif node.likeright > 0 and  node.likeright <= node.chance :
                newlog['totalLike'] += node.likeright
                newlog['totalBlance'] += node.likeright *  newlog['likePrice'] 
            elif node.likeright > 0 and  node.likeright > node.chance :
                newlog['totalLike'] += node.chance
                newlog['totalBlance'] += node.chance *  newlog['likePrice']

        elif node.likeleft == node.likeright :
            newlog['totalLike'] += node.likeleft*2
            newlog['totalBlance'] += node.likeleft * newlog['likePrice'] * 2
             

        elif  node.likeleft > node.likeright :
            newlog['totalLike'] += node.likeright*2
            newlog['totalBlance'] += node.likeright * newlog['likePrice']*2
             
            newlog['remainLikeleft'] += node.likeleft - node.likeright

        elif  node.likeleft < node.likeright :
            newlog['totalLike'] += node.likeleft*2
            newlog['totalBlance'] += node.likeleft * newlog['likePrice']*2
             
            newlog['remainLikeright'] += node.likeright - node.likeleft
 

        newlog['overLike']  +=   node.overLikeright  +  node.overLikeleft
    # Node.overLike    =  0 
     

    return render(request,'accountNode/clacAllNode.html',{'log':newlog})


@login_required 
def NodesLogList(request): 

    logs = NodesLog.objects.all().order_by('-id')
    nodes  =Node.objects.all().exclude(user__id=1)
    root  =Node.objects.get(user__id=1)
    total = 0
    for node in nodes:
        total += node.balance
    paginator = Paginator(logs, 20)  # 10 logs in each page
    page = request.GET.get('page')
    is_paginated= True if len(logs) > 20 else False
    logs = paginator.get_page(page)
    context = {
    'is_paginated': is_paginated,
    'logs':logs,
    'total':total,
    'root':root
    }

    
    return render(request,'accountNode/NodesLogs.html',context)

@login_required 
def transaction(request):
    if request.method == 'POST':
        Choose_Form = ChooseForm(  request.POST,instance=request.user)
        if Choose_Form.is_valid() :
            friend = Choose_Form.cleaned_data.get('user')
            user_id = Choose_Form.cleaned_data.get('user_id')
            if not user_id:
                messages.add_message(request, messages.ERROR, ' الرجاء ادخال اسم صديق بمساعدة الاكمال التلقائي !!!')
                return render(request, 'accountNode/transaction.html', {  'Choose_Form':Choose_Form})
            amount = Choose_Form.cleaned_data.get('amount')
            amount1 = Choose_Form.cleaned_data.get('amount1')
            if  amount != amount1:
                messages.add_message(request, messages.ERROR, ' المبلغين غير متطابقين يرجى مطابقة الرقم  !!!')
                return render(request, 'accountNode/transaction.html', {  'Choose_Form':Choose_Form})
            if  int(amount) < 0:
                messages.add_message(request, messages.ERROR, ' الرجاء ادخال رقم صحيح موجب !!!')
                return render(request, 'accountNode/transaction.html', {  'Choose_Form':Choose_Form})

            # print(friend,amount)
            requestNode = request.user.node_set.first()
            if requestNode.balance < int(amount) :
                messages.add_message(request, messages.ERROR, ' رصيدك غير كافي !!')
                return render(request, 'accountNode/transaction.html', {  'Choose_Form':Choose_Form})
            user = User.objects.filter(id  =user_id ).first()
            if not user:
                user = User.objects.filter(username =friend ).first()
            if request.user ==  user:
                messages.add_message(request, messages.ERROR, 'عفوا  لايمكنك التحويل لنفسك!!!  ')
                return render(request, 'accountNode/transaction.html', {  'Choose_Form':Choose_Form})
            node = user.node_set.first()
            node.balance +=  int(amount)
            requestNode.balance -= int(amount)
            requestNode.save()
            node.save()
            Activity.objects.create(user=user ,title=f"تم تحويل رصيد من  {request.user.first_name} {request.user.last_name} ")
            Activity.objects.create(user=request.user ,title=f"تم تحويل رصيد الى {user.first_name} {user.last_name} ")
            AccountsLog.objects.create(user_from=request.user ,user_to=user,amount=int(amount))
            messages.add_message(request, messages.SUCCESS, f' تم تحويل  {amount} من رصيدك  بنجاح  الى  {user.first_name} {user.last_name}')
            return redirect('Nodebalanc')
        else:
            messages.add_message(request, messages.ERROR, ' الرجاء ادخال قيم صحيحة  ')    


          
    data = {'amount': request.user.node_set.first().balance}
    Choose_Form = ChooseForm(initial=data    )    
    return render(request, 'accountNode/transaction.html', {  'Choose_Form':Choose_Form})


@login_required 
def Nodebalanc(request ):
    user = request.user  

    context={
    'user':user,
    }

    return render(request,'accountNode/Nodeinfo.html',context)

@login_required 
def balancelogin(request ):

    if request.method == 'POST':
        password_form = NodeForm(request.POST, instance=request.user)
        if password_form.is_valid() :
            password = password_form.cleaned_data.get('password')
            if request.user.node_set.first().password == password:
                messages.add_message(request, messages.SUCCESS, 'كلمة السر صحيحة شكرا لك ')
                

                return render(request, 'accountNode/Nodeinfo.html')       
            else:   
                messages.add_message(request, messages.ERROR, 'كلمة السر غير صحيحة')
             
            # redirect('homeblog')
    else :
        password_form = NodeForm(  instance=request.user)

    return render(request, 'accountNode/balancelogin.html', {'password_form': password_form})          


@login_required
def lookupbalance(request,id):
    obj = get_object_or_404(User, pk=id) 

    node= Node.objects.filter(user__id=id).first()

    new_balance = node.balance
    new_balance        +=  node.bounce  *1000

    if  (node.likeleft == 0 and node.likeright > 0) or (node.likeleft >0 and node.likeright == 0) and node.chance > 0:
        if node.likeleft > 0 and  node.likeleft <= node.chance :
            new_balance     += node.likeleft   * 2500
        elif node.likeleft > 0 and  node.likeleft > node.chance :
            new_balance     += node.chance   * 2500
        elif node.likeright > 0 and  node.likeright <= node.chance :
            new_balance     += node.likeright   * 2500
        elif node.likeright > 0 and  node.likeright > node.chance :
            new_balance     += node.chance   * 2500
    elif node.likeleft == node.likeright :
        new_balance       += node.likeleft * 2 * 2500 
    elif  node.likeleft > node.likeright   :
        new_balance          += node.likeright * 2500*2
    elif  node.likeleft < node.likeright   :
        new_balance        += node.likeleft * 2500*2
    if  new_balance ==   node.balance:
        new_balance ='نعتذر منك لايوجد اي اضافات !! '  
    return render(request, 'accountNode/lookupbalance.html', {'new_balance': new_balance})      


@login_required 
def changNodePass(request):
    if request.method == 'POST':
        password_form = NodeForm(request.POST, instance=request.user)
        if password_form.is_valid() :
            password = password_form.cleaned_data.get('password')
            # print('password',password)
            node = request.user.node_set.first()
            node.password = password
            node.save()
            messages.add_message(request, messages.SUCCESS, ' تم تغيير كلمة السر للخزنة شكرا لك ')
            return redirect('Nodebalanc')

             
    password_form = NodeForm(  instance=request.user)
    return render(request, 'accountNode/changNodePass.html', {  'password_form':password_form})


@login_required 
def AccountsLoglistView(request):
    logs = AccountsLog.objects.filter(Q(user_to=request.user)|Q(user_from=request.user)).order_by('-created')    
    is_paginated= True if len(logs) >20 else False
    paginator = Paginator(logs, 20)
    page = request.GET.get('page')
    logs = paginator.get_page(page)

    context = {
    'is_paginated': is_paginated,
     'logs': logs}
    return render(request, 'accountNode/AccountsLog.html',context)   


@login_required 
def  searchAccountsLog(request): 
    q= request.GET.get('q')
    if  q:
        logs = AccountsLog.objects.filter(
            Q(user_to__first_name__istartswith=q)|
            Q(user_to__last_name__istartswith=q) |
            Q(user_to__username__istartswith=q)|
            Q(user_from__first_name__istartswith=q)|
            Q(user_from__last_name__istartswith=q) |
            Q(user_from__username__istartswith=q)
                 ).distinct().order_by('-created') 
        is_paginated= True if len(logs) >20 else False
        paginator = Paginator(logs, 20)
        page = request.GET.get('page')
        logs = paginator.get_page(page)

        context = {
        'is_paginated': is_paginated,
         'logs': logs}
    else:
        messages.add_message(request, messages.ERROR, "الرجاء ادخال كلمة للبحث ")    
        context={
        }
    return render(request, 'accountNode/AccountsLog.html',context)


@login_required
def  requesttransactionRoot(request, id,amount):
    obj = get_object_or_404(User, pk=id) 

    node= Node.objects.filter(user__id=id).first()
    root= Node.objects.filter(user__id=1).first()
    if  request.user.is_staff:
        userFull  = str(obj.id)+'-'+obj.first_name+' ' +obj.last_name 
        data = {'amount': amount,'amount1':amount,'user':userFull,'user_id':id}
        Choose_Form = ChooseRootForm(initial=data    )    
        return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form,'amount':node.balance})
    return redirect('homeblog') 
    


@login_required
def  transactionRoot(request):
    if  request.user.is_staff:
        if request.method == 'POST':
            root= Node.objects.filter(user__id=1).first()
            Choose_Form = ChooseRootForm( request.POST,instance=root.user)
            # print(Choose_Form)
            if Choose_Form.is_valid() :
                friend = Choose_Form.cleaned_data.get('user')
                user_id = Choose_Form.cleaned_data.get('user_id')
          
                amount = Choose_Form.cleaned_data.get('amount')
                amount1 = Choose_Form.cleaned_data.get('amount1')
                if  amount != amount1:
                    messages.add_message(request, messages.ERROR, ' المبلغين غير متطابقين يرجى مطابقة الرقم  !!!')
                    return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form})
                if  int(amount) < 0 or int(amount) ==0:
                    messages.add_message(request, messages.ERROR, ' الرجاء ادخال رقم صحيح موجب !!!')
                    return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form})

                # print('friend,amount',friend,amount)

                

                if root.balance < int(amount) :
                    messages.add_message(request, messages.ERROR, ' رصيدك غير كافي !!')
                    return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form})
                user = User.objects.filter(id  =user_id ).first()
                if not user:
                    user = User.objects.filter(username =friend ).first()
                if request.user ==  user:
                    messages.add_message(request, messages.ERROR, 'عفوا  لايمكنك التحويل لنفسك!!!  ')
                    return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form})
                node = user.node_set.first()
                # print('node',node.balance)

                if  int(amount)> node.balance :
                    messages.add_message(request, messages.ERROR, 'لايمكن تحويل  مبلغ اضافي  !!!')
                    return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form})

                node.balance  -= int(amount)
                root.balance  -= int(amount)
                root.save()
                node.save()
                Activity.objects.create(user=user ,title=f"تم تسديد مبلغ {amount}  من  {root.user.first_name} {root.user.last_name} ")
                Activity.objects.create(user=request.user ,title=f"تم تسديد مبلغ   {amount} الى {user.first_name} {user.last_name}  من رصيد  الشركة ")
                Activity.objects.create(user=root.user ,title=f"تم تسديد مبلغ   {amount} الى {user.first_name} {user.last_name}  من  رصيد  الشركة  بواسطة "+request.user.first_name)
                AccountsLog.objects.create(user_from=root.user ,user_to=user,amount=int(amount))
                messages.add_message(request, messages.SUCCESS, f' تم تسديد   {amount} من رصيد الشركة بنجاح  الى  {user.first_name} {user.last_name}')
                return redirect('UserListView')
            


        userFull  = str(obj.id)+'-'+obj.first_name+' ' +obj.last_name 
        data = {'amount': amount,'amount1':amount,'user':userFull,'user_id':id}
        Choose_Form = ChooseRootForm(initial=data    )    
        return render(request, 'accountNode/Roottransaction.html', {  'Choose_Form':Choose_Form})


