# register/admin.py
from django.contrib import admin
from .models import Intern, Assessment, AssessmentMarks

# Inline for AssessmentMarks to be used within the Assessment admin page
class AssessmentEntryInline(admin.TabularInline):
    model = AssessmentMarks
    extra = 0
    fields = [
        'technical_skill',
        'analytical_skills',
        'troubleshooting',
        'verbal_communication',
        'written_communication',
        'collaboration',
        'time_management',
        'work_ethic',
        'strengths',
        'areas_of_improvement',
        'total_marks',
        'remarks',
    ]
    readonly_fields = ['total_marks']

# Admin class for the Intern model
@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'contact',
        'qualification',
        'college_name',
        'get_area_of_interest',
        'preferred_start_date',
        'internship_type',
        'linkedin',
        'bonafide_document_display',
    )
    list_filter = ('gender', 'qualification', 'area_of_interest', 'internship_type', 'heard_from')
    search_fields = ('full_name', 'college_name', 'contact')

    def bonafide_document_display(self, obj):
        if obj.bonafide and hasattr(obj.bonafide, 'url'):
            return obj.bonafide.name
        return 'No File'
    bonafide_document_display.short_description = 'Bonafide'

    def get_area_of_interest(self, obj):
        if obj.area_of_interest:
            return obj.get_area_of_interest_display()
        return "-"
    get_area_of_interest.short_description = "Area of Interest"

    fieldsets = (
        ('1. Personal Details', {
            'fields': (
                ('full_name', 'dob'),
                ('gender', 'contact', 'email'),
                'address', 'photo'
            )
        }),
        ('2. Educational Background', {
            'fields': (
                ('qualification', 'college_name'),
                ('year', 'specialization', 'contact_person')
            )
        }),
        ('3. Internship Details', {
            'fields': (
                ('area_of_interest', 'preferred_start_date'),
                ('duration', 'project_duration'),
                ('prior_internship', 'past_internship_details'),
                'internship_type'
            )
        }),
        ('4. Additional Information', {
            'fields': (
                'skills', 'bonafide', 'linkedin', 'heard_from'
            )
        }),
    )

# Admin class for the Assessment model
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'trainee_name',
        'assessor_name',
        'assessment_number',
        'get_total_marks',
        'get_total_percentage',
        'created_at'
    ]
    search_fields = ['trainee_name__full_name', 'assessor_name']
    list_filter = ['assessor_name', 'assessment_number', 'created_at']
    inlines = [AssessmentEntryInline]
    readonly_fields = ['total_marks', 'percentage', 'created_at', 'modified_at']

    def get_total_marks(self, obj):
        return obj.total_marks
    get_total_marks.short_description = "Total Marks"
    get_total_marks.admin_order_field = 'total_marks'

    def get_total_percentage(self, obj):
        return f"{obj.percentage:.2f}%" if obj.percentage is not None else "0.00%"
    get_total_percentage.short_description = "Percentage"
    get_total_percentage.admin_order_field = 'percentage'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_total_marks()

# Admin class for the AssessmentMarks model
@admin.register(AssessmentMarks)
class AssessmentMarksAdmin(admin.ModelAdmin):
    list_display = [
        'get_student_name',
        'assessment_number',
        'technical_skill',
        'analytical_skills',
        'troubleshooting',
        'verbal_communication',
        'written_communication',
        'collaboration',
        'time_management',
        'work_ethic',
        'total_marks',
        'assessment_date',
        'total_marks'
    ]
    list_filter = ['assessment__assessment_number', 'assessment__assessor_name']
    search_fields = ['assessment__trainee_name__full_name', 'remarks']
    readonly_fields = ['total_marks', 'created_at', 'modified_at']
    autocomplete_fields = ['assessment']
    
    def get_student_name(self, obj):
        return obj.assessment.trainee_name.full_name
    get_student_name.short_description = 'Student'

    def assessment_number(self, obj):
        return obj.assessment.assessment_number
    assessment_number.short_description = 'Assessment No.'
    assessment_number.admin_order_field = 'assessment__assessment_number'

    def assessment_date(self, obj):
        return obj.assessment.assessment_date
    assessment_date.short_description = 'Assessment Date'
    assessment_date.admin_order_field = 'assessment__assessment_date'