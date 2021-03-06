from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your views here.
def register(request):
	if request.method == "POST":
		first_name=request.POST["first_name"]
		last_name=request.POST["last_name"]
		username= request.POST["username"]
		email= request.POST["email"]
		password= request.POST["password"]
		password2= request.POST["password2"]
		# messages.error(request,"Testing error message")
		# #register user
		# return redirect("register")
		if password == password2:
			if User.objects.filter(username=username).exists():
				messages.error(request,"Username already exists")
				return redirect("register")
			else:
				if User.objects.filter(email=email).exists():
					messages.error(request,"Email already used")
					return redirect("register")
				else:
					user =User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
					#login after register
					# auth.login(request,user)
					# messages.success(request, "Logged In")
					# return redirect("index")
					user.save();
					messages.success(request, "Registered")
					return redirect("login")
			
		else:
			messages.error(request,"PASSWORD DID NOT MATCH")
			return render(request, "accounts/register.html")
	else:
		return render(request, "accounts/register.html")
def login(request):
	if request.method == "POST":
		#login user
		username = request.POST["username"]
		password = request.POST["password"]
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request,user)
			messages.success(request, "You have been logged in")
			return redirect("dashboard")
		else:
			messages.error(request,"INVALID")
			return redirect("login")
				

	
	else:
		return render(request, "accounts/login.html")
def logout(request):
	if request.method == "POST":
		auth.logout(request)
		messages.success(request,"you are now logged out")
		return redirect("index")
	
	 #logout click vaesi index--homepage ma janx...logout vanne no html
def dashboard(request):
	user_contacts = Contact.objects.order_by("-contact_date").filter(user_id=request.user.id)
	context={
	"contacts":user_contacts
	}

	return render(request, "accounts/dashboard.html",context)