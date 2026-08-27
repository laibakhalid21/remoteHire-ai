from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ProfessionalProfile, WorkExperience, Education, CandidateSkill, Project, Certification,ProfileLink, Skill
from .serializers import ProfessionalProfileSerializer, WorkExperienceSerializer, EducationSerializer, CandidateSkillSerializer, ProjectSerializer, CertificationSerializer, ProfileLinkSerializer, SkillSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView,ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser,  JSONParser
from accounts.permissions import IsProfessional

@receiver(post_save, sender=CustomUser)
def create_professional_profile(sender, instance, created, **kwargs):
    if created and instance.role=='professional':
        ProfessionalProfile.objects.create(user=instance)

#**************************ProfessionalProfile*********************************************

#APIVIEW manual list
# class ProfessionalProfileView(APIView):
#     permission_classes=[IsProfessional]
#     parser_classes=[
#         MultiPartParser,
#         FormParser
#     ]

    # def get_object(self, pk):
    #     return get_object_or_404(
    #         ProfessionalProfile,
    #         pk=pk,
    #         user=self.request.user
    #     )

# #get profile (data read)
#     def get(self,request,pk):
#         profile=self.get_object(pk)
#         serializer=ProfessionalProfileSerializer(profile)

#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# #update the existing profile with profile fields
#     def patch(self,request):
            #not pk at all, can be same as get apiview
            #/api/profile/me and get access to objects using 
#         profile=ProfessionalProfile.objects.get(user=request.user)
#         serializer=ProfessionalProfileSerializer(profile, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#extra 
    # def post(self,request):
    #     serializer=ProfessionalProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

#advance less code generic view
#GET?PATCH
class ProfessionalProfileView(RetrieveUpdateAPIView):
    serializer_class=ProfessionalProfileSerializer
    permission_classes=[IsProfessional]
    parser_classes=[
        MultiPartParser,
        JSONParser,
    ]

#Authorization protects writeablefields
#readable already protected frontend cant chnage ownership 
    #url api/profile/me demand id be default
    def get_object(self):
        return self.request.user.professional_profile

    #url api/profile/8 safe
    # def get_queryset(self):
    #     return ProfessionalProfile.objects.filter(user=self.request.user)


    #url api/profile/8
    # def get_object(self):
    #     return get_object_or_404(
    #         ProfessionalProfile,
    #         id=self.kwargs['pk'],
    #         user=self.request.user
    #     )


#**************************EXPERIENCE*********************************************

#APIVIEW Detail
# class WorkExperienceDetailView(APIView):
#     permission_classes=[IsProfessional]

# #2nd way of filteration from id 
#     def get_queryset(self):
#         return WorkExperience.objects.filter(profile__user=self.request.user)
    
#     def get_object(self, request, pk):
#         return get_object_or_404(
#            self.get_queryset(),
#             pk=pk,
#         )

#     def get(self,request,pk):
#         experience = self.get_object(request, pk)

#         serializer = WorkExperienceSerializer(experience)

#         return Response(serializer.data, status=status.HTTP_200_OK)
        

#     def patch(self, request, pk):

#         experience = self.get_object(request, pk)
#         serializer = WorkExperienceSerializer(
#             experience,
#             data=request.data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, pk):

#         experience = self.get_object(request, pk)
#         experience.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )



#listcreate apiview
# class WorkExperienceListCreateView(APIView):
#     permission_classes=[IsProfessional]

#     def get_queryset(self):
#         return WorkExperience.objects.filter(profile__user=self.request.user)

#     def get(self,request):
#         experiences=self.get_queryset()
#         serializer=WorkExperienceSerializer(
#             experiences, many=True
#         )
#         return Response(serializer.data)



#     def post(self, request):
#         serializer = WorkExperienceSerializer(data=request.data)
#         if serializer.is_valid():
#             profile = request.user.professional_profile
#             serializer.save(profile=profile)

#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST)




#generic view
class WorkExperienceListCreateView(ListCreateAPIView):

    serializer_class = WorkExperienceSerializer
    permission_classes = [IsProfessional]

    # bcz this return multiple objects of logged in user
    def get_queryset(self):
        return WorkExperience.objects.filter(
            profile__user=self.request.user
        )

    #create
    def perform_create(self, serializer):
        #get professionalProfile object and save it
        profile = self.request.user.professional_profile
        serializer.save(profile=profile) #can use id but expect object internally use id
        #assign owner



class WorkExperienceDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsProfessional]

#with url id  safe
    def get_queryset(self):
        return WorkExperience.objects.filter(
            profile__user=self.request.user
        )
    #inside workexperinece profile
    #that profile relate to professioanlprofile
    #and inside professionalProfile have user
    #equals to currently logged in user




#**************************EDUCATION******************************************

#Manual apiview same as workexpeirnece
#GENERIC
class EducationListCreateView(ListCreateAPIView):

    serializer_class = EducationSerializer
    permission_classes = [IsProfessional]

    def get_queryset(self):
        return Education.objects.filter(
            profile__user=self.request.user
        )

    #create
    def perform_create(self, serializer):
        profile = self.request.user.professional_profile
        serializer.save(profile=profile) 



class EducationDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    permission_classes = [IsProfessional]

#with url id  safe
    def get_queryset(self):
        return Education.objects.filter(
            profile__user=self.request.user
        )




#**********************************SKILLS***********************************
#Manual apiview same as workexpeirnece

# class SkillListView(ListAPIView):
#     queryset = Skill.objects.all()
#     serializer_class = SkillSerializer
#     permission_classes = [IsProfessional]



class CandidateSkillListCreateView(ListCreateAPIView):

    serializer_class = CandidateSkillSerializer
    permission_classes = [IsProfessional]

    def get_queryset(self):
        return CandidateSkill.objects.filter(
            profile__user=self.request.user
        )
    def perform_create(self, serializer):
        profile = self.request.user.professional_profile
        serializer.save(profile=profile)



class CandidateSkillDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = CandidateSkillSerializer
    permission_classes = [IsProfessional]

    def get_queryset(self):
        return CandidateSkill.objects.filter(
            profile__user=self.request.user
        )
    # http_method_names = ['get', 'patch', 'delete']



#************************************Projects************************************

class ProjectListCreateView(ListCreateAPIView):

    serializer_class = ProjectSerializer
    permission_classes = [IsProfessional]
    parser_classes=[
        MultiPartParser,
        JSONParser
    ]


    def get_queryset(self):
        return Project.objects.filter(
            profile__user=self.request.user
        )
    def perform_create(self, serializer):
        profile = self.request.user.professional_profile
        serializer.save(profile=profile)



class ProjectDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ProjectSerializer
    permission_classes = [IsProfessional]
    http_method_names = ['get', 'patch', 'delete']
    parser_classes=[
        MultiPartParser,
        JSONParser
    ]

    def get_queryset(self):
        return Project.objects.filter(
            profile__user=self.request.user
        )

    
#*******************************Certificates************************************

class CertificationListCreateView(ListCreateAPIView):

    serializer_class = CertificationSerializer
    permission_classes = [IsProfessional]
    parser_classes=[
        MultiPartParser,
        JSONParser
    ]

    def get_queryset(self):
        return Certification.objects.filter(
            profile__user=self.request.user
        )
    def perform_create(self, serializer):
        profile = self.request.user.professional_profile
        serializer.save(profile=profile)




class CertificationDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = CertificationSerializer
    permission_classes = [IsProfessional]
    #default it handles get put patch delete and here we restrict
    http_method_names = [
        'get',
        'patch',
        'delete'
    ]
    parser_classes=[
        MultiPartParser,
        JSONParser
    ]


    def get_queryset(self):
        return Certification.objects.filter(
            profile__user=self.request.user
        )

    
#************************************LINKS*****************************
class ProfileLinkListCreateView(ListCreateAPIView):

    serializer_class = ProfileLinkSerializer
    permission_classes = [IsProfessional]

    def get_queryset(self):
        return ProfileLink.objects.filter(
            profile__user=self.request.user
        )
    def perform_create(self, serializer):
        profile = self.request.user.professional_profile
        serializer.save(profile=profile)



class ProfileLinkDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ProfileLinkSerializer
    permission_classes = [IsProfessional]

    http_method_names = [
        'get',
        'patch',
        'delete'
    ]
    def get_queryset(self):
        return ProfileLink.objects.filter(
            profile__user=self.request.user
        )