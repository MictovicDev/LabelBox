from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, ProjectImage
import asyncio
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages

# Create your views here.


async def save_uploaded_file(project, file):
    """
    Save a single uploaded file asynchronously
    """
    try:
        image = await sync_to_async(ProjectImage.objects.create)(
            project=project,
            image = file
        )
        return {
            'status': 'success',
            'filename': file.name,
            'url': image.image.url
        }
    except Exception as e:
        # Handle error if something goes wrong with saving the image to the database
        print(f"Error saving image to database: {str(e)}")
        return {
            'status': 'failed',
            'filename': file.name,
            'error': str(e),
        }
        
async def create_project(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        name = request.POST.get('name')
        description = request.POST.get('description')
        files = request.FILES.getlist('images')

        # Create project using sync_to_async
        project = await sync_to_async(Project.objects.create)(
            owner=request.user,
            name=name,
            description=description
        )

        # Process images asynchronously
        tasks = [save_uploaded_file(project, file) for file in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print(results)

        return await sync_to_async(render)(request, 'project_item.html', {'project': project})


    except Exception as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    

def get_detail(request, pk):
    project = get_object_or_404(Project, pk=pk) 
    if request.headers.get('HX-Request'):  
        return render(request, 'project_detail.html', {'project': project})
    return render(request, 'project_detail.html', {'project': project})
    
    
    

