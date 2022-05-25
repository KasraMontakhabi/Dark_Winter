from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from . import models
from groups.models import Group, GroupMember

# Create your views here.

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug = self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user = self.request.user, group = group)
        except:
            messages.warning(self.request, "Already a member, brother...")
        else:
            messages.success(self.request, "Welcome to the club, brother...")
        
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(user = self.request.user, group__slug = self.kwargs.get("slug")).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, "You are not in this group brother ...")
        
        else:
            membership.delete()
            messages.success(self.request, "See you soon, brother... Horns UP...")
        return super().get(request, *args, **kwargs)
