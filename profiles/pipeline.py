from .models import UserProfile, Experience, Education

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'linkedin-oauth2':
        profile_url = response.get('publicProfileUrl')
        picture_url = response.get('pictureUrl')
        about = response.get('summary')
        
        # Create or update user profile
        profile, created = UserProfile.objects.get_or_create(user=user, linkedin_profile_url=profile_url)
        profile.picture_url = picture_url
        profile.about = about
        profile.save()

        # Example to save experiences, assuming response contains this data
        experiences = response.get('positions')
        if experiences:
            for exp in experiences['values']:
                Experience.objects.create(
                    user_profile=profile,
                    title=exp['title'],
                    company=exp['company']['name'],
                    start_date=exp['startDate'],
                    end_date=exp.get('endDate'),
                    description=exp.get('summary')
                )

        # Similarly for education
        educations = response.get('educations')
        if educations:
            for edu in educations['values']:
                Education.objects.create(
                    user_profile=profile,
                    school=edu['schoolName'],
                    degree=edu.get('degree'),
                    field_of_study=edu.get('fieldOfStudy'),
                    start_date=edu['startDate'],
                    end_date=edu.get('endDate')
                )
