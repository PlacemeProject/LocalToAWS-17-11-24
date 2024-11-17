from django.db import models
from django.utils import timezone
from credentials.models import Users  # Import the custom Users model
# from .models import Candidates
from recruiters.models import Jobs  # Import the Jobs model from recruiters app
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def path_by_user_id(user_id: int):
    user_id_int = user_id + 100000000
    revchar = ''
    i=1
    while user_id_int>0:
        rem = user_id_int%10
        revchar += chr(rem+48)
        user_id_int //= 10
        if (i == 3 or i == 6):
            revchar += '/'
        i +=1       
    path = revchar[::-1] 
    return path



def validate_file_type(file):
    mime = magic.from_buffer(file.read(1024), mime=True)
    valid_mime_types = ['application/pdf', 'image/png', 'image/jpeg']    
    if mime not in valid_mime_types:
        raise ValidationError("Invalid file type.")
    file.seek(0)

def validate_file_size(file):
    max_size = 200 * 1024  # 200KB limit
    if file.size > max_size:
        raise ValidationError("File size must be under 200KB.")

def upload_profile_pic(instance, filename):
    user_path = path_by_user_id(instance.user.userid)    
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'UsersDF/{0}/personal/Profile_{1}'.format(user_path,filename)

def upload_profile_resume(instance, filename):
    user_path = path_by_user_id(instance.user.userid)
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'UsersDF/{0}/personal/Resume_{1}'.format(user_path,filename)

class Candidates(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='candidate', null=True, blank=True)
    
    # Personal Information
    fullname = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    work_status = models.CharField(max_length=15, choices=[('Fresher', 'Fresher'), ('Experienced', 'Experienced')], blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    linkedin_profile = models.URLField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married')], blank=True, null=True)
    profile_pic = models.ImageField(upload_to=upload_profile_pic, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    resume = models.FileField(upload_to=upload_profile_resume, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            validate_file_size
        ]
    )
    
    # Education Information
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    year_of_graduation = models.IntegerField(blank=True, null=True)
    university_name = models.CharField(max_length=255, blank=True, null=True)
    secondary_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    higher_secondary_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    diploma_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bachelors_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    masters_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    doctorate_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    
    # Work Experience
    present_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    present_take_home = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_take_home = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    other_yearly_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    monthly_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    skill = models.TextField(blank=True, null=True)
    present_designation = models.CharField(max_length=200, blank=True, null=True)
    work_experience = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notice_period = models.IntegerField(blank=True, null=True)
    is_rotate_shift = models.BooleanField(default=False)
    preferred_location = models.CharField(max_length=100, blank=True, null=True)
    is_relocate = models.BooleanField(default=False)
    professional_summary = models.TextField(blank=True, null=True)

    # Additional info
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    email_otp_count = models.IntegerField(default=3)
    phone_otp_count = models.IntegerField(default=3)
    bookmarks_count = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.fullname} ({self.user.email})'

# class Documents(models.Model):
#     document_id = models.AutoField(primary_key=True)
#     candidate = models.OneToOneField('Candidates', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
#     profile_picture = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
#     resume = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    
#     def __str__(self):
#         return f'{self.candidate.user.email} - {self.profile_picture}'

class Bookmarks(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='bookmarks', null=True, blank=True)
    # job_post_id = models.ForeignKey('Jobs', on_delete=models.CASCADE, related_name='jobs')    <=======================> uncommand <=-=-=-=-=-=-=--=-=-=-=->
    bookmarked_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.candidate.user.email} - {self.bookmarked_date}'

class OnbordingDocument(models.Model):
    Onbording_document_id = models.AutoField(primary_key=True)
    candidate = models.OneToOneField('Candidates', on_delete=models.CASCADE, related_name='onbording_documents', null=True, blank=True)
    # document_name = models.CharField(max_length=255)
    # document_file = models.FileField(upload_to='documents/', validators=[validate_file_type, validate_file_size])
    # uploaded_at = models.DateTimeField(auto_now_add=True)

    # Educational Documents
    photo = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    tenth_mark_sheet = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    twelfth_mark_sheet = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    diploma_certificate = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    Bachelors_degree = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    masters_degree = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    doctorate_degree = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])

    # Personal Documents
    aadhar_card = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    bank_book = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    experience = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])

    def __str__(self):
        return f'{self.candidate.user.email} - {self.aadhar_card}'



class JobApplications(models.Model):
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='candidate_form', null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='job_applications', null=True, blank=True)  
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('selected', 'Selected'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    ], default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(blank=True, null=True)    
    shortlisted_at = models.DateTimeField(blank=True, null=True)    
    selected_at = models.DateTimeField(blank=True, null=True)    
    offered_at = models.DateTimeField(blank=True, null=True)    
    accepted_at = models.DateTimeField(blank=True, null=True)    
    rejected_at = models.DateTimeField(blank=True, null=True)    
    hired_at = models.DateTimeField(blank=True, null=True)    
    
    def __str__(self):
        return f'{self.candidate.user.email} - {self.status}'

class AdditionalInfo(models.Model):
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='candidate_info', null=True, blank=True)
    # job_post_info = models.ForeignKey('Jobs', on_delete=models.CASCADE, related_name='job_post_info')      <=======================> uncommand <=-=-=-=-=-=-=--=-=-=-=->
    post = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='postinfo', null=True, blank=True)   
    info_name = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.candidate.user.email} - {self.info_name}'

# =====================================Skills begin========================================================

class DomainForSkill(models.Model):
    domain_id = models.AutoField(primary_key=True)     
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)     
    domain = models.ForeignKey(DomainForSkill, related_name="skills", on_delete=models.CASCADE)
    skill = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.skill} ({self.domain.name})"

# =====================================Skills End========================================================
# =====================================Education begin========================================================

class LevelForEdu(models.Model):
    level_id = models.AutoField(primary_key=True)     
    name = models.CharField(max_length=50, unique=True)  # Example: "Undergraduate" or "Postgraduate"
    code = models.CharField(max_length=10, unique=True)  # Example: "UB" or "PB"

    def __str__(self):
        return self.name

class CourseForEdu(models.Model):
    course_id = models.AutoField(primary_key=True)
    level = models.ForeignKey(LevelForEdu, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)  # Example: "Bachelor of Technology"

    def __str__(self):
        return f"{self.name} ({self.level.code})"

class SpecificationForEdu(models.Model):
    specification_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(CourseForEdu, related_name="specialities", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Example: "Computer Science and Engineering", "Information Technology"

    def __str__(self):
        return f"{self.name} - {self.course.name}"

class EducationType(models.Model):
    edu_type_id = models.AutoField(primary_key=True)
    edu_type = models.CharField(max_length=50)  # Example: "Full-time" or "Part-time"

    def __str__(self):
        return f"{self.edu_type}"

# =====================================Education End========================================================