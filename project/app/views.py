from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.models import User
# from .models make_password
from django.contrib import messages
from .models import addemploye 
from .models import*
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password # 🟢 Yeh library zaroori hai


# from .cron import rotate_daily_movies 



# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from .models import moviesdata, UserProfile
# 👇 AAPKI API KEY AUTOMATIC CONNECTED HAI 👇
# TMDB_API_KEY = 'afd7a2bb5077d6fb8a1f6dfc4184382b' 






# Create your views here.

def firstpage(req):
    return render(req,'firstpage.html')



def superadmin(req):
    if req.method == 'POST':

        edit_id = req.POST.get('edit_id')

        if edit_id:
            try:
                emp=addemploye.objects.get(id=edit_id)
                emp.name=req.POST.get('name')
                emp.email=req.POST.get('email')
                emp.roll=req.POST.get('roll')
                emp.password=req.POST.get('password')
                emp.save()
                messages.success(req,f'{emp.name} changes successfully update!')
             
            except Exception as e:
                messages.error(req,f"changes is some error! try agin:{e}")
            return redirect('superadmin')



        # # Matching HTML name attributes
        name = req.POST.get('name')
        email = req.POST.get('email')
        roll = req.POST.get('roll')
        password = req.POST.get('password')



        if addemploye.objects.filter(email=email).exists():
           messages.error(req,"email allredy exist")
           return redirect('superadmin')

        try:
            new_emp = addemploye(
                    name= name, 
                    email=email,
                    roll=roll,
                    password=password
                    )
            new_emp.save()
            messages.success(req,"Employee add successfully")
            return redirect('superadmin')

        except Exception as e:
            messages.error(req, f"Database error: {e}")




    # Fetching all records for the table
    all_employees = addemploye.objects.all()
    return render(req, 'superadmin.html', {'employees': all_employees})

def delete_employee(req, emp_id):
    if req.method == 'POST': 
        try:
            emp=addemploye.objects.get(id=emp_id) 
            emp_name =emp.name
            emp.delete()

            messages.success(req, f"{emp_name} ka access successfully revoke kar diya gaya hai.")
        
     
     
        except addemploye.DoesNotExist: 
         messages.success(req, "Employee does not exist")
    return redirect('superadmin')  







def adlogin(req): 
    if req.method == 'POST':

        email = req.POST.get('email')
        password = req.POST.get('password')
    

    
        if addemploye.objects.filter(email=email , password=password).exists():          
           messages.success(req, "succesfully login")
           return redirect('aadmin')

        else :
            messages.error(req, "Invalid Email or Password!")

            return redirect('adlogin')   

            
    return render(req,"adlogin.html")








def aadmin(req):
    if req.method == 'POST':

        category_id=req.POST.get('category_id')
        movie_name = req.POST.get('movie_name')
        movie_genre = req.POST.get('movie_genre')

      
        if not category_id or not movie_name:    
            messages.error(req,"movies/id already exiests")
            return redirect('aadmin')
            

        try:
            new_movie=aadmovies(

                category_id=category_id,
                movie_name=  movie_name,
                movie_genre=movie_genre,

            )
            new_movie.save()
            messages.success(req,"movie add succesfully") 
            return redirect('aadmin') 


        except Exception as e:
            messages.error(req, f"Database error: {e}") 
            return redirect('aadmin') 
        

     
    return render(req,'aadmin.html')   


def movies_delete(req , movie_id):
    if req.method == 'POST':

        try:
            del_movie=aadmovies.objects.get(id=movie_id)
            movie_name=del_movie.movie_name
            del_movie.delete()

            messages.success(req,f"{movie_name} movie succesfully delete")

        except aadmovies.DoesNotExist:
            messages.error(req,"this movie does not exies")  
    return redirect('aadmin')      


            

            
            
















def user(req):
    if req.method == 'POST':

        email= req.POST.get('email')
        password=req.POST.get('password')

      




        if User.objects.filter(email=email).exists():
            messages.error(req, "यह ईमेल पहले से रजिस्टर्ड है।")
            return render(req, 'user.html')

        try:
            # 2. डेटाबेस में नया यूजर क्रिएट करें
            # Django में डिफ़ॉल्ट रूप से username जरूरी होता है, इसलिए हम email को ही username बना रहे हैं
            new_user = User.objects.create_user(username=email, email=email, password=password)
            new_user.save() 

            messages.success(req, "अकाउंट सफलतापूर्वक बन गया है!")
            return redirect('nav')
            
        except Exception as e:
            messages.error(req, f"कुछ गड़बड़ हुई: {e}")

    return render(req, 'user.html')












def base(req):
    return render(req,'base.html')



def login(req):
    if req.method == 'POST':

        email = req.POST.get('email')
        password = req.POST.get('password')

        try:
            # Custom User model se email dhoondhein
            user = User.objects.get(email=email)
            if check_password(password, user.password):  
                    # Custom Session initialization
                    req.session['user_id'] = user.id
                    req.session['email'] = user.email 
                    print(f"✅ Login Success for User ID: {user.id}")
                    messages.success(req, f"Welcome back!")
                    return redirect('nav')
            else:
                messages.error(req, "Invalid password. Please try again.")
                return redirect('login')

        except User.DoesNotExist:
            messages.error(req, "This Email Address is not registered.")
            return redirect('login')


    return render(req,'login.html')


