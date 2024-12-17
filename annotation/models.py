from django.db import models
from authentication.models import User

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.name} Project"
    

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="files/project_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=500)
    Note = models.TextField()


    def __str__(self):
        return f"{self.project.name} Image"

