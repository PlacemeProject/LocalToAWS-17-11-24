from django.contrib import admin
from .models import *

admin.site.register(Candidates)
admin.site.register(Bookmarks)
admin.site.register(OnbordingDocument)
admin.site.register(JobApplications)
admin.site.register(AdditionalInfo)
admin.site.register(DomainForSkill)
admin.site.register(Skills)
admin.site.register(LevelForEdu)
admin.site.register(CourseForEdu)
admin.site.register(SpecificationForEdu)
admin.site.register(EducationType)