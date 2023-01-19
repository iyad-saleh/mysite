from django.shortcuts import render ,get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from collections import defaultdict
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileUpdateForm, UserRegisterForm,UserUpdateForm,ParentForm,Password_Form
from django.views.generic import (
    ListView,DetailView,
    CreateView, UpdateView, DeleteView )
   
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from .models import  Node, Profile, Activity  , NodesLog
from django.contrib.auth.views import PasswordChangeView
from tree.models import Activity
from datetime import datetime , timedelta
 


@login_required
def homeTree(request):
    # print(request.META['HTTP_USER_AGENT'])
    # Activity.objects.create(user=request.user ,title=str(request.META['HTTP_USER_AGENT'])[:100])
    # return render(request,'home.html')
    return render(request,'tree/home.html')

     

def searchChild(parent,results):
    child = []
    for son in parent.get_child():
        child.append(son)

        results.append(( son.id ,
         {
         'name':son.user.first_name +' '+son.user.profile.father+' '+son.user.last_name+'*'+son.user.username+'*' ,
         'title':str(son.likeright)+','+str(son.client)+','+str(son.likeleft)+','+str(son.bounce)+','+str(son.received),
         'active':son.user.is_active,
         'id':str(son.user.id)+','+str(son.chance) }, 
         parent.id  ))                                
    return  child  

parents = defaultdict(list)

chart_config = {
    'chart': { 'container': "#basic-example","animateOnInit":"true",
                'connectors': { 'type': "curve" },
                'node': { 'HTMLclass': 'nodeExample1', 'collapsable': 'true'},#
                'animation': {
                'nodeAnimation': "easeOutBounce",
                'nodeSpeed': 2000,
                'connectorsAnimation': "bounce",
                'connectorsSpeed': 2000
            }
                 }, 
               
    'nodeStructure':{}}


def buildtree(t=None, parent_eid=''):
    """
    Given a parents lookup structure, construct
    a data hierarchy.
    """

    # print("parents in tree : ",parents ,"\n\n")
    parent = parents.get(parent_eid, None)
    # print("parent in tree : ",parent ,"\n\n")
    if parent is None:
        return t
    for eid, name, mid  in parent:

        if name['title'].split(',')[-1] == 'True': 
            node = { 'text': name,'HTMLclass': 'light-green','stackChildren': 'true',}#'collapsed': 'false' ,
        else:
            node = { 'text': name,'HTMLclass': 'light-blue','stackChildren': 'true',}#'collapsed': 'false' ,
        if name['active'] ==False:
            node = { 'text': name,'HTMLclass': 'light-gray','stackChildren': 'true',}#'collapsed': 'false' ,
            
        if t is None:
            t = node
        else:
            childrens = t.setdefault('children', [])
            childrens.append(node)
        buildtree(node, eid)
    # print("buildtree:999 ",t)    
    return t


def searchparent(child,results):
    parent =None
 
    if Node.objects.filter(Q(id=child.id)&Q(Lparent__isnull=False)).distinct().first():
        parent = child.Lparent
    elif Node.objects.filter(Q(id=child.id)&Q(Rparent__isnull=False)).distinct().first():  
        parent = child.Rparent  
    if parent:
        results.append(( parent.id ,
                           {    'name':parent.user.first_name +' '+parent.user.profile.father+' '+parent.user.last_name +'*'+parent.user.username+'*',
                                'title':str(parent.likeright)+','+str(parent.client)+','+str(parent.likeleft)+','+str(parent.bounce)+','+str(parent.received),
                                'active':parent.user.is_active,
                                'id':str(parent.user.id)+','+str(parent.chance) }, 
                            "" )) 
    return parent                       
 


@login_required 
def nodeChild(request):
    if request.is_ajax():
 
        root = request.GET.get('root', '')
        q    = request.GET.get('child', '')
        # print(root,q)
        if int(q)  < int(root):
            q=root

        search_q = Node.objects.filter(user__id = q).first()
         
        # print('search_q',search_q)
        results = []
        if search_q :
            parent = searchparent(search_q,results)
            results.append(( search_q.id ,
                           {    'name':search_q.user.first_name +' '+search_q.user.profile.father +' '+search_q.user.last_name +'*'+search_q.user.username+'*',
                                'title':str(search_q.likeright)+','+str(search_q.client)+','+str(search_q.likeleft)+','+str(search_q.bounce)+','+str(search_q.received),
                                'active':search_q.user.is_active, 
                                'id':str(search_q.user.id)+','+str(search_q.chance) }, 
                           parent.id  if parent else "" ))#this is the root now 
            if search_q.get_child():# return  list of right and left if any 
                i =1 
                child  = searchChild(search_q,results)
                # print("search_q.get_child()",child)
                while child and (i > 0):      
                    i -= 1
                    gr_gr = []
                    for gr_child in child:
                        if gr_child.get_child():# return  list of right and left if any

                            gr_gr += searchChild(gr_child,results)
                            # print("gr_gr.get_child()",gr_gr)
                        else:
                            continue 
                    child = list(gr_gr)           

            
        # print('results:',results,"\n\n")     
        global parents
        parents =defaultdict(list)
        for p in results:
            parents[p[2]].append(p)                
        
        # print('parents after append:',parents,"\n\n")
        data = buildtree()
        global chart_config
        chart_config['nodeStructure']=data
        # print("chart_config['nodeStructure']",chart_config['nodeStructure'],"\n\n")
        # print('chart_config:\n',chart_config) 
        data =  json.dumps(chart_config)
        # data = json.dumps(results)
        dda = json.loads(data)
        
        # print('dda\n',dda)
    else:
        data = 'fail'
    mimetype = 'application/json'
    # print( data)
    return HttpResponse(data, mimetype)

