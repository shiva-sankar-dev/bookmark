from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.
def loginpage(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            request.session["userID"]=user.id
            return redirect("homepage")
        
    
    return render(request,"loginpage.html")

def logoutpage(request):
    logout(request)
    return redirect("homepage")

def aboutus(request):

    return render(request,"aboutus.html")

def booklist(request):
    searched=""
    user=request.user
    searched_books = []  
    if user.is_authenticated:
        wishlist_items_keys = Wishlist.objects.filter(user_id=user).values_list("openlibrary_key", flat=True)
    else:
        wishlist_items_keys = []
        
    if request.method == "GET":
        searched = request.GET.get("searched-data")
        

        if searched:
            print(searched, "Fetching books for the genre with ebooks only...")
            response = requests.get(f"https://openlibrary.org/search.json?q={searched}")
            if response.status_code == 200:
                data = response.json()
                for book in data.get("docs", [])[:20]: 
                    if book.get("ebook_count_i", 0) > 0:
                        openlibrary_key = book.get("key")
                        searched_books.append({
                            "title": book.get("title"),
                            "author": ", ".join(book.get("author_name", [])),
                            "cover_id": book.get("cover_i"),
                            "openlibrary_key": openlibrary_key,
                            "openlibrary_id": openlibrary_key.split("/")[-1],
                            "in_wishlist": openlibrary_key in wishlist_items_keys, 
                        })

 
    context = {
        "searched_books": searched_books,
        "searched": searched,
    }
    return render(request, "booklist.html", context)


# def booklist(request):
#     searched = ""
#     book_list = []  # To hold book data from the API
#     if request.method == "POST":
#         searched = request.POST.get("searched-data")
        
#         if searched:
#             # Call Open Library API to fetch books
#             response = requests.get(f"https://openlibrary.org/search.json?q={searched}")
#             if response.status_code == 200:
#                 data = response.json()
#                 # Extract book details
#                 for book in data.get("docs", [])[:50]:  # Limit to 10 books
#                     book_list.append({
#                         "title": book.get("title"),
#                         "author": ", ".join(book.get("author_name", [])),
#                         "publish_year": book.get("first_publish_year"),
#                         "cover_id": book.get("cover_i"),
#                     })

#     context = {
#         "booklist": book_list,
#         "searched": searched,
#     }
#     return render(request, "booklist.html", context)



def filterlist(request, genre):
    user = request.user
    
    if user.is_authenticated:
        wishlist_items_keys = Wishlist.objects.filter(user_id=user).values_list("openlibrary_key", flat=True)
    else:
        wishlist_items_keys = []


    filtered_books = []  
    if genre:
        print(genre, "Fetching books for the genre with ebooks only...")
        response = requests.get(f"https://openlibrary.org/search.json?subject={genre}")
        if response.status_code == 200:
            data = response.json()
            for book in data.get("docs", [])[:20]: 
                if book.get("ebook_count_i", 0) > 0:
                    openlibrary_key = book.get("key")
                    filtered_books.append({
                        "title": book.get("title"),
                        "author": ", ".join(book.get("author_name", [])),
                        "cover_id": book.get("cover_i"),
                        "openlibrary_key": openlibrary_key,
                        "openlibrary_id": openlibrary_key.split("/")[-1],
                        "in_wishlist": openlibrary_key in wishlist_items_keys, 
                    })

    context = {
        "filtered_books": filtered_books,
        "wishlist_items_keys": wishlist_items_keys,
    }
    return render(request, "booklist.html", context)



# def filterlist(request, genre):
#     user = request.user
#     wishlist_items_keys = Wishlist.objects.filter(user_id=user).values_list("openlibrary_key", flat=True)

#     filtered_books = []  
#     if genre:
#         print(genre, "Fetching books for the genre with ebooks only...")
#         response = requests.get(f"https://openlibrary.org/search.json?subject={genre}")
#         if response.status_code == 200:
#             data = response.json()
#             for book in data.get("docs", [])[:20]: 
#                 if book.get("ebook_count_i", 0) > 0:
#                     availability = book.get("availability", {})
#                     read_url = availability.get('read_url', f"https://openlibrary.org/works/{book.get('key')}/read")
#                     borrow_url = availability.get('borrow_url', "Not Available")
                    
#                     # Check if the book is available to download
#                     download_url = availability.get('download_url', None)
#                     if not download_url and read_url != "Not Available":
#                         download_url = f"https://openlibrary.org/works/{book.get('key')}/download"

#                     print(f"Read URL: {read_url}")
#                     print(f"Borrow URL: {borrow_url}")
#                     print(f"Download URL: {download_url if download_url else 'Not Available'}")        
#                     openlibrary_key = book.get("key")
#                     filtered_books.append({
#                         "title": book.get("title"),
#                         "author": ", ".join(book.get("author_name", [])),
#                         "cover_id": book.get("cover_i"),
#                         "openlibrary_key": openlibrary_key,
#                         "in_wishlist": openlibrary_key in wishlist_items_keys, 
#                     })

#     context = {
#         "filtered_books": filtered_books,
#         "wishlist_items_keys": wishlist_items_keys,
#     }
#     return render(request, "booklist.html", context)




def contactus(request):
    active="contact"
    if request.method == "POST":
        fullname=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("sending-message")
        data = {
                "access_key": "0fe05a4e-e52d-4253-ac6e-34e6034c1b7d", 
                "name": fullname,
                "email": email,
                "message user send": message,
            }
    
        response = requests.post("https://api.web3forms.com/submit", json=data)
        result = response.json()
    
            # Handle success or failure response from Web3Forms
        if result.get("success"):
            return JsonResponse({"success":True,"message":"Message sent successfully"})
            
        else:
            return JsonResponse({"success":False,"message":"Message not sent successfully"})
    return render(request,"contactus.html",{"active":active})

def remove_cart_item(request,id):
    remove=Cart.objects.get(id=id)
    remove.delete()
    return redirect("cart")

def registrationpage(request):
    if request.method=="POST":
        fullname=request.POST.get("fullname","no name")
        email=request.POST.get("email","no email")
        password=request.POST.get("password","no pass")

        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
        else:
            user=User.objects.create_user(username=email,email=email)
            user.set_password(password)
            user.first_name=fullname
            user.save()

            return redirect("loginpage")
            
    return render(request,"registrationpage.html")


def index(request):
    # Initialize genre mappings
    print("Fetching data for template")
    genres = {
        "bestsellers": "Bestsellers",
        "young_adults": "Young Adult",
        "award_winning": "Award-winning books",
        "first_edition": "First Edition",
    }

    # Fetch wishlist keys for the logged-in user
    wishlist_items_keys = []
    if request.user.is_authenticated:
        wishlist_items_keys = Wishlist.objects.filter(user_id=request.user).values_list("openlibrary_key", flat=True)
    else:
        wishlist_items_keys = []

    # Function to fetch books for each category
    categories = {
        "bestsellers": [],
        "young_adults": [],
        "award_winning": [],
        "first_edition": [],
    }

    # Custom URLs for specific categories
    urls = {
        "bestsellers": "https://openlibrary.org/search.json?q=bestsellers",
        "award_winning": "https://openlibrary.org/search.json?q=award+winning",
        "first_edition": "https://openlibrary.org/search.json?q=first+edition",
        "young_adults": "https://openlibrary.org/search.json?subject=Young%20Adult",
    }

    for category, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for book in data.get("docs", [])[:10]:  # Limit to 10 books
                if book.get("ebook_count_i", 0) > 0:  # Include only books with eBooks
                    openlibrary_key = book.get("key")
                    categories[category].append({
                        "title": book.get("title"),
                        "author": ", ".join(book.get("author_name", [])),
                        "cover_id": book.get("cover_i"),
                        "openlibrary_key": openlibrary_key,
                        "openlibrary_id": openlibrary_key.split("/")[-1],
                        "in_wishlist": openlibrary_key in wishlist_items_keys,
                    })

    # Pass data to template
    context = {
        "bestsellers": categories["bestsellers"],
        "young_adults": categories["young_adults"],
        "award_winning": categories["award_winning"],
        "first_edition": categories["first_edition"],
        "active": "home",
    }
    return render(request, "index.html", context)


@csrf_exempt
def wishlist(request):
    user = request.user
    remove_item = request.POST.get("openlibrary_key")
    print(remove_item,"WWWWWWWWWWWWWWWWWw")
    wishlist_items_keys = Wishlist.objects.filter(user_id=user).values_list("openlibrary_key", flat=True).order_by('-id')
    wishlist_items = []
    if wishlist_items_keys:
        for openlibrary_key in wishlist_items_keys:
            if not openlibrary_key:  # Skip if the key is None or empty
                continue
            response = requests.get(f"https://openlibrary.org{openlibrary_key}.json")
            if response.status_code == 200:
                data = response.json()
                if data:
                        # Extract author keys from the data
                    author_keys = [author.get("author", {}).get("key") for author in data.get("authors", []) if author.get("author")]
                    authors = []
                    
                    # Fetch names of authors using their keys
                    for author_key in author_keys:
                        author_response = requests.get(f"https://openlibrary.org{author_key}.json")
                        if author_response.status_code == 200:
                            author_data = author_response.json()
                            authors.append(author_data.get("name", "Unknown"))  # Fallback to 'Unknown' if no name
                  
                    wishlist_items.append({
                        "title": data.get("title"),
                        "author": ", ".join(authors),
                        "cover_id": data.get("covers", [None])[0],  # First cover ID if available
                        "openlibrary_key": data.get("key"),
                        "openlibrary_id": openlibrary_key.split("/")[-1],
                        "description": data.get("description", "No description available"),
                        "in_wishlist": openlibrary_key in wishlist_items_keys, 
                    })
    if remove_item:
        Wishlist.objects.filter(user_id=user,openlibrary_key=remove_item).delete()
        print("successfully removed from wishlist!!")
        return JsonResponse({"success":True,"openlibrary_key":remove_item})
    context = {
        "wishlist_items": wishlist_items,
    }
    return render(request, "wishlist.html", context)




@csrf_exempt
def wishlist_toggle(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        openlibrary_key = request.POST.get("openlibrary_key")
        title = request.POST.get("title")
        author = request.POST.get("author")
        cover_id = request.POST.get("cover_id")

        wishlist_item = Wishlist.objects.filter(user_id=user, openlibrary_key=openlibrary_key).first()
        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({"added": False, "openlibrary_key": openlibrary_key})
        else:
            Wishlist.objects.create(
                user_id=user,
                openlibrary_key=openlibrary_key,
                title=title,
                author=author,
                cover_id=cover_id
            )
            return JsonResponse({"added": True, "openlibrary_key": openlibrary_key})
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.db.models import Sum
@login_required(login_url="loginpage")
def cart(request):
    user= request.user
    items_in_cart = Cart.objects.filter(users=user)
    count = Cart.objects.filter(users=user).count()
    if 'add_cart' in request.POST:
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))  
        price = float(request.POST.get('price'))
        
        book = AddBooks.objects.get(id=book_id)


        total_price = price * quantity

        cart_item = Cart.objects.create(
            users=user,
            book=book,
            quantity=quantity,
            total_price=total_price
        )
        return redirect("cart")
    
    if "checkout_btn" in request.POST:
        get_cart_items=Cart.objects.all()
        get_book_quantity=AddBooks.objects.all()
        for item in get_cart_items:
            ids=item.book.id
            items=item.quantity
            total_no_items=item.book.quantity
            stock=total_no_items - items
            get_cart_items.delete()
            if stock > 0:
                item.book.quantity=stock
                item.book.save()
                
            else:
                item.book.quantity=0
                item.book.save()
        return redirect("cart")
        
    total_cart_price = items_in_cart.aggregate(Sum('total_price'))['total_price__sum'] or 0
    if total_cart_price > 80:
        shipping_fee=total_cart_price
    else:
        shipping_fee=total_cart_price+20
    
    context = {
        "items_in_cart": items_in_cart,
        "total_cart_price": total_cart_price,
        "shipping_fee": shipping_fee,
        "count": count,
    }
    return render(request, "cart.html", context)

        


