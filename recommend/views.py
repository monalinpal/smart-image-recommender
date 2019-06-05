from rest_framework.views import APIView
from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import json
from os.path import join
import uuid
from django.utils import timezone
import os
import logging
import tempfile
import shutil
from shutil import copyfile
import datetime
from wsgiref.util import FileWrapper
import time
from datetime import timedelta
from image_recommend.settings import ICC_DATA_DIR
logger = logging.getLogger(__name__)
from recommend.src.main import *

current_date=datetime.datetime.strftime(datetime.datetime.now()+timedelta(hours=6),"%Y_%m_%d")
processed_name='Transaction_Feeds_Report_'+str(current_date)+'.xlsx'

def ImageRecommendHome(request):
    if request.method == 'POST' and request.FILES['myfile']:
          
        myfile = request.FILES['myfile']
        request_json={}
        request_json['attachment']=myfile.name
        
        request_folder = os.path.join(ICC_DATA_DIR)
          
        fs = FileSystemStorage(location=request_folder)
        filename = fs.save(str(myfile.name),myfile)
        print (str(myfile.name))
        try:
            image_find(str(myfile.name))
            return render(request, 'recommend/home.html', {'processed_name':'Executed'})
        except Exception as e:
            print (str(e))
            return render(request, 'recommend/home.html', {'exceptions': 'exceptions'})
    return render(request, 'recommend/home.html')