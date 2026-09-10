from django.shortcuts import render
from django.contrib import messages
from .models import (
	    UserProfile,
		Blog,
		Portfolio,
		Testimonial,
		Certificate
	)

from django.views import generic


from . forms import ContactForm
from . forms import UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class IndexView(generic.TemplateView):
	template_name = "main/index.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		testimonials = Testimonial.objects.filter(is_active=True)
		certificates = Certificate.objects.filter(is_active=True)
		blogs = Blog.objects.filter(is_active=True)
		portfolio = Portfolio.objects.filter(is_active=True)
		
		context["testimonials"] = testimonials
		context["certificates"] = certificates
		context["blogs"] = blogs
		context["portfolio"] = portfolio
		return context


class ContactView(generic.FormView):
	template_name = "main/contact.html"
	form_class = ContactForm
	success_url = "/"
	
	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Thank you. We will be in touch soon.')
		return super().form_valid(form)


class PortfolioView(generic.ListView):
	model = Portfolio
	template_name = "main/portfolio.html"
	paginate_by = 10

	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)


class PortfolioDetailView(generic.DetailView):
	model = Portfolio
	template_name = "main/portfolio-detail.html"

class BlogView(generic.ListView):
	model = Blog
	template_name = "main/blog.html"
	paginate_by = 10
	
	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)


class BlogDetailView(generic.DetailView):
	model = Blog
	template_name = "main/blog-detail.html"


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = UserProfile
	form_class = UserProfileForm
	template_name = 'main/profile_form.html'

	def get_object(self, queryset=None):
		# return the profile for the current user
		return UserProfile.objects.get(user=self.request.user)

	def form_valid(self, form):
		form.save()
		return redirect('main:home')
