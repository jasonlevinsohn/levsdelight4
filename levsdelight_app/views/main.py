from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from levsdelight_app.models import Slideshow, MonthMap
import re, datetime, json, pprint, os
from django.views.decorators.csrf import csrf_exempt

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
        print request.REQUEST

        file = request.FILES['farmFile']

        # Save the uploaded file to a temporary place on disk.
        this_path = os.path.dirname(os.path.abspath(__file__))
        # This can also be used `this_path = os.getcwd()`
        # for getting current working directory
        full_path_file = this_path + '/tmp_image.jpg'

        with open(full_file_path, 'wb+') as saved_tmp_file:
        for chunk in f.chunks():
            saved_tmp_file.write(chunk)
        # End saving temp file to disk 06.13.2015

        
        # desc = request.REQUEST['description']
        # title = request.REQUEST['title']
        # month = request.REQUEST['month']
        # report = "Desc: %s\n Title: %s\n Month: %s" % (desc, title, month)
        print file
    except Exception as e:
        print 'Error with uploadimage request'
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
