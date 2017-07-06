from django.http import HttpResponse

from .models import Data, Site

import datetime




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
	
	
def get_data(request):
	"""
    Return a JSON response with a sorted list of  acoustic data given a date range and site id
    
    JSON: For each species, include a {key:xxx, display:xxx} with the names to 
    use as a database key, and to display to the user (the same for now.)
    
    If there's a "date_start", "date_end", or "site_id" in the query 
    string, return only species matching these supplied parameters.  

    """
        
    
    filtered = False # make sure we're filtering by something
    data = Data.objects.all().order_by('data_entry_id')
    startDate = request.GET.get('date_start')
    endDate = request.GET.get('date_end')
    siteID = request.GET.get('site_id')
    
    #start_date = datetime.date(2005, 1, 1)
    #end_date = datetime.date(2005, 3, 31)

    
    
    if startDate and endDate and siteID:
        filtered = True
        data = Data.objects.filter(date_recorded__range=(startDate, endDate), site_id=siteID)
        
        # __range: SELECT * WHERE date_recorded BETWEEN startDate and endDate;
        
        
        
    # error message if the user didn't supply an argument to filter the species list
    if not filtered: 
        return errorResponse("Please supply a 'date_start', 'date_end', and 'site_id' argument.", format, {"data":[]})
         
    
    # return species list if it was filtered by something
    # s.genus_name_id gets the actual text of the genus_name, instead of the related object     
    else:
    	json_objects = [{'data': (d.date_entry_id + ' ' + d.site_id + ' ' + d.date_recorded+ ' ' + d.time_recorded+ ' ' + d.average)} for d in data]
    	return JSONResponse({'data': json_objects})