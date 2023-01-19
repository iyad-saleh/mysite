from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# from .models import Profile,Post
from .models import Profile, Node, NodesLog, AccountsLog ,Activity

class NodesLog_Admin(ImportExportModelAdmin):
    list_display = ['totalNodes','totalLike','overLike',
'totalBounce','remainLikeleft','remainLikeright','nodePrice',
'likePrice','BouncePrice','created','totalBlance']    # list_filter = ('box_type', 'profit')

    # list_display_links = ('id',)

    class Meta:
        model = NodesLog
admin.site.register(NodesLog,NodesLog_Admin)

class Activity_Admin(ImportExportModelAdmin):
    # list_display = '__all__'
    # list_filter = ('box_type', 'profit')

    # list_display_links = ('id',)

    class Meta:
        model = Activity
admin.site.register(Activity,Activity_Admin)

# # Register your models here.
class Profile_Admin(ImportExportModelAdmin):
    # list_display = '__all__'
    # list_filter = ('box_type', 'profit')

    # list_display_links = ('id',)

    class Meta:
        model = Profile
admin.site.register(Profile,Profile_Admin)

class AccountsLog_Admin(ImportExportModelAdmin):
    # list_display = '__all__'
    # list_filter = ('box_type', 'profit')

    # list_display_links = ('id',)

    class Meta:
        model = AccountsLog
admin.site.register(AccountsLog,AccountsLog_Admin)



class Node_Admin(ImportExportModelAdmin):
    list_display = ('id','user','right','left','likeleft','likeright',
                'bounce','Rparent','Lparent','balance','client','overLikeleft','overLikeright',
                'byuser','received','receiveduser','receiveddate')
    
    list_per_page = 500
    list_filter = ('balance','user__is_active','likeleft','likeright','client' )

    # list_display_links = ('id',)

    class Meta:
        model = Node
admin.site.register(Node,Node_Admin)
# admin.site.register(Child)



# class Post_Admin(ImportExportModelAdmin):
#     # list_display = '__all__'
#     # list_filter = ('box_type', 'profit')

#     # list_display_links = ('id',)

#     class Meta:
#         model = Post
# admin.site.register(Post,Post_Admin)