@login_required 
def addNewNode(request):
    N_form = ParentForm()
    if request.method == 'POST':
        P_form = ProfileUpdateForm(request.POST)
        u_form = UserRegisterForm(request.POST)
        if P_form.is_valid() and u_form.is_valid()  :
            # print(u_form)
            # searchparent = request.POST.get('parent')
            user_id = request.POST.get('user_id')
            # print(user_id)
            myParent = Node.objects.filter(user__id=user_id).filter(Q(right__isnull=True)|Q(left__isnull=True)).first()
            # print(myParent)
            if not myParent:
               messages.add_message(request, messages.ERROR, 'اسم الصديق غير صالح ')
               return render(request, 'tree/register.html', {'u_form': u_form,'P_form': P_form,'N_form':N_form})
                
            u_form = u_form.save()
            # print(P_form)
            P_form = P_form.save(commit=False)
            P_form.user = u_form
            P_form.save()
            newnode = Node.objects.create(user=u_form,byuser=request.user)
            if not myParent.right:
                myParent.addRChild(newnode)
            elif  not myParent.left: 
                myParent.addLChild(newnode) 
            myParent.save()      
            # N_form.user = u_form
            # N_form.save()
            # N_form.parent = myParent
            # N_form.save()
            Activity.objects.create(user=u_form ,title="ادارة الشركة تشكر انضمامكم الينا نتمنى ان تقضو تجربة ممتعة ")
            messages.add_message(request, messages.SUCCESS, 'تم اضافة الوكالة بنجاح ')
            return redirect('homeblog')
    else:
        P_form = ProfileUpdateForm()
        u_form = UserRegisterForm()
        N_form = ParentForm()
    return render(request, 'tree/register.html', {'u_form': u_form,'P_form': P_form,'N_form':N_form,'temp_txt':'وكالة جديدة '})

@login_required 
def updateNode(request,id):
    obj = get_object_or_404(User, pk=id) 
    if request.method == 'POST':
        if  request.user.is_staff:
            # print('obj',obj)
            P_form = ProfileUpdateForm(request.POST, instance=obj.profile)
            u_form = UserUpdateForm(request.POST,instance=obj)
            if P_form.is_valid() and u_form.is_valid():
                # u_form= u_form.save(commit=False)
                # u_form.user = obj
                user = u_form.save()
                # print(P_form)
                # P_form = P_form.save(commit=False)
                # P_form.user= user
                P_form.save()
                # print(P_form)
                messages.add_message(request, messages.SUCCESS, 'تم تحديث الحساب بنجاح ')
                return redirect('homeblog')
    else:
        u_form = UserUpdateForm(instance=obj)
        P_form = ProfileUpdateForm(instance=obj.profile)
    if  request.user.is_staff:    
        return render(request, 'tree/register.html', {'u_form': u_form,'P_form': P_form}) 
    else:    

        return render(request, 'tree/showProfile.html', {'u_form': u_form,'P_form': P_form})   

# class UserListView(LoginRequiredMixin, ListView): 

#     model = User
#     template_name = 'users/users.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'users'
#     # ordering = ['-date_Transported']
#     paginate_by = 5

@login_required
def UserListView(request):
    users= User.objects.all().order_by('id').exclude(id=1)
    notReceived = Node.objects.filter(received=False).count()
    total = len(users)
    paginator = Paginator(users, 10)  # 10 users in each page
    page = request.GET.get('page')
    users = paginator.get_page(page)
    is_paginated= True if total >10 else False
    context = {
    'notReceived':notReceived,
    'is_paginated': is_paginated,
    'users':users,
    'total':total
    }
    return render(request, 'users/users.html', context) 


