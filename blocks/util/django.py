
from rest_framework.exceptions import ValidationError

import io
import csv

def parse_memory_handler(request, name:str, slice_func:int):
    '''return a list of the lines from a CSV file in a request'''
    upload_file = request.FILES.get(name)
    if upload_file is None:
        raise ValidationError({"error":"file for '%s' not provided" % name})
    if upload_file.content_type != "text/csv":
        raise ValidationError({"error":"csv file required"})

    io_string = io.StringIO(upload_file.read().decode())
    read = csv.reader(io_string)
    
    return [i[slice_func] for i in read]