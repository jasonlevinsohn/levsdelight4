from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from levsdelight_app.models import Slideshow, MonthMap
import re, datetime, json, pprint, os, shutil
from django.views.decorators.csrf import csrf_exempt
from ImageUploader import ImageUploader

from levsdelight_app.models import Slideshow


# After receiving the images, process them by reducing
# the image quality and upload them to S3.
@csrf_exempt
def uploadimage(request):

    try:

        # print "The request"
        # print json.dumps(request)
        # pprint.pprint(request.__dict__)
        # print request.__dict__

        print "the request:"
        print request.POST

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
        ic = ImageUploader(str(theFile))
        ic.connectToS3()
        ic.upload_original()
        ic.create_upload_web_image()
        ic.create_upload_thumbnail()

        # Remove the tmp directory and all the temp files
        try:
            shutil.rmtree(this_path + '/tmp')
            print 'Temp Directory removed'
        except OSError as e:
            print 'Unable to remove temp direcotory'
            print e

    except Exception as e:
        print 'Error with uploadimage request'
        print e

        # Remove the tmp directory and all the temp files
        try:
            shutil.rmtree(this_path + '/tmp')
        except OSError as e:
            print 'Unable to remove temp direcotory'
            print e

        return JsonResponse({'message': e.message})


    # return HttpResponse("Hey, I appreciate the filez. \n\n %s" % (report))
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
    print "Slideshow Request Received for %s %s " % (month, year)

    result = {
            'month': month,
            'year': year
            }

    mapObject = MonthMap.objects.filter(month=month, year=year)
    map_id = mapObject[0].slideshow_id
    objects_returned = mapObject.count()
    print objects_returned
    if objects_returned > 1:
        print "ERROR: MonthMap returned more than one result"
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
