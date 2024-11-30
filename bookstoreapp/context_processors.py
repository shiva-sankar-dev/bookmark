from bookstoreapp.models import User
from bookstoreapp.models import Cart

def showuser(request):    
    showname =""
    cartcount=""
    if request.user.is_authenticated:
        
        showname=request.user.first_name  
        user=request.user  
        cartcount = Cart.objects.filter(users=user).count()

    context={
        "usernme":showname,
        "cartcount":cartcount,
    }
    return context

