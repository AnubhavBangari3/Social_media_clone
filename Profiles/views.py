from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Profile,Relationship
from Posts.models import Post
from .forms import ProfileModelForm,SignUpForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.models import User


# Create your views here.
def login_view(request):
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(User,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(reverse('home'))
        else:
            return render(request,"Profiles/login.html")
    else:
        return render(request,"Profiles/login.html")

def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
def register(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('login'))
        else:
            pass
            
    else:
        form=SignUpForm()
        return render(request,"Profiles/register.html",{"form":form})


@login_required
def home_view(request):
    p=Post.objects.all()
    context={
        "user":request.user,
        'p':p
        }
    return render(request,"Profiles/home.html",context)
@login_required
def my_profile_view(request):
    profile=Profile.objects.get(user=request.user)
    form=ProfileModelForm(request.POST or None,request.FILES or None,instance=profile)
    confirm=False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context={
        "profile":profile,
        "form":form,
        "confirm":confirm
        
        }

    return render(request,"Profiles/my_profile.html",context)
@login_required
def invites_received_view(request):
    profile=Profile.objects.get(user=request.user)
    qs=Relationship.objects.invitation_received(profile)
    results=list(map(lambda x:x.sender,qs))
    isEmpty=False
    if len(results) == 0:
        isEmpty=True

    context={
        "qs":results,
        "isEmpty":isEmpty

        }

    return render(request,"Profiles/invite.html",context)

@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)

        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my-invite')
@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
        rel.delete()
    return redirect('my-invite')

#def profiles_list_view(request):
#    user=request.user
#    qs=Profile.objects.get_all_profiles(user)

#    context={
#        "qs":qs
#        }

#    return render(request,"Profiles/profile_list.html",context)
@login_required
def invite_profiles_list_view(request):
    user=request.user
    qs=Profile.objects.get_all_profiles_to_invite(user)

    context={
        "qs":qs
        }

    return render(request,"Profiles/to_invite_list.html",context)
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model=Profile
    template_name='Profiles/detail.html'

    def get_object(self,slug=None):
        slug=self.kwargs.get('slug')
        profile=Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)
        context['profile']=profile
        #rel_r we are the sender
        rel_r=Relationship.objects.filter(sender=profile)
        #rel_s we are the receiver
        rel_s=Relationship.objects.filter(receiver=profile)
        rel_receiver=[]
        rel_sender=[]
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"]=rel_receiver
        context["rel_sender"]=rel_sender
        context["posts"]=self.get_object().get_all_author_post()
        context["len_posts"]=True if len(self.get_object().get_all_author_post()) > 0 else False
        
        return context

class ProfileListView(LoginRequiredMixin,ListView):
    model=Profile
    template_name="Profiles/profile_list.html"
    context_object_name="qs"

    def get_queryset(self):
        qs=Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)
        context['profile']=profile
        #rel_r we are the sender
        rel_r=Relationship.objects.filter(sender=profile)
        #rel_s we are the receiver
        rel_s=Relationship.objects.filter(receiver=profile)
        rel_receiver=[]
        rel_sender=[]
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"]=rel_receiver
        context["rel_sender"]=rel_sender
        context["is_empty"]=False
        if len(self.get_queryset()) == 0:
            context["is_empty"] = True
        return context
@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)

        rel=Relationship.objects.create(sender=sender,receiver=receiver,status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')
@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)

        rel=Relationship.objects.filter((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
                                     )
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')