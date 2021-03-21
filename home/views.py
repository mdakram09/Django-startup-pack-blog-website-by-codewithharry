
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    messages.success(request, 'Welcome To Contact')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 3 or len(email) < 5 or len(phone) < 10 or len(content) < 6:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(request, 'Thank you for submitting Your Form')
    return render(request, 'home/contact.html')


def about(request):
    messages.success(request, 'Welcome To About Page')
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 25:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, 'Search results not found')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Check for error inputs
        if len(username) > 10:
            messages.error(
                request, 'Your username is too long')
            return redirect('home')
        if not username.isalnum():

            messages.error(
                request, 'Your username is invalid')
            return redirect('home')
        if pass1 != pass2:
            messages.error(
                request, 'Passwords donot match')
            return redirect('home')

        # Create The user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your account has been successfully created')
        return redirect('home')

    else:
        request.HttpResponse('404-Not Found!!')


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    return HttpResponse('404- Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')
