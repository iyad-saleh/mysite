from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Carousel, Featuretts , Marketing ,Ticker

from django.urls import reverse ,reverse_lazy
from .forms import CarouselCreateForm, FeaturettsCreateForm, MarketingCreateForm 

# def login(request):
#     if request.method == 'POST':
#         form = UserloginForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'New account has been created! He is now able to log in')
#             return redirect('User_ListView')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

def home(request):
     
    context = {
        'carousel': Carousel.objects.all(),
        'Featuretts': Featuretts.objects.all(),
        'marketing': Marketing.objects.all(),
        'ticker': Ticker.objects.all(),
        

    }
    return render(request, 'blog/home.html', context)
 
#     Carousel                      

class CarouselCreateView(LoginRequiredMixin, CreateView):
    model = Carousel
    # fields = ['title', 'content','image','is_active']
    success_url = reverse_lazy('homeblog')
    form_class = CarouselCreateForm


    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)


class CarouselUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Carousel
    form_class = CarouselCreateForm
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)

    def test_func(self):
        carousel = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


class CarouselDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Carousel
    success_url = reverse_lazy('homeblog')

    def test_func(self):
        carousel = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


#     Featuretts
class FeaturettsCreateView(LoginRequiredMixin, CreateView):
    model = Featuretts
    # fields = ['title', 'content','image','is_active']
    form_class = FeaturettsCreateForm
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)


class FeaturettsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Featuretts
    # fields = ['title', 'content','image','is_active']
    form_class = FeaturettsCreateForm
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)

    def test_func(self):
        featuretts = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


class FeaturettsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Featuretts
    success_url = reverse_lazy('homeblog')

    def test_func(self):
        featuretts = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False



#            Marketing
class MarketingCreateView(LoginRequiredMixin, CreateView):
    model = Marketing
    # fields = ['title', 'content','image','is_active']
    form_class = MarketingCreateForm
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)


class MarketingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Marketing
    # fields = ['title', 'content','image','is_active']
    form_class = MarketingCreateForm
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)

    def test_func(self):
        marketing = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


class MarketingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Marketing
    success_url = reverse_lazy('homeblog')

    def test_func(self):
        marketing = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

class TickerCreateView(LoginRequiredMixin, CreateView):
    model = Ticker
    fields = ['title' ]
    # form_class = TickerCreateForm
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
         
        if self.request.user.is_superuser:
            return super().form_valid(form)


class TickerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticker
    fields = ['title' ]
  
    success_url = reverse_lazy('homeblog')
    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)

    def test_func(self):
        ticker = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


class TickerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticker
    success_url = reverse_lazy('homeblog')

    def test_func(self):
        ticker = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

