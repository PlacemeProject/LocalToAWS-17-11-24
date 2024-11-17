from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Candidates, JobApplications
from recruiters.models import Jobs,JobsLocationsMaps
from credentials.models import Users
from django.contrib.auth.decorators import login_required
from .forms import CandidatePersonalUpdateForm
from django.contrib import messages

def Home(request):
    try:
        jobs_titles = Jobs.objects.values_list('title', flat=True).distinct()
        context = {
            'jobs_titles': jobs_titles,
        }
        return render(request,'jobseeker/home.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
def Profile(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        if request.method == 'POST':
            form = CandidatePersonalUpdateForm(request.POST, instance=candidate)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your profile has been updated successfully.')
                return redirect('job_seeker:profile')
            else:
                print("Form errors:", form.errors)
                messages.error(request, 'Please correct the errors below.')
        else:
            # form = CandidateUpdateForm(instance=candidate)
            candidate = Candidates.objects.get(user=request.user)
            # doc = Documents.objects.filter(candidate=candidate.candidate_id).first()
            # if doc :
            #     print("doc found:")
            # else :
            #     print("doc not found")
            skills_list = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []
            context = {
                'candidate': candidate,
                'skills_list': skills_list,
                # 'doc':doc
            }
            return render(request,'jobseeker/profile.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
def CreateProfile(request):
    try:
        # Get the candidate object associated with the logged-in user
        candidate = Candidates.objects.get(user=request.user)
        
        # Handle the form submission
        if request.method == 'POST':
            form = CandidateUpdateForm(request.POST, instance=candidate)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('job_seeker:profile')
            else:
                print("Form errors:", form.errors)
                messages.error(request, 'Please correct the errors below.')
        else:
            form = CandidateUpdateForm(instance=candidate)
        
        # Try to get the Documents object; if it doesn't exist, set doc to None
        # doc = Documents.objects.filter(candidate=candidate.candidate_id).first()
        if doc :
            print("doc found:")
        else :
            print("doc not found")
        
        skills_list = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []

        context = {
            'form': form,
            'candidate': candidate,
            'skills_list': skills_list,
            # 'documents': doc,  # Pass the documents object to the template
        }

        return render(request, 'jobseeker/create-profile.html', context)
    
    except Candidates.DoesNotExist:
        return HttpResponse("Candidate profile does not exist.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


def Search(request):
    try:
        keyword1 = request.GET.get('q', '')
        keyword2 = request.GET.get('p', '')        
        page_number = request.GET.get('page', 1)
        # keyword='web'
        # page_number=1

        # Basic keyword search
        if keyword1 and keyword2:
            # jobs = Jobs.objects.filter(title__icontains=keyword1, location__icontains=keyword2)
            jobs = Jobs.objects.filter(
                title__icontains=keyword1,
                job_id__in=JobsLocationsMaps.objects.filter(
                    location_id__location__icontains=keyword2  # Filtering based on the location field
                ).values('job_id')
            )
            
            if not jobs.exists():
                jobs = Jobs.objects.filter(title__icontains=keyword1)
            # if not jobs.exists():
            #     context = {
            #         'search': 'Search your dream job'
            #     }
            #     return render(request, 'jobseeker/jobs.html', context)
            
        elif keyword1:
            jobs = Jobs.objects.filter(title__icontains=keyword1)
        else :
            context = {
                'search': 'Search your dream job'
           }
            return render(request, 'jobseeker/jobs.html', context)
        message = 'Search your dream job.'
        # Pagination
        paginator = Paginator(jobs, 10)  # Show 20 jobs per page
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'keyword1': keyword1,
            'keyword2': keyword2,
        }
        return render(request, 'jobseeker/jobs.html', context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def Job(request):
    try:
        job1 = request.GET.get('r', '')
        job = Jobs.objects.get(slug=job1)
        check_applied = JobApplications.objects.filter(candidate=Candidates.objects.get(user=request.user), job=job.job_id)
        applied = check_applied.exists()
        skills_list = [skill.strip() for skill in job.skills.split(',')] if job.skills else []
        context = {
            'job': job,
            'skills_list':skills_list,
            'applied': applied
        }
        return render(request,'jobseeker/job.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def MyJob(request):
    return HttpResponse("<h1>You applied jobs are shown here</h1>")

@login_required
def Apply(request):
    try:
        if request.method == 'POST':
            # slug = request.POST.get('slug') 
            applied_id = request.POST.get('id') 
            title = request.POST.get('title') 
            job = Jobs.objects.get(job_id=applied_id)
            candidate = Candidates.objects.get(user=request.user)
            # user_id = candidate.user_id
            JobApplications.objects.create(
                candidate=candidate,
                job=job
            )
            job = Jobs.objects.get(job_id=applied_id)
            job.increment_applied_count()
            messages.info(request, f'You have successfully applied to {title} job')
            return redirect('job_seeker:status')
        return redirect('job_seeker:home')

            # form = CandidatePersonalUpdateForm(request.POST, instance=candidate)
            # if form.is_valid():
            #     form.save()
            #     messages.info(request, 'Your profile has been updated successfully.')
            #     return redirect('job_seeker:job')
            # else:
            #     print("Form errors:", form.errors)
            #     messages.error(request, 'Please correct the errors below.')
            #     return redirect('job_seeker:job')

        # job1 = request.GET.get('r', '')
        # job = Jobs.objects.get(slug=job1)
        # skills_list = [skill.strip() for skill in job.skills.split(',')] if job.skills else []
        # context = {
        #     'job': job,
        #     'skills_list':skills_list
        # }
        # return render(request,'jobseeker/job.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def Status(request):
    try:
        jobs = JobApplications.objects.filter(candidate=Candidates.objects.get(user=request.user))
        context = {
            'jobs': jobs,
        }
        return render(request,'jobseeker/status.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


def Notifications(request):
    return HttpResponse("<h1>Notifications are With pop up window</h1>")
@login_required
def Onboarding(request):
    try:
        # job_applications = JobApplications.objects.filter(candidate=Candidates.objects.get(user=request.user))

        # # Retrieve job details for each application
        # jobs = Jobs.objects.filter(job__in=job_applications.values('job_id'))        
        context = {
            'jobs': True,
        }
        return render(request,'jobseeker/onboarding.html',context)
        return render(request,'jobseeker/onboarding.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)