@login_required
def Nonereceived(request):
    users= User.objects.filter(node__received= False).order_by('id').exclude(id=1)
    notReceived = Node.objects.filter(received=False).count()
    total = len(users)
    paginator = Paginator(users, 20)  # 10 users in each page
    page = request.GET.get('page')
    users = paginator.get_page(page)
    is_paginated= True if total >20 else False
    context = {
    'notReceived':notReceived,
    'is_paginated': is_paginated,
    'users':users,
    'total':total
    }
    return render(request, 'users/users.html', context) 





@login_required 
def addChance(request,id):
    user = get_object_or_404(User, pk=id) 
    if  request.user.is_superuser:
        node = user.node_set.first()
        if node.  chance  < 8:
            node.chance +=1
            node.save()

    return redirect(request.META['HTTP_REFERER']) 


@login_required 
def userActiveconfirm(request,id):
    user = get_object_or_404(User, pk=id) 
    return render(request, 'users/userActive_confirm.html', {'user':user})



def userActive(request,id):
    obj = get_object_or_404(User, pk=id) 
    if request.method == 'POST':
        if  request.user.is_superuser:
            # print(obj)
            state = obj.is_active
            if state == True:
                obj.is_active = False

                messages.add_message(request, messages.SUCCESS, 'تم ايقاف الحساب بنجاح ')
            else  :
                obj.is_active = True
                messages.add_message(request, messages.SUCCESS, 'تم تفعيل الحساب بنجاح ')  
            obj.save()     
    return redirect('UserListView') 




@login_required 
def  searchUser(request): 
    q= request.GET.get('q')
    if  q:
        users = User.objects.filter(
            Q(first_name__istartswith=q)|
            Q(last_name__istartswith=q) |
            Q(username__istartswith=q)
                 ).distinct()
        context={
                'users':users,
                }
    else:
        messages.add_message(request, messages.ERROR, "الرجاء ادخال كلمة للبحث ")    
        context={
        }
    return render(request, 'users/users.html', context) 


@login_required 
def deleteUserconfirm(request,id):
    user = get_object_or_404(User, pk=id) 
    return render(request, 'users/user_confirm_delete.html', {'user':user})


@login_required 
def deleteUser(request,id):
    obj = get_object_or_404(User, pk=id) 
    if request.method == 'POST':
        if  request.user.is_superuser:
            # print(obj)
            obj.delete()
            messages.add_message(request, messages.SUCCESS, 'تم حذف الحساب بنجاح ')
    return redirect('UserListView')        


class PasswordResetByUser(PasswordChangeView):
  template_name = 'users/reset_by_user.html'
  form_class = Password_Form
  success_url = '/'    


@login_required
def confirmPasswordforUser(request,id):
    if  request.user.is_staff:
        obj = get_object_or_404(User, pk=id) 
        return render(request, 'users/reset_for_user.html', {'obj':obj})


@login_required
def confirmreceivedforUser(request,id):
    if request.user.groups.filter(name__in=['seller']) or request.user.is_staff :
        obj = get_object_or_404(User, pk=id) 
        return render(request, 'users/received_for_user.html', {'obj':obj})

@login_required
def receivedforUser(request,id):
    if request.user.groups.filter(name__in=['seller']) or request.user.is_staff:
        obj = get_object_or_404(User, pk=id) 
        if request.method == 'POST':
            node = obj.node_set.first()
            node.received = True
            node.receiveduser = request.user
            node.receiveddate= datetime.now()
            node.save()
            rootnode = Node.objects.filter(user_id =1).first()
            root = rootnode.user
            Activity.objects.create(user=obj ,title=f"لقد استلمت مشترياتك من {request.user.first_name} {request.user.last_name} شكرا لكم ")
            Activity.objects.create(user=request.user ,title=f"تم تسليم المشتريات الى {obj.first_name} {obj.last_name}")
            Activity.objects.create(user=root ,title=f"تم تسليم المشتريات من قبل {request.user.first_name} {request.user.last_name} الى  {obj.first_name} {obj.last_name}")
            messages.add_message(request, messages.SUCCESS, f'تم تسجيل عملية البيع  بنجاح ')
        return redirect('UserListView')    


@login_required
def PasswordResetforUser(request,id):
    if  request.user.is_staff:
        obj = get_object_or_404(User, pk=id) 
        if request.method == 'POST':
            obj.set_password('123456')
            obj.save()
            Activity.objects.create(user=obj ,title="تم اعادة ضبط كلمة السر لديك ")
            messages.add_message(request, messages.SUCCESS, f'تم اعادة ضبط كلمة السر {obj.username} بنجاح ')
        return redirect('homeblog')                     

@login_required
def confirmPasswordforNode(request,id):
    if  request.user.is_staff:
        obj = get_object_or_404(User, pk=id)

        return render(request, 'users/reset_node_user.html', {'obj':obj})


