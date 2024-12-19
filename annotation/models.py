from django.db import models
from authentication.models import User

# Create your models here.

class Project(models.Model):

    # categories = (
    #     ('Vehicle', 'Vehicle'),
    #     ('Person', 'Person')
    # )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This will order the projects by created_at in descending order by default
        ordering = ['-created_at']

    

    def __str__(self):
        return f"{self.name} Project"
    

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="files/project_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=500, blank=True, null=True)
    Note = models.TextField(blank=True, null=True)
    tagged = models.BooleanField(default=False)
    


    def __str__(self):
        return f"{self.image.url} Image"
    

