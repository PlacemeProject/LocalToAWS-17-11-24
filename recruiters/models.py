from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
import hashlib
import datetime
from django.utils.text import slugify
from credentials.models import Users
# from job_seekers.model import Candidates

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

class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    candidate = models.OneToOneField('job_seekers.Candidates', on_delete=models.CASCADE, related_name='company_candidate', null=True, blank=True)
    company_name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True, null=True)
    official_email  = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    # verify email
    admin_name = models.CharField(max_length=255, blank=True, null=True)
    admin_role = models.CharField(max_length=255, blank=True, null=True)
    no_of_employees = models.PositiveIntegerField(blank=True, null=True)
    is_manufacturing_based = models.BooleanField(default=False)
    is_service_based = models.BooleanField(default=False)
    industry_type  = models.CharField(max_length=255, blank=True, null=True)
    organization_type  = models.CharField(max_length=100, choices=[
        ('private', 'Private'),
        ('public', 'Public'),
        ('government', 'Government'),
        ('non_profit', 'Non-Profit'),
    ], blank=True, null=True)
    website = models.URLField(max_length=255,blank=True, null=True)
    sub_users_limit = models.IntegerField(default=1)
    about = models.CharField(max_length=255, blank=True, null=True)
    is_company_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='recruiters_documents', null=True, blank=True)
    profile_picture = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    gst_doc = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    
    def __str__(self):
        return f'{self.candidate.user.email} - {self.profile_picture}'        


class Jobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    specification = models.TextField(null=True,blank=True)
    employment_type  = models.CharField(max_length=100, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('fixed-term', 'fixed-term'),
        ('Internship', 'Internship')

    ], blank=True, null=True)
    is_fixed_shift = models.BooleanField(default=False)
    is_rotational_shift = models.BooleanField(default=False)
    is_day_shift = models.BooleanField(default=False)
    is_night_shift = models.BooleanField(default=False)
    is_onsite = models.BooleanField(default=False)
    is_work_from_home = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    skills = models.TextField( null=True, blank=True)
    qualifications = models.TextField( null=True, blank=True)
    required_experience = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_date = models.DateTimeField(default=timezone.now)
    last_date_to_apply = models.DateTimeField(blank=True, null=True)
    opening_count = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(default=0)
    applied_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_post_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            company_slug = self.company.company_name
            # x
            base_slug = slugify(f"{self.title} {company_slug}")
            
            now = datetime.datetime.now() 
            timestamp = now.strftime("%Y%m%d%H%M%S%f")
            # timestamp = str(int(time.time()))
            # unique_string = f"{self.title}-{self.location}-{company_slug}-{timestamp}"
            unique_string = f"{self.title}-{company_slug}-{timestamp}"
            unique_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:8]
            
            slug = f"{base_slug}-{unique_hash}"
            
            while Jobs.objects.filter(slug=slug).exists():
                unique_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:8]
                slug = f"{slug}-{unique_hash}"
            
            self.slug = slug
        
        super(Jobs, self).save(*args, **kwargs)

    def increment_applied_count(self):
        self.applied_count += 1
        self.save()
        
    def days_since_posted(self):
        # Calculate the days between posted_date and now
        difference = timezone.now() - self.posted_date
        return difference.days

    def __str__(self):
        return self.title


class SubUserAccess(models.Model):
    subuser_access_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='subusers_company', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subuser_access', null=True, blank=True)
    can_post_jobs = models.BooleanField(default=False)
    can_edit_jobs = models.BooleanField(default=False)
    can_view_applicants = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.email} - {self.company.company_name} Access"


class Bookmarks(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='company_bookmars', null=True, blank=True)
    candidate = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='job_seekers_bookmarks', null=True, blank=True)
    job = models.ForeignKey('recruiters.Jobs', on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.email} bookmarked {self.job.title}"


class Commands(models.Model):
    command_id = models.AutoField(primary_key=True)
    issued_company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='command_from', null=True, blank=True)
    issued_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='command_by', null=True, blank=True) 
    issued_to = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='command_for', null=True, blank=True)
    job = models.ForeignKey('recruiters.Jobs', on_delete=models.CASCADE, related_name='command_in')
    command = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"Command issued by {self.issued_by.firstname} {self.issued_by.lastname}to {self.issued_to.user.email}"


class UserLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    sub_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='subusers_logs',blank=True, null=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


class JobTitle(models.Model):
    jobtitle_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# =====================================Location begin========================================================

class CountryForLoc(models.Model):
    country_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class StateForLoc(models.Model):
    state_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100)
    country = models.ForeignKey(CountryForLoc, related_name="states", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class DistrictForLoc(models.Model):
    district_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100)
    state = models.ForeignKey(StateForLoc, related_name="districts", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.state.name}, {self.state.country.name}"

class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    pincode = models.IntegerField(null=True, blank=True)
    district = models.ForeignKey(DistrictForLoc, related_name="locations", on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(Users, related_name='location_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.location}'

class JobsLocationsMaps(models.Model):
    jobs_location_id = models.AutoField(primary_key=True)
    job_id = models.ManyToManyField('recruiters.Jobs', related_name='job_map_jlm')
    location_id = models.ManyToManyField('recruiters.Locations', related_name='location_map_jlm')

    def __str__(self):
        jobs = ', '.join([job_id.slug for job_id in self.job_id.all()])
        return f'Jobs: {jobs}'

# =====================================Location End========================================================
# =====================================Benefits begin========================================================
class Benefits(models.Model):
    benefits_id = models.AutoField(primary_key=True)
    benefit = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    Created_by = models.ManyToManyField(Users, related_name='benefit_by')
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.benefit

class JobsBenefitsMaps(models.Model):
    jobs_benefits_id = models.AutoField(primary_key=True)
    job_id = models.ManyToManyField('recruiters.Jobs', related_name='job_map_jbm')
    benefit_id = models.ManyToManyField('recruiters.Benefits', related_name='benefit_map_jbm')

    def __str__(self):
        jobs = ', '.join([job_id.slug for job_id in self.job_id.all()])
        return f'Jobs: {jobs}'
# =====================================Benefits End========================================================
