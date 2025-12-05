from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
)
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse

@api_view(["GET"])
def index(request: HttpRequest) -> Response:
    
    context = {"ok":1}
    
    return Response(context)


@api_view(["GET", "POST"])
def optimize(request: HttpRequest) -> Response:
    
    data = request.data

    # como vai trata a entrada de dados???

    context = {"ok":1}
    
    return Response(context)
