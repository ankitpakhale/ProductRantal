from django.shortcuts import render, redirect, HttpResponse
from .models import UserRegistration, ListingModel,OwnerDetails,Booking,ProperFeedback
from .forms import UserForm, ListForm
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .filters import FilterDemo
from datetime import date
import smtplib,ssl
from email.mime.text import MIMEText
import random
import email.message
import itertools 
# text blob
from textblob import TextBlob
from django.db.models import Q
# Importing the NaiveBayesAnalyzer classifier from NLTK
from textblob.sentiments import NaiveBayesAnalyzer

def RegisterUSerView(request):
    form = UserForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration.html')

def LoginUserView(request):
    if request.POST:
        try:
            model = UserRegistration.objects.get(email_id=request.POST['email_id'])
            if model.password == request.POST['password']:
                request.session['User_email'] = model.email_id
                return redirect('UserIndexPage')
            else:
                return render(request,'login.html',{'error': "INCORRECT PASSWORD" })
        except:
            return render(request,'login.html',{'error': "INCORRECT USERNAME" })
    return render(request, 'login.html')

def forgot_pass(request):
    email=request.POST.get('email')
    request.session['email'] = email
    if email==None:
        return render(request,'email.html')
    print(email)
    otp=""
    rand1=random.choice('0123456789')
    rand2=random.choice('0123456789')
    rand3=random.choice('0123456789')
    rand4=random.choice('0123456789')
    otp=rand1+rand2+rand3+rand4
    print(otp)
    request.session['otp']=otp

    port = 465
    password = "mailtest123@"
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
    server.login("mailtesting681@gmail.com",password)
    msg=MIMEText("welcome\n" + email + "\nyour otp is : "+ otp +"\nplease don't share with others")
    msg['subject']='security mail'
    server.sendmail("mailtesting681@gmail.com",email,msg.as_string())
    server.quit()
    print(msg)
    
    return redirect('otpcheck')

def otpcheck(request):
    if request.session.has_key('otp'):
        otp=request.session['otp']
        try:
            otpobj=request.POST.get('otp')
            if otpobj==None:
                return render(request,'otp.html')
            if otp==request.POST.get('otp'):
                return redirect('newpwd')
            else:
                return HttpResponse("<a href=''>wrong otp entered</a>")
        except:
            return redirect('login')
    return render(request,'otp.html')

def newpwd(request):
    if request.session.has_key('email'):
        newpassword=request.POST.get('password')
        if newpassword==None:
            return render(request,'forget.html')
        obj=UserRegistration.objects.get(email_id=request.session['email'])
        obj.password=newpassword
        obj.save()
        del request.session['email']
        return redirect('login')
    else:
            return redirect('login')
    return render(request,'forget.html')

def Add_Listing(request):
    if 'User_email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['User_email'])
        if user_model.is_approved==True:
            if request.POST:
                form = ListForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    list_model = ListingModel.objects.latest('id')
                    list_model.email_id = user_model.email_id
                    list_model.save()
                    return redirect('myproperty')
        else:
            return render(request, 'add_list.html',{'approve':'Superuser Not Approved You'})
        return render(request, 'add_list.html',{'users_data':user_model})
    else:
        return redirect('login')

def Update_Owner_Property(request,id):
    if 'Owneremail' in request.session.keys():
        obj = ListingModel.objects.get(id=id)
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        if request.POST:
            obj.title = request.POST['title']
            obj.address = request.POST['address']
            obj.beds_qty = request.POST['beds_qty']
            obj.baths_qty =request.POST['baths_qty']
            obj.sqrft = request.POST['sqrft']
            obj.price = request.POST['price']
            img = request.FILES.get('image')
            video = request.FILES.get('video')
            if img != None:
                obj.image = img
            obj.description = request.POST['description']
            obj.country = request.POST['country']
            obj.city_type = request.POST['city_type']
            obj.rooms = request.POST['rooms']
            ac = request.POST.get('AC')
            if ac == "on":
                obj.AC = True
            else:
                obj.AC = False
            bw = request.POST.get('builtin_wardrobe')
            if bw == 'on':
                obj.builtin_wardrobe = True
            else:
                obj.builtin_wardrobe = False
            dw = request.POST.get('dish_washer')
            if dw == "on":
                obj.dish_washer = True
            else:
                obj.dish_washer = False
            fc = request.POST.get('floor_covering')
            if fc == "on":
                obj.floor_covering = True
            else:
                obj.floor_covering = False
            med = request.POST.get('medical')
            if med == "on":
                obj.medical = True
            else:
                obj.medical = False
            fen = request.POST.get('fencing')
            if fen == "on":
                obj.fencing = True
            else:
                obj.fencing = False
            inte = request.POST.get('internet')
            if inte == "on":
                obj.internet = True
            else:
                obj.internet = False
            obj.save()
            return redirect('OwnerProfileView',id)
        return render(request, 'owner_add_list.html',{'obj':obj,'owner_data':user_model})
    else:
        return redirect('ownerlogin')

