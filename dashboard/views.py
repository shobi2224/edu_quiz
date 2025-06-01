from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib import messages
from .login_req import login_required

# Create your views here.
@login_required
def dashboard(request):
    # Get the selected topic from session, if any
    selected_topic = request.session.get('selected_topic', None)
    
    if request.method == 'POST':
        selected_topic = request.POST.get('topic')
        # Store the selected topic in session
        request.session['selected_topic'] = selected_topic
        return redirect('quiz', topic_name=selected_topic) 

    return render(request,'dashboard/dashboard.html', {'selected_topic': selected_topic})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = MyUser.objects.get(username=username,password=password)
            request.session['user_id'] = user.id
            request.session['username'] = username
            messages.success(request, 'Logged in Successfully')
            return redirect('dashboard')
        except MyUser.DoesNotExist:
            messages.error(request, 'Invalid Credentials')
            return redirect('login') 

    return render(request, 'dashboard/login.html')        

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')   

        if password != confirm_password:
            messages.error(request, 'Password does not match!')
            return redirect('register')

        if MyUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if MyUser.objects.filter(email=email).exists():
            messages.error(request, 'Email ID is taken!')
            return redirect('register')
        
        MyUser.objects.create(username=username,email=email,password=password)
        messages.success(request, 'Registration Successful. Please Login.')
        return redirect('login')
    
    return render(request, 'dashboard/register.html')
    
def logout_view(request):
    request.session.flush()
    return redirect('login')