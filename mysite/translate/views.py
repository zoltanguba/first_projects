from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import NewContentForm, WordTranslationForm
from .models import Translate, WordDatabase, DestinationLanguage
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  FormView
                                 )
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers


def home(request):
    if request == 'POST':
        form = NewContentForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'Your content with the title {title} has been saved.')
            return redirect('translate')
    else:
        form = NewContentForm()
    return render(request, 'personal/base.html', {'form': form})


class ContentCreateView(CreateView):
    model = Translate
    fields = ['library', 'title', 'language', 'content']
    template_name = 'translate/create_content.html'


class TitleListView(ListView):
    model = Translate
    template_name = 'translate/translator.html'
    context_object_name = 'Translate'


class ContentListView(ListView):
    model = Translate
    template_name = 'translate/list_content.html'
    context_object_name = 'Translate'


@login_required(login_url='/login/')
def content_by_library(request):
    user = request.user

    content_list = Translate.objects.filter(user=user)
    distinct_libraries = Translate.objects.filter(user=user).values('library').distinct()
    paginator = Paginator(distinct_libraries, 3)

    page = request.GET.get('page')
    paginated_libraries = paginator.get_page(page)

    return render(request, 'translate/list_content.html', {'content_list': content_list,
                                                           'distinct_libraries': distinct_libraries,
                                                           'paginated_libraries': paginated_libraries})


class ContentDetailView(DetailView):
    model = Translate
    template_name = 'translate/translator.html'
    context_object_name = 'Translate'


@login_required(login_url='/login/')
def create_new_content(request):
    form = NewContentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Your content with the title {instance.title} has been saved.')
            return redirect('contentlist')
        else:
            form = NewContentForm()
    return render(request, 'translate/create_content.html', {'form': form})


def manage_word_translation(request, pk):
    if request.method == 'POST':
        srcLanguage = request.POST['srcLanguage']

        word = request.POST['word']
        #  destLanguage = request.POST['destLanguage']
        translatedWord1 = request.POST['translatedWord']
        knownlevel = request.POST['knownlevel']
        contentid = request.user
        destLanguage = DestinationLanguage.objects.filter(user=contentid).values('destLanguage')[0]['destLanguage']

        data = {
            'wordexists': WordDatabase.objects.filter(word__iexact=word,
                                                      contentid=contentid,
                                                      srcLanguage__iexact=srcLanguage).exists()
        }
        if data['wordexists']:
            WordDatabase.objects.filter(word__iexact=word).update(translatedWord1=translatedWord1)
            WordDatabase.objects.filter(word__iexact=word).update(knownlevel=knownlevel)
            return HttpResponse('')
        else:
            WordDatabase.objects.create(
                srcLanguage=srcLanguage,
                word=word,
                destLanguage=destLanguage,
                translatedWord1=translatedWord1,
                knownlevel=knownlevel,
                contentid=contentid
            )
            return HttpResponse('')


def get_word_known_level(request, pk):
    if request.method == 'GET':
        wordtocheck = request.GET.get('wordtocheck', None)
        srcLanguage = request.GET.get('srcLanguage', None)
        userid = request.user
        ownuser = WordDatabase.objects.filter(word__iexact=wordtocheck,
                                              contentid=userid,
                                              srcLanguage__iexact=srcLanguage).exists()
        otheruser = WordDatabase.objects.filter(word__iexact=wordtocheck,
                                                srcLanguage__iexact=srcLanguage).exists()

        if ownuser:
            data = {
                'wordexists': WordDatabase.objects.filter(word__iexact=wordtocheck,
                                                          contentid=userid,
                                                          srcLanguage__iexact=srcLanguage).exists(),
                'knownlevel': WordDatabase.objects.filter(contentid=userid, word__iexact=wordtocheck).values('knownlevel')[0]['knownlevel'], # The query returns a list of dicts, that's why the 0 index is needed
                'translatedWord1': WordDatabase.objects.filter(contentid=userid, word__iexact=wordtocheck).values('translatedWord1')[0]['translatedWord1']
            }
            return JsonResponse(data)
        elif otheruser:

            data2 = WordDatabase.objects.filter(word__iexact=wordtocheck).values('translatedWord1')
            datatosend = []
            for item in list(data2):
                datatosend.append(item['translatedWord1'])


            data = {
                'wordexists': WordDatabase.objects.filter(word__iexact=wordtocheck,
                                                          contentid=userid,
                                                          srcLanguage__iexact=srcLanguage).exists(),
                'translatedWord1': datatosend
            }
            return JsonResponse(data)

        else:
            data = {
                'wordexists': WordDatabase.objects.filter(word__iexact=wordtocheck,
                                                          contentid=userid,
                                                          srcLanguage__iexact=srcLanguage).exists()
            }
            return JsonResponse(data)


#  Change translator window view based on the word the user has clicked on
def translator_window_design(request,pk):
    if request.method == 'GET':
        wordtocheck = request.GET.get('wordtocheck', None)
        data = {
            'wordexists': WordDatabase.objects.filter(word__iexact=wordtocheck).exists()
        }
        return JsonResponse(data)


@login_required(login_url='/login/')
def delete_content(request, pk):
    content_to_delete = Translate.objects.filter(pk__iexact=pk)
    if request.method == 'POST':
        title = Translate.objects.filter(pk__iexact=pk).values('title')[0]['title']
        instance = Translate.objects.get(pk=pk)
        instance.delete()
        #  Translate.objects.filter(pk__iexact=pk).delete
        messages.success(request, f'Your content with the title {title} has been deleted.')
        return redirect('contentlist')


    return render(request, 'translate/delete_content.html', {'content_to_delete': content_to_delete})





def translate(request):
    return render(request, 'translate/translator.html')


def timer(request):
    return render(request, 'personal/timer.html')


''' 
    def create_translation(request):
    if request.method == 'POST':
    srcLanguage = request.POST['srcLanguage']
       word = request.POST['word']
       destLanguage = request.POST['destLanguage']
       translatedWord = request.POST['translatedWord']

       WordDatabase.objects.create(
           srcLanguage=srcLanguage,
           word=word,
           destLanguage=destLanguage,
           translatedWord=translatedWord
       )

   return HttpResponse('')


def word_view(request, pk):
    translate = Translate.objects.get(id=pk)
    return render(request, 'translate/translator.html', context={'Translate': translate})
    
    

def create_word_translation1(request, pk):
    form = WordTranslationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return HttpResponse('')


def create_word_translation(request, pk):
    if request.method == 'POST':
        srcLanguage = request.POST['srcLanguage']
        word = request.POST['word']
        destLanguage = request.POST['destLanguage']
        translatedWord1 = request.POST['translatedWord']
        knownlevel = request.POST['knownlevel']
        contentid = request.POST['contentid']

        WordDatabase.objects.create(
            srcLanguage=srcLanguage,
            word=word,
            destLanguage=destLanguage,
            translatedWord1=translatedWord1,
            knownlevel=knownlevel,
            contentid=contentid
        )
        return HttpResponse('')
'''