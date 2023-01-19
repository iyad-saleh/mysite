from faker import Faker
from tree.models import *
from django.db.models import Q
import random
from django.contrib.auth.models import User

# from .models import  Node, Profile

# fake = Faker('ar_SA')#ar_PS

'''
fake.first_name()
fake.first_name_female()
fake.first_name_male()
fake.last_name()
fake.date(pattern="%Y-%m-%d", end_datetime=None)


fake.street_address()
fake.city()
fake.address()
fake.msisdn() # # '0414831596096'
fake.credit_card_number(card_type=None)# '30189443830208'
'''
def GenerateUsers(count=5):
    for i in range(count):
        fake = Faker()
        username =''
        while not username:
            username =fake.first_name()+'_'+fake.last_name()+'_'+str(fake.msisdn()[:2])
            try:
                test  = User.objects.filter(username=username).first()
                if not test:
                    break
            except Exception as e:
                username =''
        print('username: ',username)    
        user = User.objects.create(username=username,email=fake.email(),password='ABC123456789')
        fake = Faker(random.choice(['ar_SA','ar_PS']))
        user.first_name =fake.first_name()
        user.last_name =fake.last_name()
        user.set_password('1234')
        user.save()
        profile = Profile.objects.create(user=user ,father= fake.first_name(),mather= fake.first_name_female(),
            nationalNumber   =fake.credit_card_number(card_type=None) ,entry= fake.state(),town= fake.street_address(),
            date_Grants  = fake.date(pattern="%Y-%m-%d", end_datetime=None),
            inheritor = fake.name(),birth_date  = fake.date(pattern="%Y-%m-%d", end_datetime=None),
            country_birth  = fake.country(),city_birth = fake.city(),tele=fake.msisdn(),
            town_birth  = fake.street_name(),country_address  = fake.country(),
            city_address  =  fake.city(),town_address  = fake.street_name(),
            country_Shipping =  fake.country(),city_Shipping   = fake.city(),
            town_Shipping  = fake.street_name(),street_Shipping  = fake.street_name(),
            )
        nodes =Node.objects.filter(Q(Rparent__isnull=False) | Q(Lparent__isnull=False)).distinct().exclude(id=1) #  he has  parent  
        nodes = nodes.filter(Q(right__isnull=True) | Q(left__isnull=True)).distinct()# free to have child
        newChild = Node.objects.create(user=user)
        parent = random.choice(nodes)
        if  not parent.left :
            try:
                # print(node,' befor  addLChild ',freechild)
                parent.addLChild(newChild)
                print(parent,' addLChild ',newChild )
                continue
            except Exception as e:
                print(e)
        if  not parent.right:
            try:
                # print(node,' befor  addRChild ',freechild)
                parent.addRChild(newChild)
                print(parent,' addRChild ',newChild)
            except Exception as e:
                print(e)












def genratenode():
    fake = Faker('ar_SA')#ar_PS
    for i in range(150):
        Node.objects.create(name=fake.first_name())
    fake = Faker('ar_PS')#ar_PS   
    for i in range(150):
        Node.objects.create(name=fake.first_name()) 

def clacNode():
    nodes = Node.objects.all()
    totalNodes = nodes.count()

    totalLike = 0
    for node in nodes :
        if node.bounce > 1 :
            Node.totalBounce  += node.bounce
            node.bounce = 0  
        if node.likeleft == node.likeright :
            totalLike += node.likeleft*2
            node.balance += node.likeleft * 2500*2
            node.likeleft =0
            node.likeright =0
            node.save()
        elif  node.likeleft > node.likeright   :
            totalLike += node.likeright*2
            node.likeleft = node.likeleft - node.likeright
            node.balance += node.likeright * 2500*2
            node.likeright = 0
            node.save()
            Node.remainLike += node.likeleft
        elif  node.likeleft < node.likeright   :
            totalLike += node.likeleft*2
            node.likeright = node.likeright - node.likeleft
            node.balance += node.likeleft * 2500*2
            node.likeleft = 0
            node.save()
            Node.remainLike += node.likeright
    print( 'totalNodes:',totalNodes,'  | pay for totalLike:',totalLike,"*2500 =",totalLike*2500,"$",
        '|  overLike:',Node.overLike,"| remainLike: ",Node.remainLike,
        ' |Node.totalBounce',Node.totalBounce , "*100= ",Node.totalBounce*1000)
    return totalLike   

        
def addnode():

    nodes =Node.objects.filter(Q(Rparent__isnull=False) | Q(Lparent__isnull=False)).distinct() #  he has  parent  except 1
    nodes = nodes.filter(Q(right__isnull=True) | Q(left__isnull=True)).distinct()# free to have child
    print('nodes',nodes ,len(nodes))
    for x,node  in enumerate(nodes):
        if  not node.left :
            freechild = random.choice(Node.objects.filter(Q(Rparent__isnull=True) & Q(Lparent__isnull=True)).exclude(id=node.id).exclude(id=1).distinct()) # free child 
            print("freechild left",x,freechild)
            try:
                # print(node,' befor  addLChild ',freechild)
                node.addLChild(freechild)
                print(node,' addLChild ',freechild )
            except Exception as e:
                print(e)
        if  not node.right:
            freechild = random.choice(Node.objects.filter(Q(Rparent__isnull=True) & Q(Lparent__isnull=True)).exclude(id=node.id).exclude(id=1).distinct()) # free child 
            print("freechild right",x,freechild)
            try:
                # print(node,' befor  addRChild ',freechild)
                node.addRChild(freechild)
                print(node,' addRChild ',freechild)
            except Exception as e:
                print(e)
            
if __name__ == '__main__':
    addnode()
'''
r.addLChild(s)


f = Node.objects.create(name='first')
r.addRChild(f)

t = Node.objects.create(name='third')
f.addRChild(t)

fth = Node.objects.create(name='fifth')
t.addRChild(fth)

ff = Node.objects.create(name='fourth')
f.addLChild(ff)

six = Node.objects.create(name='six')
ff.addLChild(six)












try:
    if r.Lparent:
        print(',,kk')
except RelatedObjectDoesNotExist:
    if r.Rparent:
        print('mmm')
else:
    print('kk ')


 '''