import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

def reset(request):
    if request.method == "POST":
        # HTML फॉर्म से डेटा गेट करना
        email = request.data.get('email') or request.POST.get('email')
        otp_entered = request.data.get('otp') or request.POST.get('otp')
        new_password = request.data.get('new_password') or request.POST.get('new_password')
        confirm_password = request.data.get('confirm_password') or request.POST.get('confirm_password')

        # 1. चेक करें कि यूजर इस ईमेल से रजिस्टर्ड है या नहीं
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "This email address is not registered.")
            return render(request, 'forgot_password.html')

        # 2. सेशन से जनरेटेड OTP और ईमेल गेट करना
        session_otp = request.session.get('reset_otp')
        session_email = request.session.get('reset_email')

        # 3. OTP वेरिफिकेशन चेक
        if not session_otp or str(session_otp) != str(otp_entered) or session_email != email:
            messages.error(request, "Invalid or expired OTP. Please check your email.")
            return render(request, 'forgot_password.html')

        # 4. पासवर्ड मैचिंग चेक
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'forgot_password.html')

        # 5. पासवर्ड लेंथ चेक (बेसिक सिक्योरिटी)
        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'forgot_password.html')

        # 6. नया पासवर्ड सेव करना
        user.password = make_password(new_password)
        user.save()

        # काम पूरा होने के बाद सेशन से OTP डिलीट करना
        del request.session['reset_otp']
        del request.session['reset_email']

        messages.success(request, "Your password has been successfully reset! You can now login.")
        return redirect('login') # अपनी लॉगिन URL का नाम यहाँ लिखें

    # GET Request: जब यूजर पहली बार पेज पर आएगा
    return render(request, 'reset.html')


def send_otp_view(request):
    """
    नोट: इस व्यू का उपयोग आप तब कर सकते हैं जब आप ईमेल डालकर 
    'Send OTP' बटन पर क्लिक करवाएं।
    """
    if request.method == "POST":
        email = request.POST.get('email')
        
        if User.objects.filter(email=email).exists():
            # 6 डिजिट का रैंडम OTP जनरेट करना
            otp = random.randint(100000, 999999)
            
            # OTP और ईमेल को सेशन में सेव करना (10 मिनट के लिए वैध रख सकते हैं)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            request.session.set_expiry(600) # 10 मिनट में एक्सपायर हो जाएगा

            # यूजर को ईमेल भेजना
            subject = "Netflix Clone - Password Reset OTP"
            message = f"Your OTP for resetting the password is: {otp}. Do not share this with anyone."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "OTP has been sent to your registered email.")
            except Exception as e:
                messages.error(request, "Failed to send email. Please check your SMTP settings.")
        else:
            messages.error(request, "This email is not registered with us.")
            
    return redirect('reset_password') # अपने रिसेट पासवर्ड वाले URL पर भेजें






import requests
from django.conf import settings
from django.shortcuts import render


