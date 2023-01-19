from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in ,user_logged_out ,user_login_failed 
import datetime


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.PositiveIntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Activity(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100,blank=True, null=True)
    read  = models.BooleanField(default=False)          
    created     = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username} {self.title}'

@receiver(user_logged_in, sender=User)
def catch_login(sender, user, request, **kwargs):
    Activity.objects.create(user=user ,title="تم تسجيل الدخول من"+str(request.META['HTTP_USER_AGENT'])[:45])
       

class Standard(models.Model):
    nodePrice     = models.IntegerField( default=25000) # 25 000 
    likePrice     = models.IntegerField( default=2500) # 2500
    BouncePrice   = models.IntegerField( default=1000) # 2500
        

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    father      = models.CharField(max_length=100,blank=True, null=True, default='-')
    mather      = models.CharField(max_length=100,blank=True, null=True, default='-')
    nationalNumber  = models.CharField(max_length=20,blank=True, null=True, default='-')
    entry        = models.CharField(max_length=100,blank=True, null=True, default='-')
    town         = models.CharField(max_length=100,blank=True, null=True, default='-')
    date_Grants  = models.DateField(blank=True, null=True )
    tele         =  models.CharField(max_length=100,blank=True, null=True, default='-')
    inheritor     = models.CharField(max_length=100,blank=True, null=True, default='-')
    birth_date    = models.DateField(blank=True, null=True )
    country_birth = models.CharField(max_length=100,blank=True, null=True, default='-') 
    city_birth    = models.CharField(max_length=100,blank=True, null=True, default='-') 
    town_birth    = models.CharField(max_length=100,blank=True, null=True, default='-') 
    country_address = models.CharField(max_length=100,blank=True, null=True, default='-') 
    city_address  = models.CharField(max_length=100,blank=True, null=True, default='-') 
    town_address  = models.CharField(max_length=100,blank=True, null=True, default='-') 
    country_Shipping  = models.CharField(max_length=100,blank=True, null=True, default='-') 
    city_Shipping  = models.CharField(max_length=100,blank=True, null=True, default='-') 
    town_Shipping  = models.CharField(max_length=100,blank=True, null=True, default='-') 
    street_Shipping  = models.CharField(max_length=100,blank=True, null=True, default='-') 

    def __str__(self):
        return f'{self.user.username}'

class AccountsLog(models.Model):
    user_from   = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, related_name='fromUser',null=True)
    user_to     = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,related_name='toUser', null=True)
    created     = models.DateTimeField(auto_now_add=True)
    amount      =models.IntegerField( default=0) # 25 000
    def __str__(self):
        return f'{self.user_from.first_name} {self.user_from.last_name} to {self.user_to.first_name} {self.user_to.last_name}   '

class NodesLog(models.Model):
    totalNodes      = models.IntegerField( blank=True, null=True,default=0)#   number of  new node 
    totalLike       = models.IntegerField( blank=True, null=True,default=0)
    overLike        = models.IntegerField( blank=True, null=True,default=0)
    totalBounce     = models.IntegerField( blank=True, null=True,default=0)
    remainLikeleft  = models.IntegerField( blank=True, null=True,default=0)
    remainLikeright  = models.IntegerField( blank=True, null=True,default=0)
    nodePrice       = models.IntegerField( default=55000) # 25 000 
    likePrice       = models.IntegerField( default=2500) # 2500
    BouncePrice     = models.IntegerField( default=1000) # 1000
    created         = models.DateTimeField(auto_now_add=True)
    totalBlance     =models.IntegerField( default=0) # 25 000


