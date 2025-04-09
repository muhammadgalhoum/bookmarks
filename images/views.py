import redis
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden

from .forms import ImageCreateForm, ImageUpdateForm
from .models import Image

from actions.utils import create_action


# Connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# Create your views here.

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'create_image.html', {'section': 'images', 'form': form})


@login_required
def image_update(request, year, month, day, slug):
    image = get_object_or_404(
        Image, created__year=year, created__month=month, created__day=day, slug=slug)

    if image.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this image.")

    if request.method == 'POST':
        form = ImageUpdateForm(
            instance=image, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image updated successfully.')
            return redirect(image.get_absolute_url())
    else:
        form = ImageUpdateForm(instance=image)

    return render(request, 'create_image.html', {'section': 'images', 'form': form, 'is_update': True})


@login_required
def image_detail(request, year, month, day, slug):
    image = get_object_or_404(
        Image, created__year=year, created__month=month, created__day=day, slug=slug)
    
    # Increment total image views by 1
    total_views = r.incr(f'image:{year}:{month}:{day}:{slug}:views')

    # Increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)

    follower_ids = image.user.followers.values_list('id', flat=True)
    if request.user.id in follower_ids or request.user == image.user:
        return render(request, 'image_detail.html', 
            {'section': 'images', 'image': image, 'total_views': total_views})
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not authorized to access this page.'})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.liked_by.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.liked_by.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Image URL or Image does not exist.'})
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    following_ids = request.user.following.values_list('id', flat=True)
    images = Image.objects.filter(user_id__in=following_ids)
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # If AJAX request and page out of range, return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request, 'list_images.html', {'section': 'images', 'images': images})
        
    return render(request,'list.html',{'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # Get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # Get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images_ranking.html', {'section': 'images', 'most_viewed': most_viewed})
