# register/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Intern, Assessment, AssessmentMarks
import os
import re


class InternForm(forms.ModelForm):
   
    
    class Meta:
        model = Intern
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-md'}),
            'contact': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'max': '2005-12-31', 'class': 'form-control rounded-md'}),
            'gender': forms.Select(attrs={'class': 'form-control rounded-md'}),
            'qualification': forms.Select(attrs={'class': 'form-control rounded-md'}),
            'year': forms.Select(attrs={'class': 'form-control rounded-md'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'internship_type': forms.Select(attrs={'class': 'form-control rounded-md'}),
            'area_of_interest': forms.Select(attrs={'class': 'form-control rounded-md'}),  
            'preferred_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control rounded-md'}),
            'prior_internship': forms.Select(
                choices=[('Yes', 'Yes'), ('No', 'No')],
                attrs={'class': 'form-control rounded-md'}
            ),
            'linkedin': forms.URLInput(attrs={'class': 'form-control rounded-md'}),
            'heard_from': forms.Select(attrs={'class': 'form-control rounded-md'}),
            'bonafide': forms.ClearableFileInput(attrs={'class': 'form-control-file border p-2 rounded-md'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file border p-2 rounded-md'}),
            'address': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
            'past_internship_details': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
            'skills': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
            'project_duration': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'duration': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
        }

    
    def clean_bonafide(self):
        file = self.cleaned_data.get('bonafide')
        if file:
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in ['.pdf', '.doc', '.docx']:
                raise ValidationError("Only .pdf, .doc, and .docx files are allowed for Bonafide.")
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be under 5MB.")
        return file

    def clean_photo(self):
        image = self.cleaned_data.get('photo')
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError("Only .jpg, .jpeg, .png images are allowed for Photo.")
        return image

    def clean_linkedin(self):
        url = self.cleaned_data.get('linkedin')
        if url and not re.match(r'^https:\/\/(www\.)?linkedin\.com\/.*$', url):
            raise ValidationError("Enter a valid LinkedIn URL starting with https://linkedin.com/")
        return url



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Only Gmail addresses are allowed.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not re.match(r'^[6-9]\d{9}$', contact):
            raise ValidationError("Enter a valid 10-digit Indian mobile number starting with 6-9.")
        return contact

# --- Start of changes for AssessmentForm ---
class AssessmentForm(forms.ModelForm):
    trainee_name = forms.ModelChoiceField(
        queryset=Intern.objects.all().order_by('full_name'),
        label="Trainee Name",
        widget=forms.Select(attrs={'class': 'form-select rounded-md', 'id': 'trainee-name-select'})
    )
    domain = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control rounded-md', 'id': 'domain-field'})
    )

    class Meta:
        model = Assessment
        fields = [
            'trainee_name', 'domain', 'assessor_name', 'assessment_date', 'topics', 'assessment_number',
        ]
        widgets = {
            'assessor_name': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'assessment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control rounded-md'}),
            'topics': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
            'assessment_number': forms.Select(attrs={'class': 'form-select rounded-md'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        trainee = cleaned_data.get("trainee_name")
        domain = cleaned_data.get("domain")
        assessment_number = cleaned_data.get("assessment_number")

        if trainee and domain and assessment_number:
            exists = Assessment.objects.filter(
                trainee_name=trainee,
                domain=domain,
                assessment_number=assessment_number
            )

            # Exclude current object when editing
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)

            if exists.exists():
                raise ValidationError(
                    f"⚠ Assessment {assessment_number} already exists for {trainee} in {domain}. "
                    "You don’t need to fill this again."
                )

        return cleaned_data

# --- End of changes for AssessmentForm ---

class AssessmentMarksForm(forms.ModelForm):
    class Meta:
        model = AssessmentMarks
        fields = [
            'technical_skill', 'analytical_skills', 'troubleshooting',
            'verbal_communication', 'written_communication', 'collaboration',
            'time_management', 'work_ethic',
            'strengths', 'areas_of_improvement', 'remarks',
        ]
        widgets = {
            'technical_skill': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'analytical_skills': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'troubleshooting': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'verbal_communication': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'written_communication': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'collaboration': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'time_management': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'work_ethic': forms.NumberInput(attrs={'class': 'form-control rounded-md', 'min': 0, 'max': 5}),
            'strengths': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
            'areas_of_improvement': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
            'remarks': forms.Textarea(attrs={'class': 'form-control rounded-md', 'rows': 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        score_fields = [
            'technical_skill', 'analytical_skills', 'troubleshooting',
            'verbal_communication', 'written_communication', 'collaboration',
            'time_management', 'work_ethic'
        ]
        for field in score_fields:
            value = cleaned_data.get(field)
            if value is not None and not (0 <= value <= 5):
                self.add_error(field, "Score must be between 0 and 5.")
        return cleaned_data