from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from levsdelight_app.models import Slideshow, MonthMap
import re, datetime, json, pprint, os, shutil, logging, base64
from django.views.decorators.csrf import csrf_exempt
from ImageUploader import ImageUploader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout


from levsdelight_app.models import Slideshow

# print "View Name: %s" % __name__
logger = logging.getLogger(__name__)

# Update the titles and descriptions of the slide objects.
def update(request):
    if request.method == 'POST':
        try:
            slide_list = json.loads(request.body)

            for s in slide_list:
                slideshow_obj = Slideshow.objects.get(pk=s['id'])
                slideshow_obj.title = s['title']
                slideshow_obj.desc = s['desc']
                slideshow_obj.save()

        except Exception as e:
            return HttpResponse('Error updating Slides: %s' % e)

        return HttpResponse('Slide Updated. Disco Party')

    else:
        return HttpResponse('Error Reordering Slides: unknown')

# Update the slides with ids in the list to the new order
# associated with that list.
def reorder(request):
    if request.method == 'POST':
        try:

            parsedList = json.loads(request.body)

            for s in parsedList:
                slideshow_obj = Slideshow.objects.get(pk=s['id'])
                slideshow_obj.order_id = s['newOrder']
                slideshow_obj.save()

        except Exception as e:
            return HttpResponse('Error Reordering Slides: %s' % e)

        return HttpResponse('Disco Party')
    else:
        return HttpResponse('Error Reordering Slides: unknown')

@csrf_exempt
def auth(request):
    if request.method == 'POST':

        auth_header = request.META['HTTP_AUTHORIZATION']
        base64_pass = auth_header.split(' ')[1] 
        user_pass = base64.b64decode(base64_pass).split(':')
        username = user_pass[0]
        password = user_pass[1]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'code': 0, 'status': 'active', 'user': user.username})
            else:
                return JsonResponse({'code': 0, 'status': 'inactive', 'user': user.username})
        else:
            return JsonResponse({'code': 2, 'status': 'incorrect_password', 'user': username})

    elif request.method == 'DELETE':
        logout(request)
        return HttpResponse('You have been logged out')

    elif request.method == 'GET':

        if request.user.is_authenticated():
            return JsonResponse({'user': request.user.get_username()})
        else:
            return JsonResponse({'user': 'anonymous'})

    else:
        return HttpResponse('What is your method')

def deploytest(request):

    logger.info('Deploy Test has been called - from git foo')

    return HttpResponse('This is a test of deploying')

# After receiving the images, process them by reducing
# the image quality and upload them to S3.
@csrf_exempt
def uploadimage(request):
    file_type_to_save = '-web'

    try:

        # print "The request"
        # print json.dumps(request)
        # pprint.pprint(request.__dict__)
        # print request.__dict__

        # print "the request:"
        # print request.POST

        theFile = request.FILES['farmFile']

        # Save the uploaded file to a temporary place on disk.
        # this_path = os.path.dirname(os.path.abspath(__file__))
        this_path = os.getcwd()
        
        # Create a temporary directory to store the files
        os.mkdir('tmp')
        # This can also be used `this_path = os.getcwd()`
        # for getting current working directory
        full_file_path = this_path + '/tmp/' + str(theFile)

        with open(full_file_path, 'wb+') as saved_tmp_file:
            for chunk in theFile.chunks():
                saved_tmp_file.write(chunk)
        
        # Upload the file to S3
        month_to_save_to = request.POST.get('folder_name', 'june2015')

        ic = ImageUploader(str(theFile), month_to_save_to)
        ic.connectToS3()
        ic.upload_original()
        ic.create_upload_web_image()
        ic.create_upload_thumbnail()


        # Remove the tmp directory and all the temp files
        try:
            shutil.rmtree(this_path + '/tmp')
        except OSError as e:
            logger.error('Unable to remove temp directory')
            logger.error(e)

    except Exception as e:
        logger.error('Error with upload request')
        logger.error(e)

        # Remove the tmp directory and all the temp files
        try:
            shutil.rmtree(this_path + '/tmp')
        except OSError as e:
            logger.error('Unable to remove temp direcotory')

        return JsonResponse({'message': e.message})

    try:

        # Create the 
        s_id = request.POST['slideshow_id']
        slideshow_folder = request.POST['picture_location']
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')

        create_date = request.POST['modified_date']

        # Create file type string
        split_file_string = slideshow_folder.split('.')
        concat_file_string = '%s%s.%s' % (
                split_file_string[0],
                file_type_to_save,
                split_file_string[1])

        picture_obj = Slideshow(
                title=title,
                desc=desc,
                pictureLocation=concat_file_string,
                isActive=True,
                slideshow_id=s_id,
                order_id=0,
                pub_date=create_date
                )

        picture_obj.save()

        
    except Exception as e:

        return JsonResponse({'message': e.message})

    # return HttpResponse("Hey, I appreciate the filez. \n\n %s" % (report))
    try:

        subject = 'L2 Pictures added to %s' % (month_to_save_to)
        from_email = 'jason@llamasontheloosefarm.com'
        to = 'jason.levinsohn@gmail.com'
        text_content = 'L3 Pictures Updated'
        formatted_message = """
            <b>Picture saved to %s</b>
        """ % (month_to_save_to)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(formatted_message, "text/html")
        msg.send()
    except Exception as e:
        return JsonResponse({'message': e.message})

    return HttpResponse('Thanks we got it')


def home(request):

    today = datetime.datetime.now()
    month = today.strftime('%B').lower()
    year = today.strftime('%Y')

    # newPath = 'slideshow/%s/%s' % (year, month)
    template = loader.get_template('base.html')
    context = RequestContext(request, {
            'month': month,
            'year': year
        })

    return HttpResponse(template.render(context))

def slideshow(request, year=None, month=None):

    # template = loader.get_template('slideshow.html')
    # context = RequestContext(request, {
    #         'month': month,
    #         'year': year
    #     })
    # return HttpResponse(template.render(context))

    result = {
            'month': month,
            'year': year
            }

    mapObject = MonthMap.objects.filter(month=month, year=year)
    map_id = mapObject[0].slideshow_id
    objects_returned = mapObject.count()
    print objects_returned
    if objects_returned > 1:

        return HttpResponse("ERROR: MonthMap returned more than one result")
    else:
        month_slides_query_set = Slideshow.objects.filter(slideshow_id=map_id)
        serialized_data = serializers.serialize('json', month_slides_query_set)

        # This allows us to bypass the cross-origin response problem when dealing with
        # not the quite same domain.  http://localhost:8000.
        response =  HttpResponse(serialized_data)
        response['Access-Control-Allow-Origin'] = '*'

        return response

def monthlist(request):

    month_maps = MonthMap.objects.all()

    logger.info('Month List Function called')

    serialized_map = serializers.serialize('json', month_maps)
    response = HttpResponse(json.dumps(serialized_map))
    response = HttpResponse(serialized_map)
    response['Access-Control-Allow-Origin'] = '*'


    return response

def allslides(request, limit=None):

    if (limit):
        all_slides = Slideshow.objects.all().order_by('-pub_date')[:limit]
        print 'Limiter'
    else:
        all_slides = Slideshow.objects.all().order_by('-pub_date');
        print 'No limit'

    serialized_slides = serializers.serialize('json', all_slides);

    response = HttpResponse(serialized_slides);
    response['Access-Control-Allow-Origin'] = '*'

    return response