class Node(models.Model):
    
    byuser         = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='by', null=True, blank=True)
    user           = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    right          = models.OneToOneField('self', on_delete=models.SET_NULL, related_name='Rparent', null=True, blank=True)
    left           = models.OneToOneField('self', on_delete=models.SET_NULL, related_name='Lparent', null=True, blank=True)
    client         = models.IntegerField( blank=True, null=True,default=0)
    likeleft       = IntegerRangeField(   default=0, min_value=0, max_value=32)
    likeright      = IntegerRangeField(   default=0, min_value=0, max_value=32)
    bounce         = IntegerRangeField( default=0, min_value=0, max_value=2)
    balance        = models.IntegerField( default=0)
    password       = models.CharField(max_length=50,default='123456')
    created        = models.DateTimeField(auto_now_add=True)
    updated        =  models.DateTimeField(auto_now=True) 
    overLikeleft   = models.IntegerField( default=0)
    overLikeright  = models.IntegerField( default=0)
    chance         = IntegerRangeField( default=8, min_value=0, max_value=8)
    received      =models.BooleanField(default=False)
    receiveduser  = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receivedby', null=True, blank=True)
    receiveddate  = models.DateTimeField( null=True, blank=True)
    def __str__(self):
        name = '' 
        try:
            name= self.user.first_name
        except Exception as e:
            name = 'no  name'
        return name

    def get_child(self):
        myChild = []
        if self.right :
            myChild.append(self.right)
        if self.left:
            myChild.append(self.left)
        return myChild


    @staticmethod        
    def addParentLike(node,*args, **kwargs):

        freeChildLeft = Node.objects.filter(Lparent__isnull=False)
        freeChildRight = Node.objects.filter(Rparent__isnull=False)
        parent = None
        
        if node in freeChildRight:
            try:
                if node.Rparent and not parent:
                    parent = node.Rparent  #  grand
                    if parent.user.is_active:
                        if parent.likeright < 32 :# if it's active and not more 32 like  
                            parent.likeright +=1
                            Activity.objects.create(user=parent.user ,title="تم اضافة وكالة جديدة من اليمين :"+node.user.first_name)
                        else:
                            parent.overLikeright += 1       
                    parent.client += 1
                    parent.save()
            except Exception as e:
                print('Exception :',node.user," Rparent : ",e)
        elif node in freeChildLeft and not parent:
            try:
                if node.Lparent:
                    parent = node.Lparent  #  grand
                    if parent.user.is_active:
                        if parent.likeleft < 32 :# if it's active and not more 32 like 
                            parent.likeleft +=1
                            # print('parent.user',parent.user)
                            Activity.objects.create(user=parent.user ,title="تم اضافة وكالة جديدة من اليسار :"+node.user.first_name)
                            # print("new likeleft parent ",parent)
                        
                        else:
                            parent.overLikeleft += 1       
                    parent.client += 1
                    parent.save()
            except Exception as e:
                print('Exception :',node.user," Lparent :",e)
        if parent:
            Node.addParentLike(parent,*args, **kwargs)       
    
    def addRChild(self,node,*args, **kwargs):
        # print('addRChild',self.user)
        parentexists=False
        try:
            if node.Rparent :
                parentexists=True 
                raise Exception('Rparent for  child exists',node)  
        except Exception as e:
            pass
        try:
            if node.Lparent:
                parentexists=True 
                raise Exception('Lparent for  child exists',node)  
        except Exception as e:
            pass
        
        if not self.right  and not parentexists :
            if not self.id == node.id :

                self.right = node
                self.likeright +=1
                self.bounce +=1
                self.client +=1
                # print('addRChild',self.user)
                  
                Activity.objects.create(user= self.user ,title="تم اضافة وكالة جديدة من اليمين")
                 
                self.save()
                self.addParentLike(self,*args, **kwargs)
        else:    
            raise Exception('right child existsss' ) 


    def addLChild(self,node,*args, **kwargs):
        parentexists=False
        try:
            if node.Rparent :
               parentexists=True 
               # print('parent for  child exists') 
               raise Exception('parent for  child exists',node)  
        except Exception as e:
            pass
        try:
            if node.Lparent:
               parentexists=True  
               # print('parent for  child exists')  
               raise Exception('parent for  child exists',node)  
        except Exception as e:
            pass
        if not self.left and not parentexists:
            if not self.id == node.id :
                self.left = node
                self.likeleft +=1
                self.bounce +=1
                self.client +=1
                # print('addLChild',self.user)
                # user = User.objects.get(id=self.user ) 
                Activity.objects.create(user=self.user ,title="تم اضافة وكالة جديدة من اليسار")
                 
                
                self.save()
                self.addParentLike(self,*args, **kwargs)
        else:    
            raise Exception('left child exists' )                

