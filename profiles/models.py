from django.db import models
from accounts.models import CustomUser
from django.db.models import Q, F



class ProfessionalProfile(models.Model):

    PROFESSIONAL_TYPE_CHOICES = [
        ('developer', 'Developer'),
        ('designer', 'Designer'),
    ]
    # SENIORITY_CHOICES = [
    #     ('junior', 'Junior'),
    #     ('mid', 'Mid-Level'),
    #     ('senior', 'Senior'),
    #     ('lead', 'Lead'),
    # ]
    AVAILABILITY_CHOICES = [
        ('actively_looking', 'Actively Looking'),
        ('open_to_opportunities', 'Open to Opportunities'),
        ('not_looking', 'Not Looking'),
    ]
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]

    # User relationship
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='professional_profile'
    )
    headline = models.CharField(
        max_length=150,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    resume_uploaded_at = models.DateTimeField(
        null=True,
        blank=True
    )
    avatar = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    location_country = models.CharField(
        max_length=100,
        blank=True
    )

    location_city = models.CharField(
        max_length=100,
        blank=True
    )

    # Professional information
    professional_type = models.CharField(
        max_length=50,
        choices=PROFESSIONAL_TYPE_CHOICES,
        blank=True,
        db_index=True
    )

    availability_status = models.CharField(
        max_length=30,
        choices=AVAILABILITY_CHOICES,
        blank=True,
        db_index=True
    )

    employment_type_preference = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        blank=True
    )

    # System / calculated fields
    profile_completeness = models.PositiveIntegerField(
        default=0
    )

    trust_score = models.PositiveIntegerField(
        default=0
    )

    is_public = models.BooleanField(
        default=False
    )

    last_active_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        full_name= f"{self.user.first_name} { self.user.last_name}".strip()
        return full_name or self.user.email


# **************************************************************************#
class WorkExperience(models.Model):

    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='work_experiences'
    )

    job_title = models.CharField(
        max_length=100
    )

    company_name = models.CharField(
        max_length=150
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    currently_working = models.BooleanField(
        default=False
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        ordering = ['-start_date']
        constraints=[
            models.CheckConstraint(
                condition=Q(end_date__isnull=True) | Q(end_date__gte=F('start_date')),
                name='work_end_after_start',
            )
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


# **************************************************************************#
class Education(models.Model):

    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='educations'
    )

    institution_name = models.CharField(
        max_length=150
    )

    degree = models.CharField(
        max_length=150
    )

    field_of_study = models.CharField(
        max_length=150,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    currently_studying = models.BooleanField(
        default=False
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        ordering=['-end_date','-start_date']


    def __str__(self):
        return f"{self.degree} - {self.institution_name}"


# **************************************************************************#
class Skill(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )
    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name


# **************************************************************************#
class CandidateSkill(models.Model):
    
    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='candidate_skills'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name='candidate_profiles'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'skill'],
                name='unique_profile_skill'
            )
        ]

    def __str__(self):
        return f"{self.profile} - {self.skill}"


# **************************************************************************#
class Project(models.Model):

    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    project_url = models.URLField(
        blank=True
    )

    github_url = models.URLField(
            blank=True
        )
    technologies=models.CharField(
        blank=True
    )

    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

# **************************************************************************#
class Certification(models.Model):

    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='certifications'
    )

    name = models.CharField(
        max_length=200
    )

    issuing_organization = models.CharField(
        max_length=200
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    credential_url = models.URLField(
        blank=True
    )

    certificate_file = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        ordering = ['-issue_date', '-created_at']

    def __str__(self):
        return self.name



# **************************************************************************#
class ProfileLink(models.Model):

    LINK_TYPE_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('portfolio', 'Portfolio'),
        ('behance', 'Behance'),
        ('dribbble', 'Dribbble'),
        ('other', 'Other'),
    ]

    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='profile_links'
    )

    link_type = models.CharField(
        max_length=20,
        choices=LINK_TYPE_CHOICES
    )

    url = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.profile} - {self.link_type}"


# **************************************************************************#
class ResumeAnalysis(models.Model):

    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='resume_analyses'
    )

    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='resume_analyses'
    )

    score = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    analysis_result = models.JSONField(
        default=dict,
        blank=True
    )

    analyzed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering=['-analyzed_at']
    def __str__(self):
        return f"{self.profile} - {self.job}"