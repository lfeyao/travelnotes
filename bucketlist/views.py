from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import timezone
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from bucketlist.models import Category, Page, Place
from bucketlist.forms import CategoryForm, PageForm, PlaceForm, UserForm, UserProfileForm

# def encode_url(str):
#     new_url  = str.replace(' ', '_')
#     new_url = new_url.replace(',', "")
#     return new_url

# def decode_url(str):
#     new_url  = str.replace(' ', '_')
#     new_url = new_url.replace(',', "")
#     return new_url

# def initialize_db(all_categories, all_pages):
    # for page in all_pages:
    #     page.was_done = True
    #     page.save()

    # Initialize DB for proper URL Names 
    # for category in all_categories:
    #     category.name_url = encode_url(category.name)
    #     category.save()

    # for page in all_pages:
    #     page.name_url = encode_url(page.name)
    #     page.category_url = page.category.name_url
    #     page.save()

    # all_places = Place.objects.order_by(Lower('name').desc())
    # for place in all_places:
    #     place.name_url = encode_url(place.name)
    #     place.save()

# Create your views here.
@login_required
def index(request):

    all_categories = Category.objects.order_by(Lower('name').desc())
    all_pages = Page.objects.order_by(Lower('name').desc())
    upcoming_trips = Page.objects.filter(was_done = False).order_by('-likes')

    # initialize_db(all_categories, all_pages)

    context_dict={'full_categories': all_categories, 'filter_pages': all_pages, 'upcoming_trips': upcoming_trips} 

    # Render the response and return to the client.
    return render(request, 'html/index.html', context_dict)

    
@login_required
def category(request, category_name_url):

    # Build up the dictionary we will use as out template context dictionary.
    context_dict = {'filter_category_name_url': category_name_url}

    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list
    
    try:
        filter_category = Category.objects.get(name_url=category_name_url)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        filter_pages = Page.objects.filter(category_url=category_name_url).order_by(Lower('name').desc())
        
        # Adds our results list to the template context under name pages.
        context_dict['filter_pages'] = filter_pages
        
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['filter_category'] = filter_category

        upcoming_trips = Page.objects.filter(category_url=category_name_url, was_done = False).order_by('-likes')
        context_dict['upcoming_trips'] = upcoming_trips

    except Category.DoesNotExist:
        return redirect('/')

    # Go render the response and return it to the client.
    return render(request, 'html/index.html', context_dict)

@permission_required('bucketlist.create_category')
def add_category(request):
    
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # Have we been provided with a valid form?
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.create_category()
            return redirect('/category/' + new_category.name_url)
        else:
            return index(request)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'html/add_category.html', {'form': form})

@permission_required('bucketlist.change_category')
def edit_category(request, category_name_url):
    
    context_dict = {}
    
    # Get the category
    try:
        filter_category = Category.objects.get(name_url=category_name_url)
    except Category.DoesNotExist:
        return HttpResponse("Failed")

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=filter_category)
        
        # Have we been provided with a valid form?
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()

            return redirect('/category/' + new_category.name_url)
        else:
            return redirect('/')
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm(instance=filter_category)

    context_dict['category_name_url']= category_name_url
    context_dict['form'] = form

    return render(request, 'html/add_category.html',context_dict)

@login_required
def page_detail(request, category_name_url, page_name_url):

    filter_page = Page.objects.get(name_url=page_name_url)
    
    filter_see_places = Place.objects.filter(location=filter_page, category='See').order_by('-likes')
    filter_eat_places = Place.objects.filter(location=filter_page, category='Eat').order_by('-likes')
    filter_sleep_places = Place.objects.filter(location=filter_page, category='Sleep').order_by('-likes')

    context_dict = {'filter_page': filter_page, 'filter_see_places': filter_see_places, 'filter_eat_places': filter_eat_places, 'filter_sleep_places': filter_sleep_places}
    
    context_dict['category_name_url'] = category_name_url
    context_dict['page_name_url'] = page_name_url

    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list

    return render(request, 'html/page_detail.html', context_dict)

@login_required
def add_page(request, category_name_url = None):
    context_dict ={}
    
    if category_name_url is not None:
        filter_category = Category.objects.get(name_url=category_name_url)

    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            page = form.save(commit=False)
            page.create_page()

            return redirect('/category/' + page.category_url + '/' + page.name_url)
            # return category(request, page.category_url)
        else:
            return HttpResponse("Failed")
    else:
        if category_name_url is None:
            form = PageForm()
        else:
            form = PageForm(initial = {'category': filter_category})

    context_dict['form'] = form
    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list

    return render(request, 'html/add_page.html',context_dict)