def nav(req):

    API_KEY = settings.TMDB_API_KEY
    BASE_URL = "https://api.themoviedb.org/3"

    trending_movies = []
    netflix_originals = []
    tv_shows = []
    popular_movies = []
    upcoming_movies = []
    hindi_movies = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    session = requests.Session()

    # ================= Trending =================
    try:
        res = session.get(
            f"{BASE_URL}/trending/movie/day?api_key={API_KEY}",
            headers=headers,
            timeout=15
        )

        print("Trending Status:", res.status_code)
        print("Trending URL:", f"{BASE_URL}/trending/movie/day?api_key={API_KEY}")
        print("Trending Status:", res.status_code)
        print("Trending Response:", res.text[:300])

        if res.status_code == 200:
            trending_movies = res.json().get("results", [])

    except Exception as e:
        print("Trending Error:", e)


        

    # ================= Netflix Originals =================
    try:
        res = session.get(
            f"{BASE_URL}/discover/tv?api_key={API_KEY}&with_networks=213",
            headers=headers,
            timeout=15
        )

        print("Originals Status:", res.status_code)

        if res.status_code == 200:
            netflix_originals = res.json().get("results", [])

    except Exception as e:
        print("Originals Error:", e)

    # ================= TV Shows =================
    try:
        res = session.get(
            f"{BASE_URL}/tv/popular?api_key={API_KEY}",
            headers=headers,
            timeout=15
        )

        print("TV Status:", res.status_code)

        if res.status_code == 200:
            tv_shows = res.json().get("results", [])

    except Exception as e:
        print("TV Error:", e)

    # ================= Popular Movies =================
    try:
        res = session.get(
            f"{BASE_URL}/movie/popular?api_key={API_KEY}",
            headers=headers,
            timeout=15
        )

        print("Popular Status:", res.status_code)

        if res.status_code == 200:
            popular_movies = res.json().get("results", [])

    except Exception as e:
        print("Popular Error:", e)

    # ================= Upcoming Movies =================
    try:
        res = session.get(
            f"{BASE_URL}/movie/upcoming?api_key={API_KEY}",
            headers=headers,
            timeout=15
        )

        

        print("Upcoming Status:", res.status_code)
        print("Popular URL:", f"{BASE_URL}/movie/popular?api_key={API_KEY}")
        print("Popular Status:", res.status_code)
        print("Popular Response:", res.text[:300])

        if res.status_code == 200:
            upcoming_movies = res.json().get("results", [])

    except Exception as e:
        print("Upcoming Error:", e)

    # ================= Hindi Movies =================
    try:
        res = session.get(
            f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_original_language=hi&sort_by=popularity.desc",
            headers=headers,
            timeout=15
        )
        

        print("Hindi Status:", res.status_code)

        if res.status_code == 200:
            hindi_movies = res.json().get("results", [])

    except Exception as e:
        print("Hindi Error:", e)

    # ================= My List =================
    my_list_movies = trending_movies[2:8] if trending_movies else []

    print("Trending:", len(trending_movies))
    print("Originals:", len(netflix_originals))
    print("TV:", len(tv_shows))
    print("Popular:", len(popular_movies))
    print("Upcoming:", len(upcoming_movies))
    print("Hindi:", len(hindi_movies))

    

    context = {
        "trending_movies": trending_movies,
        "netflix_originals": netflix_originals,
        "tv_shows": tv_shows,
        "popular_movies": popular_movies,
        "upcoming_movies": upcoming_movies,
        "hindi_movies": hindi_movies,
        "my_list_movies": my_list_movies,

       
    }
  






    return render(req, "nav.html", context)



def movie_details(request, movie_id):

    API_KEY = settings.TMDB_API_KEY

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    response = requests.get(url)

    movie = {}

    if response.status_code == 200:
        movie = response.json()

    return render(request, "movie_details.html", {"movie": movie})




import requests
from django.conf import settings

def tvshows(req):

    url = "https://api.themoviedb.org/3/tv/popular"

    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "page": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        shows = data.get("results", [])

        print("TV SHOW COUNT:", len(shows))

        return render(req, "tvshows.html", {
            "shows": shows
        })

    except requests.RequestException as e:

        print("TMDB ERROR:", e)

        return render(req, "tvshows.html", {
            "shows": []
        })


    
import requests
from django.conf import settings

def movies(req):

    url = "https://api.themoviedb.org/3/movie/popular"

    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "page": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        movies = data.get("results", [])

    except requests.RequestException as e:
        print("TMDB ERROR:", e)
        movies = []

    return render(req, "movies.html", {
        "movies": movies
    })



import requests
from django.conf import settings

def newpopular(req):

    url = "https://api.themoviedb.org/3/movie/popular"

    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "page": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        movies = data.get("results", [])

        print("NEW & POPULAR:", len(movies))

    except requests.RequestException as e:
        print("TMDB ERROR:", e)
        movies = []

    return render(req, "newpopular.html", {
        "movies": movies
    })


from django.contrib.auth.decorators import login_required

@login_required
def mylist(req):

    saved_movies = MyList.objects.filter(user=req.user)

    if saved_movies.exists():
        movies = saved_movies
        recommended = False
    else:
        # Home page ki movies yahan se
        movies = get_home_movies()[:5]
        recommended = True

    return render(req, "mylist.html", {
        "movies": movies,
        "recommended": recommended
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import MyList


@login_required
def add_to_mylist(req, movie_id):

    MyList.objects.get_or_create(
        user=req.user,
        movie_id=movie_id,
    )

    return redirect('movies')



import requests
from django.conf import settings

def browselanguage(req):

    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "api_key": settings.TMDB_API_KEY,
        "with_original_language": "hi",
        "language": "en-US",
        "page": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        movies = data.get("results", [])

    except requests.RequestException as e:
        print("TMDB ERROR:", e)
        movies = []

    return render(req, "browselanguage.html", {
        "movies": movies
    })




def nlogo(req):
    return render(req,'nlogo.html')


def otp(req):
    return render(req,'otp.html')


def notification(req):
    return render(req,'notification.html')

def profile(req):
    return render(req,'profile.html')

def Subscription(req):
    return render(req,'Subscription.html')


def help(req):
    return render(req,'help.html')




def setting(req):
    return render(req,'setting.html')





def history(req):
    return render(req,'history.html')





import requests
from django.conf import settings
from django.shortcuts import render


def movie_details(req, movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        movie = response.json()

    except requests.RequestException as e:

        print("TMDB MOVIE DETAILS ERROR:", e)

        return render(req, "movie_details.html", {
            "movie": None
        })

    return render(req, "movie_details.html", {
        "movie": movie
    })



def search_movies(request):
    # Your search logic goes here...
    return render(request, 'search_results.html', context)