@login_required
def PasswordResetforNode(request,id):
    if  request.user.is_staff:
        obj = get_object_or_404(User, pk=id) 
        if request.method == 'POST':
            node= Node.objects.filter(user__id=id).first()
            node.password='123456'
            node.save()
            Activity.objects.create(user=obj ,title="تم اعادة ضبط كلمة السر الخزنة ")
            messages.add_message(request, messages.SUCCESS, f'تم اعادة ضبط كلمة السر الخزنة للمشترك {obj.username} بنجاح ')
        return redirect('homeblog')  



@login_required
def Activitylist(request):
    user= request.user
    date_N_days_ago = datetime.now() - timedelta(days=7)
    oldactivities  = Activity.objects.filter(user=user).filter(created__lt = date_N_days_ago)
    for oldact in oldactivities:
        oldact.delete()
    # print(date_N_days_ago,oldactivities)
    activities = Activity.objects.filter(user=user).order_by('read').order_by('-created')


    total = len(activities)
    paginator = Paginator(activities, 10)  # 10 activities in each page
    page = request.GET.get('page')
    activities = paginator.get_page(page)

    is_paginated= True if total >10 else False
    context = {
    'is_paginated': is_paginated,
    'activities':activities,
    'total':total
    }

    return render(request, 'users/Activity.html', context) 


#  this new 




@login_required
def AddEmployee(request,id):
    if request.user.is_superuser :
        obj = get_object_or_404(User, pk=id) 
        return render(request, 'users/AddEmployee.html', {'obj':obj})


@login_required
def Employee(request,id):
    if   request.user.is_staff:
        obj = get_object_or_404(User, pk=id) 
        if request.method == 'POST':
            employeeJob = request.POST.get('employeeJob')
            seller = Group.objects.filter(name='seller').first()

            if  employeeJob == 'seller' :
                obj.groups.add(seller)
                try:
                    obj.is_staff =False
                except Exception as e:
                    pass
                
            elif  employeeJob == 'is_staff' :
                obj.is_staff =True
                try:
                    obj.groups.clear()
                except Exception as e:
                    pass
            
            else:
                try:
                    obj.is_staff =False
                    obj.groups.clear()
                except Exception as e:
                    pass
            obj.save()        


        return redirect('UserListView') 


@login_required
def displayEmployee(request):
    staff = User.objects.filter(is_staff=True).order_by('id')
    lastChange = NodesLog.objects.latest('created').created
    try:
        beforeChange = NodesLog.objects.all().order_by('id')[::-1][1].created# last week
       
    except Exception as e:
        beforeChange= datetime.now()
    # print('lastChange',lastChange)
    # print('beforeChange',beforeChange)
    if not lastChange:
        
        lastChange = datetime.now()
    # r.by.filter(created__gte=lastChange).count()
    
    users =[] 

    for  x,user in  enumerate(staff):

        record = {
        'id'           :   user.id,
        'username'     :   user.username,
        'first_name'   :   user.first_name,
        'father'      :   user.profile.father,
        'last_name'  :   user.last_name,
        'total'     :    user.by.all().count(),
        'new'        :  user.by.filter(created__gte=lastChange).count(),
        'last'        :  user.by.filter(Q(created__gte= beforeChange) & Q(created__lt=  lastChange)).count(),
        }
        users.append(record)

    return render(request, 'users/staffEmployee.html', {'users':users})



@login_required
def displayseller(request):
    # seller = Group.objects.filter(name='seller').first()
    seller = User.objects.filter(Q(groups__name='seller')|Q(is_staff=True)).order_by('id')
    lastChange = NodesLog.objects.latest('id').created
    try:
        beforeChange = NodesLog.objects.all().order_by('id')[::-1][1].created# befor lastChange
    except Exception as e:
        beforeChange= datetime.now()
    print('lastChange',lastChange)
    print('beforeChange',beforeChange)
    if not lastChange:
        
        lastChange = datetime.now()
    # r.by.filter(created__gte=lastChange).count()
    
    users =[] 

    for  x,user in  enumerate(seller):
        # print('user.receivedby.receiveddate',user.receivedby.node_set.receiveddate)
        record = {
        'id'           :   user.id,
        'username'     :   user.username,
        'first_name'   :   user.first_name,
        'father'      :   user.profile.father,
        'last_name'  :   user.last_name,
        'total'     :    user.receivedby.all().count(),
        'new'        :  user.receivedby.filter(receiveddate__gte =lastChange).count(),
        'last'        :  user.receivedby.filter(Q(receiveddate__gte = beforeChange) & Q(receiveddate__lt=  lastChange)).count(),
        }
        users.append(record)

    return render(request, 'users/sellerEmployee.html', {'users':users})
