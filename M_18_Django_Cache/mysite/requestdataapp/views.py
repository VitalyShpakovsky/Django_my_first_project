from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.files.storage import FileSystemStorage


def handel_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        fs = FileSystemStorage()
        myfile = request.FILES["myfile"]
        if myfile.size > 1048576:
            print("Слишком большой файл", myfile)
            return render(request, 'requestdataapp/file-error.html')
        else:
            filename = fs.save(myfile.name, myfile)
            print("Saved file", filename)

    return render(request, 'requestdataapp/file-upload.html')

