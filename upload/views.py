from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Image
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views import generic
from .forms import ImageForm
from django.contrib.auth.models import User




def upload_detail(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        idd = request.user.id
        entry = User.objects.get(pk=idd)
        p = Image(userid = entry, product = request.FILES['product'])
        if form.is_valid():
            p.save()
            return render(request, 'recomendation.html')
    else:
        form = ImageForm()
    return render(request, 'details.html',{'form':form})


'''def upload_detail(request):
    return render(request, 'details.html')'''