def details(request, id):
    user = request.user
    if user.is_authenticated:
        wishlist_items_keys = Wishlist.objects.filter(user_id=user).values_list("openlibrary_key", flat=True)
    else:
        wishlist_items_keys = []

    selected_book = None  
    if id:
        print(f"Fetching details for book with ID: {id}")
        response = requests.get(f"https://openlibrary.org/works/{id}.json") 
        if response.status_code == 200:
            data = response.json()
            availability = data.get("availability", {})
            print(f"Availability data: {availability}")

            read_url = availability.get("read_url")
            borrow_url = availability.get("borrow_url")
            download_url = availability.get("download_url")
            if not read_url:
                read_url = f"https://openlibrary.org/works/{id}/read"
            if not download_url:
                download_url = None  # Set None if no valid URL is available
                
            print(f"Read URL: {read_url}")
            print(f"Download URL: {download_url if download_url else 'Not Available'}")

            openlibrary_key = id
            author_keys = [author.get("author", {}).get("key") for author in data.get("authors", []) if author.get("author")]
            authors = []
                    
            for author_key in author_keys:
                author_response = requests.get(f"https://openlibrary.org{author_key}.json")
                if author_response.status_code == 200:
                    author_data = author_response.json()
                    authors.append(author_data.get("name", "Unknown"))
            selected_book = {
                "title": data.get("title", "No title available"),
                "author": ", ".join(authors),
                "cover_id": data.get("covers", [None])[0],
                "openlibrary_key": openlibrary_key,
                "read_url": read_url if read_url else None,
                "download_url": download_url if download_url else None,
                "in_wishlist": openlibrary_key in wishlist_items_keys,
                "description": data.get("description", "No description available"),
                "subjects": data.get("subjects", []),
            }

    context = {
        "selected_book": selected_book,
    }

    return render(request, "details.html", context)