def AllListView(request):
    if 'User_email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['User_email'])
        list_model = ListingModel.objects.all()  
        if request.GET:
            try:
                q = request.GET.get('search_data')
                print(q)
                print("Q Call")
            except:
                q = None
                print("No Q")
            
            if q != None and request.GET['search_data'] != None:
                apartmenttype = ListingModel.objects.all()
                apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                print("Q Collect")
                return render(request, 'listing.html', {'apartment1':apartment,'apartment':apartmenttype})
            else: 
                search = request.GET.get('text')
                pricefilter = request.GET.get('pricefilter')
                apartmenttype = ListingModel.objects.all()
                print("Q other Data")
                apartment = request.GET.get('city_type')
                if apartment != '':
                    list_model = ListingModel.objects.filter(city_type=apartment).order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)

                if pricefilter == 'low':
                    list_model = ListingModel.objects.all().order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                elif pricefilter == 'high':
                    list_model = ListingModel.objects.all().order_by('-price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                else:
                    list_model = ListingModel.objects.all()
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype,'users_data':user_model})
        else:
            print("Q POST")
            apartmenttype = ListingModel.objects.all()
            print("Q POst DAta")
            list_model = ListingModel.objects.all().filter(available=True)
            user_filter = FilterDemo(request.GET, queryset=list_model)
        list_model = ListingModel.objects.all()
        user_filter = FilterDemo(request.GET, queryset=list_model)
        return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype,'users_data':user_model})
        
    else:
        if request.GET:
            try:
                q = request.GET.get('search_data')
                print(q)
                print("Q Call")
            except:
                q = None
                print("No Q")
            
            if q != None and request.GET['search_data'] != None:
                apartmenttype = ListingModel.objects.all()
                apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                print("Q Collect")
                return render(request, 'listing.html', {'apartment1':apartment,'apartment':apartmenttype})
            else: 
                search = request.GET.get('text')
                pricefilter = request.GET.get('pricefilter')
                apartmenttype = ListingModel.objects.all()
                print("Q other Data")
                apartment = request.GET.get('city_type')
                if apartment != '':
                    list_model = ListingModel.objects.filter(city_type=apartment).order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)

                if pricefilter == 'low':
                    list_model = ListingModel.objects.all().order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                elif pricefilter == 'high':
                    list_model = ListingModel.objects.all().order_by('-price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                else:
                    list_model = ListingModel.objects.all()
                    user_filter = FilterDemo(request.GET, queryset=list_model)

        else:
            print("Q POST")
            apartmenttype = ListingModel.objects.all()
            print("Q POst DAta")
            list_model = ListingModel.objects.all()
            user_filter = FilterDemo(request.GET, queryset=list_model)
    return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype})



