from django.shortcuts import render,redirect
from .models import Post,Comment,Like
from Profiles.models import *
from Posts.forms import PostModelForm,CommentModelForm
from django.views.generic import DeleteView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
#Posts
@login_required
def post_comment_create_and_list_view(request):
    qs=Post.objects.all()
    profile=Profile.objects.get(user=request.user)

    post_form=PostModelForm()
    comment_form=CommentModelForm()
    post_added=False
    comment_added=False
    #name of button 
    if "submit-post-form" in request.POST:
        print(request.POST)

        post_form=PostModelForm(request.POST ,request.FILES)
        if post_form.is_valid():
            instance=post_form.save(commit=False)
            instance.author=profile
            instance.save()
            post_form=PostModelForm()
            post_added=True

    if "submit-comment-form" in request.POST:
        comment_form=CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance=comment_form.save(commit=False)
            #in comment model user and post are foreign keys to Profile,Post model
            instance.user=profile
            instance.post=Post.objects.get(id=request.POST.get('post_id'))#getting by name=post_id in form
            instance.save()
            comment_form=CommentModelForm()
            comment_added=True
    
    context={
        "qs":qs,
        "profile":profile,
        "post_form":post_form,
        "comment_form":comment_form,
        "post_added":post_added
        }
    return render(request,"Posts/main.html",context)
@login_required
def like_unlike_post(request):
    user=request.user
    if request.method == 'POST':
        ##calling name=post_id 
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        profile=Profile.objects.get(user=user)
        #proofile model is showing forward relation with liked in Post
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like,created=Like.objects.get_or_create(user=profile,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

        post_obj.save()
        like.save()

        data={
            "value":like.value,
            "likes":post_obj.liked.all().count()
            }

        #return JsonResponse(data,safe=False)
    return redirect('main-post-view')

class PostDeleteView(LoginRequiredMixin ,DeleteView):
    model=Post
    template_name="Posts/confirm_delete.html"
    success_url=reverse_lazy('main-post-view')

    def get_object(self,*args,**kwargs):
        pk=self.kwargs.get('pk')
        obj=Post.objects.get(pk=pk)

        if not obj.author.user == self.request.user:
            messages.warning(self.request,"you need to be the author of the post in order to delete it.")
        return obj

class PostUpdateView(LoginRequiredMixin ,UpdateView):
    form_class=PostModelForm
    model=Post
    template_name="Posts/update.html"
    success_url=reverse_lazy('main-post-view')
    def form_valid(self,form):
        profile=Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None,"you need to be the author of the post in order to update it.")

