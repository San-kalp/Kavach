from django.shortcuts import render 
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

renderer = JSONRenderer()



def home(request):
    return render(request,'home/home.html')

@api_view(['GET'])
def checkSanction(request):
    try :
        headers = {'X-API-Key': 'd5d868e989c742cf7522c4ffd60d399e2ee509d42b56ec65dfeb61817c644eb5','Accept': 'application/json',}

        data = requests.get('https://public.chainalysis.com/api/v1/address/0x1da5821544e25c636c1417ba96ade4cf6d2f9b5a', headers=headers)


        return Response(data)
    
    except Exception as e:
        print("Error :", e)
