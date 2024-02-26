from django.shortcuts import render
from .models import Profile

import pdfkit
from django.http import HttpResponse
from django.template import loader
import io



#for filling up the resume
def resume_data(request):

    if request.method=='POST':
        name=request.POST.get("name","")
        email=request.POST.get("email","")
        phone=request.POST.get("phone","")
        summary=request.POST.get("summary","")
        degree=request.POST.get("degree","")
        school=request.POST.get("school","")
        universty=request.POST.get("universty","")
        previous_work=request.POST.get("previous_work","")
        Skills=request.POST.get("skills","")
        profile=Profile( name=name , email=email , phone=phone  , summary=summary , degree=degree , school=school , universty=universty , previous_work=previous_work , Skills=Skills )
        profile.save()
    return render(request , 'resumeapp/resumedata.html')



#for converting the html file to pdffile
def resume(request,id):
    user_profile=Profile.objects.get(pk=id)

    path_wkhtmltopdf = r'C:\wkhtmltopdf\bin'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    #converting html file to a downloadable pdf
    template=loader.get_template('resumeapp/resume.html')
    html=template.render({'user_profile':user_profile})
    
    options={
        'page-size':'letter',
        'encoding':"UTF-8",
    }

    pdf = pdfkit.from_string(html,False,options,configuration=config)

    response=HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition']='attachment'
    filename="resume.pdf"


    return response

#to display all the users resumes ! 
def list(request):
    profiles = Profile.objects.all()
    return render(request,'resumeapp/list.html',{'profiles':profiles})