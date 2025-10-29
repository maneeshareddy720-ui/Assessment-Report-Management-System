# register/models.py
from django.db import models
import uuid

class Intern(models.Model):
    # Django will automatically create 'id' as an integer primary key.
    
    # Dropdown/choice fields
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    QUALIFICATIONS = [
        ('', 'Select Qualification'),
        ('B.Tech', 'B.Tech'),
        ('MBA', 'MBA'),
        ('Other', 'Other')
    ]
    YEAR_CHOICES = [('', 'Select')] + [(str(i), str(i)) for i in range(1, 5)]
    INTEREST_AREAS = [
        ('', 'Select'),
        ('Web Development', 'Web Development'),
        ('Mobile App Development', 'Mobile App Development'),
        ('Data Science', 'Data Science'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Python', 'Python'),
        ('Full Stack', 'Full Stack'),
        ('DevOps', 'DevOps'),
        ('Networking', 'Networking'),
        ('Linux', 'Linux'),
        ('.NET', '.NET'),
        ('MEAN', 'MEAN'),
        ('MERN', 'MERN'),
        ('PHP', 'PHP'),
        ('Laravel', 'Laravel'),
        ('Drupal', 'Drupal'),
        ('Finance', 'Finance'),
        ('HR', 'HR'),
        ('Digital Marketing', 'Digital Marketing'),
        ('Business Analyst', 'Business Analyst'),
        ('Sales Analyst', 'Sales Analyst'),
        ('Administration', 'Administration')
    ]
    INTERNSHIP_TYPES = [
        ('', 'Select'),
        ('Offline', 'Offline'),
        ('Online', 'Online'),
        ('Hybrid', 'Hybrid')
    ]
    HEARD_FROM_OPTIONS = [
        ('', 'Select'),
        ('BG Employee', 'BG Employee'),
        ('From Google Reviews', 'From Google Reviews'),
        ('Friends', 'Friends'),
        ('Through Social Media', 'Through Social Media'),
        ('Relation', 'Relation'),
        ('Existing Employees', 'Existing Employees')
    ]

    # --- Section 1: Personal Details ---
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    address = models.TextField()
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # --- Section 2: Educational Background ---
    qualification = models.CharField(max_length=50, choices=QUALIFICATIONS)
    college_name = models.CharField(max_length=100)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES)
    specialization = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)

    # --- Section 3: Internship Details ---
    area_of_interest = models.CharField(max_length=100, choices=INTEREST_AREAS)
    preferred_start_date = models.DateField()
    duration = models.CharField(max_length=50)
    project_duration = models.CharField(max_length=50, blank=True)
    prior_internship = models.CharField(
        max_length=10,
        choices=[('', 'Select'), ('Yes', 'Yes'), ('No', 'No')]
    )
    past_internship_details = models.TextField(blank=True)
    internship_type = models.CharField(max_length=10, choices=INTERNSHIP_TYPES)

    # --- Section 4: Additional Information ---
    skills = models.TextField(blank=True)
    bonafide = models.FileField(upload_to='bonafide/')
    linkedin = models.URLField()
    heard_from = models.CharField(max_length=50, choices=HEARD_FROM_OPTIONS, blank=True)

    def __str__(self):
       return f"{self.full_name} ({self.area_of_interest}) - {self.email}"



class Assessment(models.Model):
    ASSESSMENT_CHOICES = [
        (1, "Assessment 1"),
        (2, "Assessment 2"),
        (3, "Assessment 3"),
    ]
    MAX_MARKS = 40  # ✅ Each assessment = 40 marks

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trainee_name = models.ForeignKey(
        "Intern",
        on_delete=models.CASCADE,
        related_name="assessments"
    )
    domain = models.CharField(max_length=100, choices=Intern.INTEREST_AREAS)  # you can use Intern.INTEREST_AREAS
    assessor_name = models.CharField(max_length=100)
    assessment_date = models.DateField()
    topics = models.TextField()
    assessment_number = models.IntegerField(choices=ASSESSMENT_CHOICES)
    total_marks = models.IntegerField(default=0, null=True, editable=False)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def update_total_marks(self):
        """
        Recalculate total marks and percentage for this assessment.
        """
        # Sum all marks given in AssessmentMarks
        total = self.marks.aggregate(total=models.Sum("total_marks"))["total"] or 0
        self.total_marks = total

        # Percentage out of 40 (MAX_MARKS)
        self.percentage = (total / self.MAX_MARKS) * 100 if self.MAX_MARKS else 0

        self.save(update_fields=["total_marks", "percentage"])

    def __str__(self):
        return f"{self.trainee_name.full_name} - {self.domain} - A{self.assessment_number}"


class AssessmentMarks(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="marks"
    )
    technical_skill = models.PositiveSmallIntegerField(default=0)
    analytical_skills = models.PositiveSmallIntegerField(default=0)
    troubleshooting = models.PositiveSmallIntegerField(default=0)
    verbal_communication = models.PositiveSmallIntegerField(default=0)
    written_communication = models.PositiveSmallIntegerField(default=0)
    collaboration = models.PositiveSmallIntegerField(default=0)
    time_management = models.PositiveSmallIntegerField(default=0)
    work_ethic = models.PositiveSmallIntegerField(default=0)

    total_marks = models.IntegerField(default=0, editable=False)
    strengths = models.TextField(blank=True, null=True)
    areas_of_improvement = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Automatically calculate total marks (sum of all fields).
        Then update the parent Assessment totals.
        """
        self.total_marks = (
            self.technical_skill +
            self.analytical_skills +
            self.troubleshooting +
            self.verbal_communication +
            self.written_communication +
            self.collaboration +
            self.time_management +
            self.work_ethic
        )

        super().save(*args, **kwargs)

        # Update parent assessment totals
        self.assessment.update_total_marks()

    def __str__(self):
        return f"{self.assessment.trainee_name.full_name} - Assessment {self.assessment.assessment_number}"
