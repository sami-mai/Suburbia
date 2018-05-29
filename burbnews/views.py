from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from burbnews.models import Topic, TopicMember
from . import models
from . import forms


User = get_user_model()


# @login_required(login_url='/accounts/login/')
# def home(request, id):
#     title = "Rider"
#     current_user = request.user
#     # profile = Rider_Profile.objects.get(name=current_user.id)
#     context = {"title": title, "current_user": current_user}  #, "profile": profile}
#
#     return render(request, 'index-rider.html', context)


class CreateTopic(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Topic


class SingleTopic(generic.DetailView):
    model = Topic


class ListTopics(generic.ListView):
    model = Topic


class JoinTopic(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("single_topic", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get("slug"))

        try:
            TopicMember.objects.create(user=self.request.user, topic=topic)

        except IntegrityError:
            messages.warning(self.request, ("Warning, already a member of {}".format(topic.name)))

        else:
            messages.success(self.request, "You are now a member of the {} topic.".format(topic.name))

        return super().get(request, *args, **kwargs)


class LeaveTopic(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("single_topic", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.TopicMember.objects.filter(
                user=self.request.user,
                topic__slug=self.kwargs.get("slug")
            ).get()

        except models.TopicMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this topic because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this topic."
            )
        return super().get(request, *args, **kwargs)


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "topic")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "burbnews/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "topic")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('topic', 'image', 'message')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "topic")
    success_url = reverse_lazy("all_posts")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
