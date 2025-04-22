from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Contact
from .forms import *

from actions.models import Action
from actions.utils import create_action


User = get_user_model()

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    # Flat=True means that the result will be a list of ids instead of list of tuples
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        # The query is for retrieving the user actions, including related objects
        actions = actions.select_related('user').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES,)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request, 'account/edit.html', {'user_form': user_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    paginator = Paginator(users, 6)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        # If page out of range return the last page
        users = paginator.page(paginator.num_pages)
    return render(request, 'account/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, slug, uuid):
    # Get user by UUID (primary lookup)
    user = get_object_or_404(User, uuid=uuid, is_active=True)
    # Redirect if slug is outdated (e.g., username changed)
    if user.slug != slug:
        return redirect("account:user_detail", slug=user.slug, uuid=user.uuid, permanent=True)
    return render(request, 'account/detail.html', {'section': 'people', 'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if user == request.user:
                return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself.'})
            else:
                if action == 'follow':
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                    create_action(request.user, 'is following', user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
