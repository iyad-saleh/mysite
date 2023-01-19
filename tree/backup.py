from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect, HttpResponse
import xlwt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import  Node, Profile
from django.contrib.auth.decorators import login_required
from faker import Faker
from tree.models import *
from django.db.models import Q
import random
 


@login_required
def export_as_csv(  request):
    import csv
    users = User.objects.all().order_by('id')
    filename = 'AllUsers'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        filename)
    writer = csv.writer(response)
    writer.writerow(['id','username','email','first_name','last_name','balance',
            'left','right','client','likeleft','likeright','father','mather','nationalNumber',
            'entry','town','date_Grants','tele','inheritor','birth_date','country_birth','city_birth',
            'town_birth','country_address','city_address','town_address','country_Shipping',
            'city_Shipping','town_Shipping','street_Shipping'])
                        
    for obj in users:
        node         =obj.node_set.first()

        id          = obj.id
        username    =obj.username  
        email       =obj.email     
        first_name  =obj.first_name
        last_name   =obj.last_name
        balance       =node.balance
        left         =node.left
        right        =node.right
        client       =node.client
        likeleft     =node.likeleft
        likeright    =node.likeright
        father       =obj.profile.father
        mather       =obj.profile.mather
        nationalNumber =obj.profile.nationalNumber
        entry        =obj.profile.entry
        town         =obj.profile.town
        date_Grants  =obj.profile.date_Grants
        tele         =obj.profile.tele
        inheritor    =obj.profile.inheritor
        birth_date   =obj.profile.birth_date
        country_birth =obj.profile.country_birth
        city_birth   =obj.profile.city_birth
        town_birth   =obj.profile.town_birth
        country_address =obj.profile.country_address
        city_address =obj.profile.city_address
        town_address =obj.profile.town_address
        country_Shipping =obj.profile.country_Shipping
        city_Shipping =obj.profile.city_Shipping
        town_Shipping =obj.profile.town_Shipping
        street_Shipping =obj.profile.street_Shipping

        writer.writerow([id,username,email,first_name,last_name,balance,left,right,client,
                            likeleft,likeright,father,mather,nationalNumber,entry,town,
                        date_Grants,tele,inheritor,birth_date,country_birth,city_birth,
                        town_birth,country_address,city_address,town_address,country_Shipping,
                        city_Shipping,town_Shipping,street_Shipping ])


           
    return response



@login_required
def export_as_xls( request):
    users = User.objects.all().order_by('id')
    filename = 'AllUsers'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename={}.xls'.format(
        filename)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(filename )
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id','username','email','first_name','last_name','balance',
            'left','right','client','likeleft','likeright','father','mather','nationalNumber',
            'entry','town','date_Grants','tele','inheritor','birth_date','country_birth','city_birth',
            'town_birth','country_address','city_address','town_address','country_Shipping',
            'city_Shipping','town_Shipping','street_Shipping']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    for obj in users:
        node         =obj.node_set.first()

        id           = obj.id
        username     =obj.username  
        email        =obj.email     
        first_name   =obj.first_name
        last_name     =obj.last_name
        balance       =node.balance
        left          = node.left.user.first_name+' '+node.left.user.last_name  if node.left else  ""
        right        =node.right.user.first_name+' '+node.right.user.last_name if node.right else  ""
        client       =node.client
        likeleft     =node.likeleft
        likeright    =node.likeright
        father       =obj.profile.father
        mather       =obj.profile.mather
        nationalNumber =obj.profile.nationalNumber
        entry        =obj.profile.entry
        town         =obj.profile.town
        date_Grants  =obj.profile.date_Grants
        tele         =obj.profile.tele
        inheritor    =obj.profile.inheritor
        birth_date     =obj.profile.birth_date
        country_birth  =obj.profile.country_birth
        city_birth      =obj.profile.city_birth
        town_birth      =obj.profile.town_birth
        country_address =obj.profile.country_address
        city_address    =obj.profile.city_address
        town_address    =obj.profile.town_address
        country_Shipping =obj.profile.country_Shipping
        city_Shipping    =obj.profile.city_Shipping
        town_Shipping    =obj.profile.town_Shipping
        street_Shipping  =obj.profile.street_Shipping


        rows = [id,username,email,first_name,last_name,balance,left,right,client,
                            likeleft,likeright,father,mather,nationalNumber,entry,town,
                        date_Grants,tele,inheritor,birth_date,country_birth,city_birth,
                        town_birth,country_address,city_address,town_address,country_Shipping,
                        city_Shipping,town_Shipping,street_Shipping ]
        # for row in rows:
        row_num += 1
        for col_num in range(len(rows)):
            ws.write(row_num, col_num, rows[col_num], font_style)

    wb.save(response)
    return response



@login_required
def GenerateUsers(request,cnt):

    for i in range(cnt):
        fake = Faker(random.choice(['ar_SA','ar_PS','']))
        username =''
        while not username:
            username =fake.first_name()+'_'+fake.last_name()+'_'+str(fake.msisdn()[:2])
            try:
                test  = User.objects.filter(username__exact=username).first()
                if not test:
                    break
            except Exception as e:
                username =''
        # print('username: ',username)    
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
        newChild = Node.objects.create(user=user,byuser=request.user)
        parent = random.choice(nodes)
        if  not parent.left :
            try:
                # print(node,' befor  addLChild ',freechild)
                parent.addLChild(newChild)
                # print(parent,' addLChild ',newChild )
                continue
            except Exception as e:
                print(e)
        if  not parent.right:
            try:
                # print(node,' befor  addRChild ',freechild)
                parent.addRChild(newChild)
                # print(parent,' addRChild ',newChild)
            except Exception as e:
                print(e)
    return redirect(request.META['HTTP_REFERER'])            