@permission_required('bucketlist.change_page')
def edit_page(request, category_name_url, page_name_url):

    # Get the page
    try:
        filter_page = Page.objects.get(name_url=page_name_url)
    except Page.DoesNotExist:
        return HttpResponse("Failed")

    context_dict = {'filter_page': filter_page}

    if request.method == 'POST':
        form = PageForm(request.POST, instance = filter_page)
        
        if form.is_valid():
            page = form.save(commit=False)
            page.create_page()
            new_page_url = page.name_url
            return redirect('/category/' + category_name_url + '/' + new_page_url)
            # return page_detail(request, category_name_url, new_page_url)
        else:
            return HttpResponse("Failed")
    else:
        form = PageForm(instance = filter_page)

    context_dict['category_name_url']= category_name_url
    context_dict['page_name_url'] = page_name_url
    context_dict['form'] = form
    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list

    return render(request, 'html/add_page.html', context_dict)

@permission_required('bucketlist.delete_page')
def delete_page(request, category_name_url, page_name_url):
    
    context_dict = {}
    # Get the place
    try:
        filter_page = Page.objects.get(name_url=page_name_url)

    except Category.DoesNotExist:
        return HttpResponse("Failed")

    filter_page.delete()

    return redirect('/')

@login_required
def add_place(request, category_name_url, page_name_url):
    
    context_dict = {}

    filter_page = Page.objects.get(name_url=page_name_url)
    
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        
        if form.is_valid():
            place = form.save(commit=False)
            place.create_place()
            return redirect('/category/' + category_name_url + '/' + page_name_url)
            # return page_detail(request, category_name_url, page_name_url)
        else:
            return HttpResponse("Failed")
    else:
        form = PlaceForm(initial = {'location': filter_page})

    context_dict['category_name_url']= category_name_url
    context_dict['page_name_url']= page_name_url
    context_dict['form'] = form

    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list

    return render(request, 'html/place_detail.html', context_dict)

@login_required
def edit_place(request, category_name_url, page_name_url, place_id):
    
    context_dict = {}
    # Get the place
    try:
        filter_place = Place.objects.get(id=place_id)

    except Category.DoesNotExist:
        return HttpResponse("Failed")

    if request.method == 'POST':
        form = PlaceForm(request.POST, instance = filter_place)
        
        if form.is_valid():
            place = form.save(commit=False)
            place.save()

            return redirect('/category/' + category_name_url + '/' + page_name_url)
        else:
            return HttpResponse("Failed")
    else:
        form = PlaceForm(instance = filter_place)

    context_dict['category_name_url']= category_name_url
    context_dict['page_name_url']= page_name_url
    context_dict['form'] = form
    context_dict['filter_place']= filter_place

    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list

    return render(request, 'html/place_detail.html', context_dict)

@permission_required('bucketlist.delete_place')
def delete_place(request, category_name_url, page_name_url, place_id):
    
    context_dict = {}
    # Get the place
    try:
        filter_place = Place.objects.get(id=place_id)

    except Category.DoesNotExist:
        return HttpResponse("Failed")

    filter_place.delete()

    return redirect('/category/' + category_name_url + '/' + page_name_url)

@login_required
def vote_place(request, category_name_url, page_name_url, place_id, direction):
   
    filter_place = Place.objects.get(id=place_id)
    if direction == "up":
        filter_place.likes = filter_place.likes + 1

    if direction == "down":
        filter_place.likes = filter_place.likes - 1
    
    filter_place.save()

    return redirect('/category/' + category_name_url + '/' + page_name_url)

@login_required
def vote_page(request, category_name_url, page_name_url, direction):
   
    filter_page = Page.objects.get(name_url=page_name_url)
    if direction == "up":
        filter_page.likes = filter_page.likes + 1

    if direction == "down":
        filter_page.likes = filter_page.likes - 1
    
    filter_page.save()

    return redirect('/')

# User Registration View

@permission_required('bucketlist.create_userprofile')
def register(request):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}

    # Render the template depending on the context.
    return render_to_response('html/register.html',context_dict,context)

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'html/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return redirect('/login')