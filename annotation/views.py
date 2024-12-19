from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
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
    images = project.images.filter(tagged=False).order_by('id')
    try:
        image = project.images.filter(tagged=False).order_by('id')[0].image.url
        print(image)
        total_images = images.count()
        index = 0
        print(index)
        context = {'project': project,
                    'image': image,
                    'index': index,
                    'total_images': total_images
                    }
        if request.headers.get('HX-Request'):  
            return render(request, 'project_detail.html',context)
        return render(request, 'project_detail.html',context)
    except Exception as e:
        print('index out of range')
        return redirect('complete.html')
        
    

def back(request, pk, index):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=pk)
        images = project.images.filter().order_by('id')
        try:
            image = images[index].image.url
        except Exception as e:
            image = images[0].image.url
            index = 0
            print(e)
        total_images = images.count()
        context = {
            'project': project,
            'index': index - 1,
            'image': image,
            'total_images': total_images,
        }
        if request.headers.get('HX-Request'):
            return render(request, 'project_detail.html', context)
            


def save_and_next(request, pk, index):
    if request.method == 'POST':
            label = request.POST.get('label')
            description = request.POST.get('description')
            project = get_object_or_404(Project, id=pk)
            images = project.images.filter(tagged=False).order_by('id')
            count = images.count()
            try:
                image = images[index]
                image.label = label
                image.note = description
                image.tagged = True
                image.save()
                image_url = images[index].image.url
                messages.add_message(request, messages.SUCCESS, 'Image Annotated')
            except Exception as e:
                if count == index:
                    project.completed = True
                    project.save()
                    return render(request, 'complete.html')
                # image_url = images[0].image.url
                print(e)
            total_images = images.count()
            context = {
                'project': project,
                'index': index + 1,
                'image': image_url,
                'total_images': total_images,
            }
            if request.headers.get('HX-Request'):
                return render(request, 'project_detail.html', context)
            
            
    