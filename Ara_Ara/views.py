from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg
from django.shortcuts import render, redirect

from Ara_Ara.forms import NewUserForm
from Ara_Ara.models import Anime, Review


def generate_context():
    return {
        'top_anime': [Anime.objects.get(id=i['anime']) for i in
                      Review.objects.values('anime').annotate(avg_score=Avg('score')).order_by('-avg_score')[:6]],
        'ongoing_favourites': [Anime.objects.get(id=i['anime']) for i in
                               Review.objects.values('anime')
                                   .filter(anime__in=Anime.objects.values('id').filter(status='a'))
                                   .annotate(avg_score=Avg('score')).order_by('-avg_score')[:6]]
    }


# Create your views here.
@login_required
def view_base(request):
    return render(request, 'base.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, "Account created!")
            messages.info(request, f"You are now logged in as {username}")
            return redirect('homepage')

        for field in form:
            for msg in field.errors:
                print(msg)
                messages.error(request, msg)
        return render(request, 'register.html', context=dict(form.__dict__['data']))

    return render(request, 'register.html')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect(request.GET.get('next', '/').replace("?", "%3F"))
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# logout a user
@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


# display homepage
def homepage(request):
    context = generate_context()
    context['animes'] = Anime.objects.all().order_by('total_eps')[::-1]
    return render(request, 'homepage.html', context)


def anime_details(request, anime_id):
    context = generate_context()
    context['anime'] = Anime.objects.get(id=anime_id)
    context['user_reviews'] = Review.objects.filter(anime=context['anime'], user__is_staff=False)[:3]
    context['staff_reviews'] = Review.objects.filter(anime=context['anime'], user__is_staff=True)[:3]
    context['scores'] = Review._meta.get_field('score').choices[::-1]
    return render(request, 'anime.html', context)


def review(request):
    if request.method == 'POST':
        new_review = Review(
            anime=Anime.objects.get(id=request.POST['anime_id']),
            user=request.user,
            score=request.POST['score'],
            review=request.POST['review'].replace('\n', '<br/>')
        )
        new_review.save()
        messages.success(request, f"Review for {new_review.anime} added!")
        return anime_details(request, anime_id=new_review.anime.id)
