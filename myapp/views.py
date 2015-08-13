from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy

from .forms import NameForm
from .models import Choice, Question, Author

def add_name(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = NameForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            #return render_to_response('polls/author.html', {'form': form}, context)
            return HttpResponse("Error.")
    else:
        # If the request was not a POST, display the form to enter details.
        form = NameForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('polls/author.html', {'form': form}, context)

# Create your views here.
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'polls/author.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'polls/author.html', {'form': form})
    
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')#[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def author(request):
    latest_author_list = Author.objects.all()
    context = {'latest_author_list': latest_author_list}
    return render(request, 'polls/author.html', context)

class AuthorCreate(generic.CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(generic.UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(generic.DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

def add_Question(request):
    if(request.GET.get('mybtn')):
        q = Question(question_text="What's new?", pub_date=timezone.now())
        q.save()
    return IndexView.as_view()

"""
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
"""

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp:results', args=(p.id,)))