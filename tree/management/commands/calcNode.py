
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from tree.models import  Node, Profile, NodesLog, AccountsLog ,Activity



class Command(BaseCommand):
    help = 'Calc All Node '
    
    def handle(self, *args, **options):
        nodes = Node.objects.all().exclude(user__id=1)
        root = Node.objects.get(user__id=1)
        lastChange = NodesLog.objects.latest('created').created
        if not lastChange:
            from datetime import datetime
            lastChange = datetime.now()
        totalNewNodes = nodes.filter(created__gte=lastChange).count() #whether the value is greater than or equal to
         
        # print('totalNewNodes',totalNewNodes)

        newlog = NodesLog.objects.create(totalNodes=totalNewNodes,
                                        likePrice= 2000,BouncePrice=1000,
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


 