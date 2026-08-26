from django.urls import path
from .views import ProfessionalProfileView
from .views import ProfessionalProfileView, WorkExperienceListCreateView, WorkExperienceDetailView, EducationListCreateView, EducationDetailView, CandidateSkillListCreateView, CandidateSkillDetailView, ProjectListCreateView,ProjectDetailView, CertificationListCreateView, CertificationDetailView, ProfileLinkDetailView, ProfileLinkListCreateView

urlpatterns=[
#ProfessionalProfile
    path( 'profile/', ProfessionalProfileView.as_view(), name='professional-profile' ),
#WorkExperience
    path( 'profile/experiences/', WorkExperienceListCreateView.as_view(), name='work-experience-list-create' ),
    path( 'profile/experiences/<int:pk>/', WorkExperienceDetailView.as_view(), name='work-experience-detail' ),
#Education
    path( 'profile/educations/', EducationListCreateView.as_view(), name='education-list-create' ), 
    path( 'profile/educations/<int:pk>/', EducationDetailView.as_view(), name='education-detail' ),
#SKILLS
    # path('skills/', SkillListView.as_view(), name='skill-list'),
#CandidateSKILL
    path( 'profile/skills/', CandidateSkillListCreateView.as_view(), name='candidate-skill-list-create' ), 
    path( 'profile/skills/<int:pk>/', CandidateSkillDetailView.as_view(), name='candidate-skill-detail' ),
#Projects
    path( 'profile/projects/', ProjectListCreateView.as_view(), name='project-list-create' ), 
    path( 'profile/projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail' ),
#Certificates
    path( 'profile/certifications/', CertificationListCreateView.as_view(), name='certification-list-create' ), 
    path( 'profile/certifications/<int:pk>/', CertificationDetailView.as_view(), name='certification-detail' ),
#ProfileLinks
    path( 'profile/links/', ProfileLinkListCreateView.as_view(), name='profile-link-list-create' ), 
    path( 'profile/links/<int:pk>/', ProfileLinkDetailView.as_view(), name='profile-link-detail' ),
]