from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from . import models
from django.shortcuts import get_object_or_404


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description', 'grouptype')
    model = Group


class SingleGroup(generic.DetailView):
    model = Group


class ListGroup(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(
                self.request, 'Warning, already a member of {}'.format(group.name))
        else:
            messages.success(
                self.request, 'Now you are a member of the {} group'.format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user, group__slug=self.kwargs.get('slug')).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request, "You can't leave a group you aren't part of, moron.")
        else:
            membership.delete()
            messages.success(
                self.request, 'You have succesfully left this group')

        return super().get(request, *args, **kwargs)
