from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import timezone
from django.db.models.functions import Lower

from bucketlist.models import Category, Page, Place
from bucketlist.forms import CategoryForm, PageForm

# def encode_url(str):
#     new_url  = str.replace(' ', '_')
#     new_url = new_url.replace(',', "")
#     return new_url

# def decode_url(str):
#     new_url  = str.replace(' ', '_')
#     new_url = new_url.replace(',', "")
#     return new_url


# Create your views here.
def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    all_categories = Category.objects.order_by(Lower('name').desc())
    all_pages = Page.objects.order_by(Lower('name').desc())

    # Initialize DB for proper URL Names 
    # for category in all_categories:
    #     category.name_url = encode_url(category.name)
    #     category.save()

    # for page in all_pages:
    #     page.name_url = encode_url(page.name)
    #     page.category_url = page.category.name_url
    #     page.save()

    context_dict={'full_categories': all_categories, 'filter_pages': all_pages} 

    # Render the response and return to the client.
    return render_to_response('html/index.html', context_dict, context)

def page_detail(request, category_name_url, page_name_url):

    context = RequestContext(request)

    filter_page = Page.objects.get(name_url=page_name_url)
    #filter_places = Place.objects.filter(location=filter_page)

    filter_see_places = Place.objects.filter(location=filter_page, category='See').order_by(Lower('name').desc())
    filter_eat_places = Place.objects.filter(location=filter_page, category='Eat').order_by(Lower('name').desc())
    filter_sleep_places = Place.objects.filter(location=filter_page, category='Sleep').order_by(Lower('name').desc())

    context_dict = {'filter_page': filter_page, 'filter_see_places': filter_see_places, 'filter_eat_places': filter_eat_places, 'filter_sleep_places': filter_sleep_places}
    
    context_dict['category_name_url'] = category_name_url
    context_dict['page_name_url'] = page_name_url
    
    return render_to_response('html/detail.html', context_dict, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    
    context_dict = {}
  
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            page = form.save(commit=False)
            page.create_page()
            
            return category(request, category_name_url)
        else:
            return HttpResponse("Failed")
    else:
        form = PageForm()

    context_dict['category_name_url']= category_name_url
    context_dict['form'] = form

    return render_to_response('html/add_page.html',context_dict,context)

def edit_page(request, category_name_url, page_name_url):

    context = RequestContext(request)

    # Get the page
    try:
        filter_page = Page.objects.get(name_url=page_name_url)
    except Page.DoesNotExist:
        return HttpResponse("Failed")

    context_dict = {'filter_page': filter_page}

    if request.method == 'POST':
        form = PageForm(request.POST, instance = filter_page)
        
        if form.is_valid():
            new_page = form.save(commit=False)
            new_page.save()
            new_page_url = encode_url(new_page.name)
            return page_detail(request, category_name_url, new_page_url)
        else:
            return HttpResponse("Failed")
    else:
        form = PageForm(instance = filter_page)

    context_dict['category_name_url']= category_name_url
    context_dict['page_name_url'] = page_name_url
    context_dict['form'] = form
    
    return render_to_response('html/add_page.html', context_dict, context)

def delete_page(request, category_name_url, page_name_url):
    context = RequestContext(request)
    
    try:
        Page.objects.get(name_url=page_name_url).delete()

    except Page.DoesNotExist:
        # We get here if we didn't find the specified page.
        # Don't do anything - the template displays the "no category" message for us.
        return HttpResponse("Failed")

    return category(request, category_name_url)
    
def places_page(request, category_name_url, page_name_url):

    context = RequestContext(request)
    
    filter_category_name = decode_url(category_name_url)
    filter_page_name = decode_url(page_name_url)

    # Get the page
    try:
        filter_page = Page.objects.get(name=filter_page_name).order_by(Lower('name').desc())
    except Page.DoesNotExist:
        return HttpResponse("Failed")

    #filter_places = Place.objects.filter(location=filter_page)
    filter_see_places = Place.objects.filter(location=filter_page, category='See')
    filter_eat_places = Place.objects.filter(location=filter_page, category='Eat')
    filter_sleep_places = Place.objects.filter(location=filter_page, category='Sleep')

    context_dict = {'filter_category_name': filter_category_name, 'filter_page': filter_page, 'filter_see_places': filter_see_places, 'filter_eat_places': filter_eat_places, 'filter_sleep_places': filter_sleep_places}
    context_dict['category_name_url']= category_name_url
    context_dict['page_name_url'] = page_name_url
    context_dict['category_name'] = filter_category_name
    
    return render_to_response('html/places.html', context_dict, context)


def about(request):
    return HttpResponse("About What? <a href='/bucketlist/'>Index</a>")

def category_list(request):
     return render_to_response('html/category_list.html')

def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Build up the dictionary we will use as out template context dictionary.
    context_dict = {'filter_category_name_url': category_name_url}

    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list
    
    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        if category_name_url == '':
            filter_category = Category.objects.order_by(Lower('name').desc())
        else:
            filter_category = Category.objects.get(name_url=category_name_url)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        filter_pages = Page.objects.filter(category_url=category_name_url).order_by(Lower('name').desc())
        
        # Adds our results list to the template context under name pages.
        context_dict['filter_pages'] = filter_pages
        
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['filter_category'] = filter_category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        return render_to_response('html/index.html', context_dict, context)

    # Go render the response and return it to the client.
    return render_to_response('html/index.html', context_dict, context)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        category_name = new_category.name

        # Have we been provided with a valid form?
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.create_category()
            return category(request, category_name)
        else:
            return index(request)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'html/add_category.html', {'form': form})

def edit_category(request, category_name_url):
    context = RequestContext(request)
    
    context_dict = {}
    
    # Get the category
    try:
        cat = Category.objects.get(name_url=category_name_url)
    except Category.DoesNotExist:
        return render_to_response('html/index.html',context_dict,context)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=cat)
        
        # Have we been provided with a valid form?
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()

            #cat.name = new_category.name
            #cat.save()

            return category(request, new_category.name_url)
        else:
            return category(request, category_name_url)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm(instance=cat)

    context_dict['category_name_url']= category_name_url
    context_dict['form'] = form

    return render_to_response('html/add_category.html',context_dict,context)

def delete_category(request, category_name_url):
    context = RequestContext(request)
    
    context_dict = {}
    
    try:
        Category.objects.filter(name_url=category_name_url).delete()

    except Category.DoesNotExist:
        # We get here if we didn't find the specified page.
        return render_to_response('html/index.html',context_dict,context)

    full_category_list = Category.objects.order_by(Lower('name').desc())
    context_dict['full_categories'] = full_category_list

    for category in full_category_list:
        category.url = encode_url(category.name)

    return render_to_response('html/index.html',context_dict,context)

