from rest_framework import serializers
from .models import ProfessionalProfile, WorkExperience, Education,Skill,CandidateSkill,Project,Certification,ProfileLink,ResumeAnalysis


class ProfessionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = [
            'id',
            'user',
            'headline',
            'bio',
            'resume',
            'resume_uploaded_at',
            'avatar',
            'location_country',
            'location_city',
            'professional_type',
            'availability_status',
            'employment_type_preference',
            'profile_completeness',
            'trust_score',
            'is_public',
            'last_active_at',
            'created_at',
            'updated_at',
        ]

    read_only_fields=[
        'id', 
        'user',
        'profile_completeness',
        'trust_score',
        'last_active_at',
        'created_at',
        'updated_at',
        'resume_uploaded_at'
    ]


class WorkExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkExperience

        fields = [
            'id',
            'profile',
            'job_title',
            'company_name',
            'start_date',
            'end_date',
            'currently_working',
            'description',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'created_at',
            'updated_at',
        ]


    def validate(self, attrs):
        start_date=attrs.get(
            'start_date',
            self.instance.start_date if self.instance else None)

        end_date = attrs.get(
            'end_date',
            self.instance.end_date if self.instance else None
        )

        currently_working = attrs.get(
            'currently_working',
            self.instance.currently_working if self.instance else False
        )

        if end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be before start date."
            )
        
        if currently_working and end_date:
            raise serializers.ValidationError(
                "Currently working experience cannot have an end date."
            )
        
        if not currently_working and not end_date:
            raise serializers.ValidationError(
                "End date is required when you are not currently working."
            )
        return attrs


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education

        fields = [
            'id',
            'profile',
            'institution_name',
            'degree',
            'field_of_study',
            'start_date',
            'end_date',
            'currently_studying',
            'description',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        start_date=attrs.get(
            'start_date',
            self.instance.start_date if self.instance else None)

        end_date = attrs.get(
            'end_date',
            self.instance.end_date if self.instance else None
        )

        currently_studying = attrs.get(
            'currently_working',
            self.instance.currently_studying if self.instance else False
        )

        if end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be before start date."
            )
        
        if currently_studying and end_date:
            raise serializers.ValidationError(
                "Currently studying cannot have an end date."
            )
        
        if not currently_studying and not end_date:
            raise serializers.ValidationError(
                "End date is required when you are not currently studying."
            )
        return attrs





class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill

        fields = [
            'id',
            'name',
        ]

        read_only_fields = [
            'id',
        ]


class CandidateSkillSerializer(serializers.ModelSerializer):
    skill_name=serializers.CharField(
        source='skill.name',
        read_only=True
    )
    class Meta:
        model = CandidateSkill

        fields = [
            'id',
            'profile',
            'skill',
            'skill_name',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'skill_name',
            'created_at',
        ]


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project

        fields = [
            'id',
            'profile',
            'title',
            'description',
            'project_url',
            'github_url',
            'technologies',
            'image',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'created_at',
        ]


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification

        fields = [
            'id',
            'profile',
            'name',
            'issuing_organization',
            'issue_date',
            'credential_url',
            'certificate_file',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'created_at',
        ]


class ProfileLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileLink

        fields = [
            'id',
            'profile',
            'link_type',
            'url',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'created_at',
            'updated_at',
        ]


class ResumeAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResumeAnalysis

        fields = [
            'id',
            'profile',
            'job',
            'score',
            'analysis_result',
            'analyzed_at',
        ]

        read_only_fields = [
            'id',
            'profile',
            'score',
            'analysis_result',
            'analyzed_at',
        ]