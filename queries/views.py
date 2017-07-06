from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import Data, Sites

import datetime
import json
from django.core import serializers




class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CSVResponse(HttpResponse):
    """
    An HttpResponse that renders its contents as a CSV.
    
    'rows' should be a list of dict objects, with each entry corresponding to 1 CSV field.
    'fields' is the ordered list of field names in the CSV.
    """
    def __init__(self, rows, fields, **kwargs):
               
        csvfile = StringIO()
        
        # Write header with field names
        headerwriter = csv.writer(csvfile)    
        headerwriter.writerow(fields)
                                      
        # Write CSV rows
        writer = csv.DictWriter(csvfile, fields, extrasaction='ignore')
        for row in rows:
            writer.writerow(row)
            
            
        kwargs['content_type'] = 'text/csv'
        super(CSVResponse, self).__init__(csvfile.getvalue(), **kwargs)
        self['Content-Disposition'] = 'attachment'




def errorResponse(errormessage, format, extraJSON={}):
    """
    A nice standardized way to show the user an error message.
    """    
    
    if format == 'csv':
        return CSVResponse(
            [{'errormessage': errormessage}],
            fields=('errormessage',)  )
            
    else:
        json_objects = extraJSON.copy()
        json_objects['error'] = True
        json_objects['errormessage'] = errormessage
        return JSONResponse(json_objects)
        
        
def hello_peeg(request):
	return HttpResponse('hello peeg')

def site(request,id):
	siteID = request.GET.get('site_id')
	site = Sites.objects.get(site_id=id)	
	json_objects = [{'siteID': site.site_id, 'siteName': site.site_name}]
	return JSONResponse(json_objects)
	
	
def get_sites(request):
	sites = Sites.objects.all().order_by('int_id')	
	# json_objects = [{'site': (s.site_id + ', ' + s.site_name)} for s in sites]
	json_objects = [{'siteID': s.site_id, 'siteName': s.site_name} for s in sites]
	return JSONResponse(json_objects)
	
def get_data(request):
	
	# arguments passed to request
	startDate = request.GET.get('date_start')
	endDate = request.GET.get('date_end')
	siteID = request.GET.get('site_id')
	
	filtered = False
	data = Data.objects.all().order_by('data_entry_id')
	
# 	'date_recorded': d.date_recorded,
#   'date_recorded': datetime.date(2016, 10, 28)
# 	json_objects = [{'data_entry_id': d.data_entry_id, 'site_id': d.site_id, 'date_recorded': str(d.date_recorded),'time_recorded':d.time_recorded, 'average':d.average} for d in data]
# 	print (json_objects)
# 	return JSONResponse(json_objects)
	
	if startDate and endDate and siteID:
		filtered = True
		# __range: SELECT * WHERE date_recorded BETWEEN startDate and endDate;
		#data = Data.objects.filter(date_recorded__range=(startDate, endDate), site_id=siteID, time_recorded__contains='00:00')
		data = Data.objects.filter(date_recorded__range=(startDate, endDate), site_id=siteID)
		#.order_by('date_recorded', 'time_recorded')
		json_objects = [{'data_entry_id': d.data_entry_id, 'site_id': d.site_id, 'date_recorded': str(d.date_recorded),'time_recorded':d.time_recorded, 'average':d.average} for d in data]
		return JSONResponse(json_objects)
	else:
		return errorResponse("Please supply a 'date_start', 'date_end', and 'site_id' argument.", format, {"data":[]})
# 	
# 	if not filtered: # error message if the user didn't supply an argument to filter the species list
# 		#json_objects = [{'data': (d.date_recorded+ ' ' + d.time_recorded+ ' ' + d.average)} for d in data]
# 		#return errorResponse("Please supply a 'date_start', 'date_end', and 'site_id' argument.", format, {"data":[]})
# 		data = Data.objects.all()
# 		json_objects = [{'data': (d.data_entry_id + ' ' + d.site_id + ' ' + d.date_recorded+ ' ' + d.time_recorded+ ' ' + d.average)} for d in data]
# 	else:
# 		json_objects = [{'data': (d.data_entry_id + ' ' + d.site_id + ' ' + d.date_recorded+ ' ' + d.time_recorded+ ' ' + d.average)} for d in data]
# 		return JSONResponse({'data': json_objects})