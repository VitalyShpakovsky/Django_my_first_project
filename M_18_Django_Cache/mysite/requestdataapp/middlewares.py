from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render
import time


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_user = {}

    def __call__(self, request: HttpRequest):
        # if request.META.get('REMOTE_ADDR') in self.request_user and (round(time.time(), 0) - self.request_user[request.META.get('REMOTE_ADDR')]) <= 0.1:
        #     return HttpResponseBadRequest('Lots of requests from your ip_address', status=404)
        # else:
        self.request_user = {request.META.get('REMOTE_ADDR'): round(time.time(), 0)}
        response = self.get_response(request)
        return response
    