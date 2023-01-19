
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from .models import  Node, Profile ,Activity
from django.db.models import Q
from django.contrib.auth.decorators import login_required



@login_required
def readActivity(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        if q :
            q = q.split(',')
            # print('readActivity  q',q)
            # pass
            for act in q :
                # print(act)
                active = Activity.objects.filter(id=int(act)).first()
                if active:
                    active.read=True
                    active.save()
        data = json.dumps([{'label' :"Done"}])
    else:
        data = json.dumps([{'label' :"Done"}])
        data = 'fail'
    mimetype = 'application/json'
    # print( data)
    return HttpResponse(data, mimetype)        


@login_required
def autoActivity(request):

    if request.is_ajax():
        user= request.user
        if user.is_authenticated:
            activities = Activity.objects.filter(user=user,read=False).count() 
        
            results = []
            
            
            results.append({'label' :str(activities)})
            data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    # print( data)
    return HttpResponse(data, mimetype)




def autocompleteFriend(request):
    if request.is_ajax():
        q = request.GET.get("term", '')
        # print("q",q)
        search_qs = Node.objects.filter(Q(user__first_name__istartswith=q)
                                    | Q(user__username__istartswith=q)
        ).filter(Q(right__isnull=True)|Q(left__isnull=True)).distinct() 
        

        # search_qs = User.objects.filter( Q(first_name__istartswith=q)| Q(username__istartswith=q) ).distinct()
        
           
                
        results = []
        # print( search_qs)
        for r in search_qs:
             
            label = str( r.user.id)+'- '+r.user.first_name+' '+r.user.profile.father +' '+r.user.last_name+' //  ('+r.user.date_joined.strftime('%Y/%m/%d')+")"
            
            results.append({'label':label,'value':str( r.user.id)})
         
        # print(results)    
        data = json.dumps(results)
        # print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)    



def autocompleteBalanceToFriend(request):
    if request.is_ajax():
        q = request.GET.get("term", '')
        # print("q",q)
        search_qs = Node.objects.filter(Q(user__first_name__istartswith=q)
                                    | Q(user__username__istartswith=q) ).distinct() 
       

        # search_qs = User.objects.filter( Q(first_name__istartswith=q)| Q(username__istartswith=q) ).distinct()
        results = []
        # print( search_qs)
        for r in search_qs:
             
            label = str( r.user.id)+'- '+r.user.first_name+' '+r.user.profile.father +' '+r.user.last_name+' //  ('+r.user.date_joined.strftime('%Y/%m/%d')+")"
            
            results.append({'label':label,'value':str( r.user.id)})
         
        # print(results)    
        data = json.dumps(results)
        # print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)    


















