from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Ebook, Comment
from django.core.paginator import Paginator
from django.contrib import auth
from django.utils import timezone
from django.db.models import Q
import operator

def home(request):
    ebooks = Ebook.objects.order_by('-id')[:8]
    return render(request, 'ebook/home.html', {
        'ebooks' : ebooks
    })

def categories(request):
    categories = Category.objects.order_by('name')
    return render(request, 'ebook/categories.html', {
		'categories': categories,
		})

def category(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    ebooks = category.ebook_set.all()

    paginator = Paginator(ebooks, 12)
    try:
        page = request.GET['page']
    except:
        page = 1
    ebooks = paginator.get_page(page)

    return render(request, 'ebook/category.html', {
		'category' : category,
		'ebooks' : ebooks
		})

def ebooks(request):
    ebooks = Ebook.objects.all()
    paginator = Paginator(ebooks, 12)
    try:
        page = request.GET['page']
    except:
        page = 1
    ebooks = paginator.get_page(page)
    return render(request, 'ebook/ebooks.html', {
		'ebooks': ebooks,
		})

def ebook(request, ebook_id):
    ebook = get_object_or_404(Ebook, pk = ebook_id)
    comments = ebook.comment_set.all()
    return render(request, 'ebook/ebook.html', {
		'ebook' : ebook,
        'comments' : comments,
		})

def comment(request, ebook_id):
    if request.method == 'POST':
        user = auth.get_user(request)
        ebook = get_object_or_404(Ebook, pk = ebook_id)

        # create the comment
        comment = Comment()
        comment.body = request.POST['body']
        comment.pub_time = timezone.datetime.now()
        comment.ebook = ebook
        comment.user = user
        comment.save()

        return redirect('ebook', ebook_id)
    else:
        return redirect('home')

def staff(request):
    return render(request,'admin/')

def search(request):
    return render(request,'ebook/search.html')

def search_books(request):

    if request.method=='POST':
        srch=request.POST.get('srh')

        if srch:
            match=Ebook.objects.filter(Q(title=srch)|Q(authors=srch)|Q(title__icontains=srch)|Q(authors__icontains=srch)|Q(title__istartswith=srch)|Q(authors__istartswith=srch))

            paginator = Paginator(match, 12)
            try:
                page = request.GET['page']
            except:
                page = 1
            match = paginator.get_page(page)

            if match:
                return render(request, 'ebook/search.html', {
            		'ebooks': match,
            		})
            else:
                return render(request,'ebook/search.html',{'error':"No result found"})
        else:
            return render(request,'ebook/search.html')

    return render(request,'ebook/search.html')
