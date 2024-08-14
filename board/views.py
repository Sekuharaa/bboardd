from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import AdForm, CommentForm
from .filters import AdFilter
from django.conf import settings
class AdList(ListView):
    model = Ad
    ordering = '-created_at'
    template_name = 'ads.html'
    context_object_name = 'ads'

class AdDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'
    pk_url_kwarg = 'id'

class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'ad_create.html'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user
        return super().form_valid(form)

class AdEdit(LoginRequiredMixin, UpdateView):
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad_id = self.request.path[1::]
        context['ad_id'] = ad_id
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        ad_id = self.request.path[1::]
        comment.ad = Ad.objects.get(id=ad_id)
        comment.user = self.request.user
        comment.save()
        message = f"Поступил новый отклик на объявление {ad_id}"
        rec = comment.ad.user
        send_mail(
            subject='Новый отклик',
            message=message,
            from_email='settings.DEFAULT_FROM_EMAIL',
            recipient_list=[rec.email, ]
        )
        return super().form_valid(form)

class AcceptedCommentList(ListView):
    model = Comment
    template_name = 'comment_list.html'
    context_object_name = 'comments'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad_id = self.request.path[10::]
        queryset = Comment.objects.filter(status=True, ad_id=ad_id)
        length = queryset.count()
        context['length'] = length
        context['queryset'] = queryset
        context['ad_id'] = ad_id
        return context

class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')


def accept(request, id):
    Comment.objects.filter(id=id).update(status=True)
    comment = Comment.objects.get(id=id)
    rec = comment.user
    message = f"Ваш отклик на объявление {comment.ad.id} принят"
    send_mail(
        subject='Отклик принят',
        message=message,
        from_email='settings.DEFAULT_FROM_EMAIL',
        recipient_list=[rec.email, ]
    )

    return redirect('profile')

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'invalid_code.html')
        return redirect('account_login')

class ProfileView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'profile.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(ad__user__id=self.request.user.id)
        self.filterset = AdFilter(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context