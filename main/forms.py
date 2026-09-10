from django import forms
from .models import ContactProfile
from .models import UserProfile


class ContactForm(forms.ModelForm):

	name = forms.CharField(max_length=100, required=True,
		widget=forms.TextInput(attrs={
			'placeholder': '*Full name..',
			}))
	email = forms.EmailField(max_length=254, required=True, 
		widget=forms.TextInput(attrs={
			'placeholder': '*Email..',
			}))
	message = forms.CharField(max_length=1000, required=True, 
		widget=forms.Textarea(attrs={
			'placeholder': '*Message..',
			'rows': 6,
			}))


	class Meta:
		model = ContactProfile
		fields = ('name', 'email', 'message',)


class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('avatar', 'title', 'bio', 'cv')
		widgets = {
			'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
			'bio': forms.Textarea(attrs={'rows': 4}),
		}

	def clean_avatar(self):
		avatar = self.cleaned_data.get('avatar')
		if avatar:
			# limit to 5 MB
			max_size = 5 * 1024 * 1024
			if avatar.size > max_size:
				raise forms.ValidationError('Avatar file size must be under 5 MB')
			# basic content-type check (may not be present for some storage backends)
			content_type = getattr(avatar, 'content_type', '')
			if content_type and not content_type.startswith('image'):
				raise forms.ValidationError('Uploaded file is not an image')
		return avatar

	def clean_cv(self):
		cv = self.cleaned_data.get('cv')
		if cv:
			max_size = 10 * 1024 * 1024
			if cv.size > max_size:
				raise forms.ValidationError('CV file size must be under 10 MB')
		return cv