def OwnerAllListView(request):
    if 'Owneremail' in request.session.keys():
        user=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        list_model = ListingModel.objects.all().filter(available=True)  
        if request.GET:
            try:
                q = request.GET.get('search_data')
                print(q)
                print("Q Call")
            except:
                q = None
                print("No Q")
            
            if q != None and request.GET['search_data'] != None:
                apartmenttype = ListingModel.objects.all()
                apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                print("Q Collect")
                return render(request, 'Ownerlisting.html', {'apartment1':apartment,'apartment':apartmenttype,'owner_data':user})
            else: 
                search = request.GET.get('text')
                pricefilter = request.GET.get('pricefilter')
                apartmenttype = ListingModel.objects.all()
                print("Q other Data")
                apartment = request.GET.get('city_type')
                if apartment != '':
                    list_model = ListingModel.objects.filter(city_type=apartment).order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)

                if pricefilter == 'low':
                    list_model = ListingModel.objects.all().order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                elif pricefilter == 'high':
                    list_model = ListingModel.objects.all().order_by('-price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                else:
                    list_model = ListingModel.objects.all().filter(verified=True)
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                return render(request, 'Ownerlisting.html', {'all_list': user_filter,'apartment':apartmenttype,'owner_data':user})
        else:
            print("Q POST")
            apartmenttype = ListingModel.objects.all()
            print("Q POst DAta")
            list_model = ListingModel.objects.all().filter(available=True)
            user_filter = FilterDemo(request.GET, queryset=list_model)
        list_model = ListingModel.objects.all()
        user_filter = FilterDemo(request.GET, queryset=list_model)
        return render(request, 'Ownerlisting.html', {'all_list': user_filter,'apartment':apartmenttype,'owner_data':user})
        
    else:
        return redirect('ownerlogin')

def UserIndexPage(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        # list_model = ListingModel.objects.all().order_by('-id')[:3]
        
        prod = ListingModel.objects.all()
        
        data_set = {}
        for i in prod:
            sub_dict = {}
            print("------------------")
            print(i.id)
            fda = ProperFeedback.objects.filter(Property_name=i)
            tot_pos = 0.0
            tot_ret = 0.0
            count = 0
            for j in fda:
                count += 1
                # print("-+++-")
                # print(j.cust_name)
                # print(j.feed_pos)
                tot_pos += float(j.feed_pos)
                tot_ret += float(j.rating)
                # print(j.rating)
                # print("-+++-")
            
            if tot_pos > 0:
                tot_pos = float(tot_pos/count)
            else:
                tot_pos = 0.1
            if tot_ret > 0:
                tot_ret = float(tot_ret/count)
            else:
                tot_ret = 1
            sub_dict['count'] = count
            sub_dict['pos'] = f"{tot_pos:.4f}"
            sub_dict['ret'] = f"{tot_ret:.2f}"
            
            data_set[i] = sub_dict
            # print(sub_dict)
            print(f"total user = {count}")
            print(f"total positive = {tot_pos:.4f}")
            print(f"total rating = {tot_ret:.2f}")
            print("------------------")
        print(data_set)
        
  
        # printing original dict
        print("The original dictionary : " + str(data_set))
        
        # using sorted()
        # Sort nested dictionary by key
        res = sorted(data_set.items(), key = lambda x: x[1]['pos'])
        data_set = dict(reversed(res))
        # print result
        print("The sorted dictionary by marks is : " + str(res))
        print("The reversed dictionary by marks is : " + str(data_set))
        N = 6 
        data_set = dict(itertools.islice(data_set.items(), N))
        # return render(request,'deshbord.html',{'data_set':data_set})
        
        # return render(request, 'index.html',{'top':list_model,'users_data':user,'data_set':data_set})
        return render(request, 'index.html',{'users_data':user,'data_set':data_set})
    else:
        list_model = ListingModel.objects.all().order_by('-id')[:3]
        return render(request, 'index.html',{'top':list_model})
        

def OwnerIndexView(request):
    if 'Owneremail' in request.session.keys():
        user=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        list_model = ListingModel.objects.all().order_by('-id')[:3]
        return render(request, 'Ownerindex.html',{'top':list_model,'owner_data':user})
    else:
        return redirect('ownerlogin')
    

def ProfileView(request, id):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        model = ListingModel.objects.get(id=id)
        q = str(model.country)
        model.view_count += 1
        model.save()
        dataset = ''
        try:
            dataset = ListingModel.objects.filter(Q(country__icontains=q)| Q(address__icontains=q))[0:4]
        except:
            dataset = ListingModel.objects.all()[0:4]
        feeds = ProperFeedback.objects.filter(Property_name=model)
        try:
            User_feed = ProperFeedback.objects.get(Property_name=model,cust_data=user)
            if request.POST:
                User_feed.Property_name = model
                User_feed.cust_name = user
                User_feed.rating = request.POST['rating']
                User_feed.feedback = request.POST['feedback']
                
                test = str(request.POST['feedback'])
                # Applying the NaiveBayesAnalyzer
                blob_object = TextBlob(test, analyzer=NaiveBayesAnalyzer())
                # Running sentiment analysis
                analysis = blob_object.sentiment
                print(analysis)
                pos = float("{:.2f}".format(analysis.p_pos))
                neg = float("{:.2f}".format(analysis.p_neg))
                
                obj.feed_pos=pos
                obj.feed_neg=neg
                User_feed.save()
            return render(request, 'property-single.html', {'data_set':dataset,'data': model,'users_data':user,'feed_data':feeds,'feed':User_feed})
        except:
            if request.POST:
                obj = ProperFeedback()
                obj.Property_name = model
                obj.cust_data = user
                obj.rating = request.POST['rating']
                obj.feedback = request.POST['feedback']
                
                test = str(request.POST['feedback'])
                # Applying the NaiveBayesAnalyzer
                blob_object = TextBlob(test, analyzer=NaiveBayesAnalyzer())
                # Running sentiment analysis
                analysis = blob_object.sentiment
                print(analysis)
                pos = float("{:.5f}".format(analysis.p_pos))
                neg = float("{:.5f}".format(analysis.p_neg))

                obj.feed_pos=pos
                obj.feed_neg=neg

                
                
                obj.save()
            
        return render(request, 'property-single.html', {'data_set':dataset,'data': model,'users_data':user,'feed_data':feeds})
    else:
        return redirect('login')

def OwnerProfileView(request, id):
    if 'Owneremail' in request.session.keys():
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        model = ListingModel.objects.get(id=id)
        model.view_count += 1
        model.save()
        return render(request, 'ownerproperty-single.html', {'data': model,'owner_data':user_model})
    else:
        return redirect('ownerlogin')

def Owner_myproperty(request):
    if 'Owneremail' in request.session.keys():
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        all_list = ListingModel.objects.filter(email_id=request.session['Owneremail'])
        return render(request, 'ownermyproperty.html', {'all_list': all_list,'owner_data':user_model})
    else:
        return redirect('login')

def MyPropertyView(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        all_list = ListingModel.objects.filter(email_id=request.session['User_email'])
        return render(request, 'myproperty.html', {'all_list': all_list,'users_data':user})
    else:
        return redirect('login')


def deleteproperty(request, id):
    model = ListingModel.objects.get(id=id)
    model.delete()
    return redirect('myproperty')


def logout(request):
    if 'User_email' in request.session.keys():
        del request.session['User_email']
        return redirect('UserIndexPage')
    else:
        return redirect('UserIndexPage')

def ownersignup(request):
    if request.POST:
        model= OwnerDetails()
        model.Ownername=request.POST['Ownername']
        model.Owneremail=request.POST['Owneremail']
        model.Ownerphone=request.POST['Ownerphone']
        model.Ownerstate=request.POST['Ownerstate']
        model.password=request.POST['password']
        model.save()
        request.session['Owneremail']=model.Owneremail
        print(request.session['Owneremail'])
        return redirect('ownerlogin')
    return render(request,'ownersignup.html')

def ownerlogin(request):
    if request.POST:
        Owneremail=request.POST['Owneremail']
        password=request.POST['password']
        try:
            mo=OwnerDetails.objects.get(Owneremail=Owneremail)
            if mo.password==password:
                request.session['Owneremail']=mo.Owneremail
                return redirect('alldata')
            else:
                return render(request,'ownerlogin.html',{'error': "INCORRECT PASSWORD" })
        except:
            return render(request,'ownerlogin.html',{'error': "INCORRECT USERNAME" })
    return render(request,'ownerlogin.html')

def owner_Add_Listing(request):
    if 'Owneremail' in request.session.keys():
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        print(user_model)
        model=ListingModel()
        count=0
        if request.POST:
            form = ListForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                list_model = ListingModel.objects.latest('id')
                list_model.email_id = user_model.Owneremail
                list_model.property_id+=1
                list_model.save()        
                return redirect('Owner_myproperty')
        return render(request, 'owner_add_list.html',{'owner_data':user_model})
    else:
        return redirect('ownerlogin')

def prop_booking(request,id):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        prod=ListingModel.objects.get(id=id)
        if user.email_id == prod.email_id:
            return HttpResponse("<h2>You Are Owner Of This Property</h2>")
        else:
            owner=OwnerDetails.objects.get(Owneremail=prod.email_id)
            if request.POST and request.FILES:
                model=Booking()
                model.user_id=user
                model.owner_id=owner
                model.prop_id=prod
                model.document=request.POST and request.FILES['document']
                model.date=date.today()
                model.save()
                prod.available=False
                prod.rooms -= 1
                prod.save()
            return render(request,'booking.html',{'users_data':user,'prod':prod,'wait':'WAIT for approval'})
    else:
        return redirect('login')


def UserBooks(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        prod = Booking.objects.filter(user_id=user)
        return render(request,'UserBooks.html',{'users_data':user,'prod':prod})
    else:
        return redirect('login')

def viewBooks(request,id):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        prod = Booking.objects.get(id=id)
        return render(request,'UserspecBooks.html',{'users_data':user,'prod':prod})
    else:
        return redirect('login')

def alldata(request):
    if 'Owneremail' in request.session.keys():
        owner=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        book=Booking.objects.all().filter(owner_id=owner)
    return render(request,'alldata.html',{'book':book,'owner_data':owner})


def edit(request,id):
    if 'Owneremail' in request.session.keys():
        owner=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        book=Booking.objects.get(id=id)
        return render(request,'editbook.html',{'book':book,'owner_data':owner})
    else:
        return redirect('ownerlogin')

def update(request,id):
    if 'Owneremail' in request.session.keys():
        book=Booking.objects.get(id=id)
        if request.POST:
            book.boked=request.POST['boked']
            book.date=date.today()
            book.save()

            # my_email = "mailtesting681@gmail.com"
            # my_pass = "mailtest@123"
            # fr_email = book.user_id.email_id
            # mead_data = ""
            # front = """
            # <!DOCTYPE html>
            # <html>
            #     <body>
            #         <div>
            #             <h2>Name : """ + str(book.user_id.full_name) + """</h2>
            #             <h2>Email : """ + str(book.user_id.email_id) + """</h2>
            #             <h2>Property Name: """ + str(book.prop_id) + """</h2>
            #         </div>
            #         <br>
            #         <div>
            #             <h3>Owner of the Product apporved your request for property on """+ str(book.date) +"""
            #             <br>Thank you for using Rental System....</h3>
            #         </div>
            #     </body>
            # </html>
            # """
            # email_content = front + mead_data
            # print(email_content)
            
            # msg = email.message.Message()
            # msg['Subject'] = 'Approval for request' 
            # msg['From'] = my_email
            # msg['To'] = fr_email
            # password = my_pass
            # msg.add_header('Content-Type', 'text/html')
            # msg.set_payload(email_content)
            # s = smtplib.SMTP('smtp.gmail.com',587)
            # s.starttls()
            # s.login(msg['From'], password)
            # s.sendmail(msg['From'], [msg['To']], msg.as_string())
            return redirect('alldata')
        else:
            pass
    return render(request,'editbook.html')

def userbuy(request):
    if 'Owneremail' in request.session.keys():
        owner=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        mod=Booking.objects.filter(owner_id=owner)
        return render(request,'userbuy.html',{'owner':owner,'mod':mod})
    else:
        return redirect('ownerlogin')

def Owner_logout(request):
    if 'Owneremail' in request.session.keys():
        del request.session['Owneremail']
        return redirect('ownerlogin')
    else:
        return redirect('ownerlogin')

def getdetails(request,id):
    if 'User_email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['User_email'])
        prod=Booking.objects.get(id=id)
        print(prod.id)
        return render(request,'getdetails.html',{'prod':prod})
    else:
        return redirect('login')
        
def main(request):
    return render(request,'login/index.html')