from urllib import request
import pytz
import random
import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from account.models import Account, Credit, UserProfile
from job.models import Company, Invoice, Payment, Post, Comment, Field, Role, Industry, Discipline, State, Region, Qualification


def register(request):
    
    if request.method == 'POST':

        first_name = request.POST['fname']
        last_name = request.POST['lname']
        phone_number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_check = Account.objects.get(email=email)
            messages.error(request, 'An Email already exists for this address')
        
        except ObjectDoesNotExist:
            user = Account.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            email = email,
            password = password
            )
            user.save()

            user_profile = UserProfile.objects.create(user=user, profile_pic='userprofile/profile.png')
            user_profile.save()

            return redirect('login')


    return render(request, 'register.html')


def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, 'Invalid Credentials!')

    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):

    auth.logout(request)

    return redirect('login')

def home(request):

    posts = Post.objects.filter(free_post=False, draft=False)

    return render(request, 'index.html', {'posts': posts})

def search(request):
    print(request.GET)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            posts = Post.objects.order_by('-date_posted').filter(
                Q(description__icontains=keyword) 
                # | Q(company__name__icontains=keyword)
                | Q(position_title__icontains=keyword)
                # | Q(field__field__icontains=keyword)
                # | Q(qualification__qualification__icontains=keyword)
                | Q(employment_type__icontains=keyword)
                # | Q(state__state__icontains=keyword)
                | Q(city__icontains=keyword)
                # | Q(role__role__icontains=keyword)
                # | Q(industry__industry__icontains=keyword)
                # | Q(discipline__discipline__icontains=keyword)
                # | Q(region__region__icontains=keyword)
            )

    return render(request, 'index.html', {'posts': posts})

@login_required(login_url='login')
def add_company(request):

    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        name     = request.POST['name']
        regno    = request.POST['regno']
        type     = request.POST['type']
        relation = request.POST['relation']
        industry = request.POST['industry']
        link     = request.POST['link']
        address  = request.POST['address']
        number   = request.POST['number']
        email    = request.POST['email']
        # logo     = request.POST['logo']
        about    = request.POST['about']

        company = Company(
            user=request.user, name=name,
            reg_no=regno, type=type,
            affiliation=relation, industry=industry,
            web_link=link, address=address,
            phone_number=number, email=email,
            description=about
        )
        company.save()
        return redirect(reverse('managecompanies'))

    return render(request, 'addCompany.html', {"profile": profile})

@login_required(login_url='login')
def paid_post(request):

    user = Account.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    companies = Company.objects.filter(user=request.user)
    fields = Field.objects.all()
    roles = Role.objects.all()
    industries = Industry.objects.all()
    disciplines = Discipline.objects.all()
    states = State.objects.all()
    regions = Region.objects.all()
    qualifications = Qualification.objects.all() 

    if request.method == 'POST':

        if user_profile.credit > 0:
            
            company = request.POST['selectCompany']
            position_title = request.POST['posTitle']
            qualification = request.POST['qualification']
            employment_type = request.POST['employType']
            city = request.POST['city']
            min_exp = request.POST['minexp']
            max_exp = request.POST['maxexp']
            currency = request.POST['currency']
            term = request.POST['term'] 
            minsal = request.POST['minsal']
            maxsal = request.POST['maxsal']
            appdead = request.POST['appdead']
            appdeaddate = request.POST['date']
            #addons
            state = request.POST['state']
            role = request.POST['role']
            industry = request.POST['industry']
            discipline = request.POST['discipline']
            field = request.POST['jobField']
            region = request.POST['region']
            #endaddons
            description = request.POST['jobDesc']
            # app_method = request.POST['appMethod']
            post_now = bool(request.POST['postNow'])

            date_string = f'{appdeaddate}'
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')

            #time naive to time aware
            tz = pytz.timezone('US/Pacific')
            utc_dt = tz.localize(date_obj, is_dst=None).astimezone(pytz.utc)

            post = Post(
                user=user, company_id=company, position_title=position_title,
                qualification=qualification, employment_type=employment_type,
                state_id=state, city=city, min_exp=min_exp, max_exp=max_exp,
                currency=currency, term=term, min_salary=minsal, 
                max_salary=maxsal, app_deadline=appdead, dead_date=utc_dt,
                description=description, draft=True if post_now == False else False,
                featured_post=True, role_id=role, industry_id=industry,
                discipline_id=discipline, region_id=region, field_id=field
            )
            post.save()
            
            user_profile.credit -= 1
            user_profile.save()

            # print(post.__dict__.values())
            return HttpResponse('Your Job has been Posted')
        
        else:
            return HttpResponse('You do not have enough credits to perform this action')

        

    context = {
        "profile": user_profile,
        "companies": companies,
        "fields": fields,
        "roles": roles,
        "industries": industries,
        "disciplines": disciplines,
        "states": states,
        "regions": regions,
        "qualifications": qualifications
        }

    return render(request, 'paidjob.html', context)

@login_required(login_url='login')
def free_post(request):

    user = Account.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    companies = Company.objects.filter(user=request.user)
    fields = Field.objects.all()
    roles = Role.objects.all()
    industries = Industry.objects.all()
    disciplines = Discipline.objects.all()
    states = State.objects.all()
    regions = Region.objects.all()
    qualifications = Qualification.objects.all() 

    if request.method == 'POST':

        if user_profile.free_post:
            
            company = request.POST['selectCompany']
            position_title = request.POST['posTitle']
            qualification = request.POST['qualification']
            employment_type = request.POST['employType']
            city = request.POST['city']
            min_exp = request.POST['minexp']
            max_exp = request.POST['maxexp']
            currency = request.POST['currency']
            term = request.POST['term'] 
            minsal = request.POST['minsal']
            maxsal = request.POST['maxsal']
            appdead = request.POST['appdead']
            appdeaddate = request.POST['date']
            #addons
            state = request.POST['state']
            role = request.POST['role']
            industry = request.POST['industry']
            discipline = request.POST['discipline']
            field = request.POST['jobField']
            region = request.POST['region']
            #endaddons
            description = request.POST['jobDesc']
            # app_method = request.POST['appMethod']
            post_now = bool(request.POST['postNow'])

            date_string = f'{appdeaddate}'
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')

            #time naive to time aware
            tz = pytz.timezone('US/Pacific')
            utc_dt = tz.localize(date_obj, is_dst=None).astimezone(pytz.utc)

            post = Post(
                user=user, company_id=company, position_title=position_title,
                qualification=qualification, employment_type=employment_type,
                state_id=state, city=city, min_exp=min_exp, max_exp=max_exp,
                currency=currency, term=term, min_salary=minsal, 
                max_salary=maxsal, app_deadline=appdead, dead_date=utc_dt,
                description=description, draft=True if post_now == False else False,
                featured_post=True, free_post=True, role_id=role, industry_id=industry,
                discipline_id=discipline, region_id=region, field_id=field
            )
            post.save()
            
            user_profile.free_post = False
            user_profile.save()

            # print(post.__dict__.values())
            return HttpResponse('Your Free Post has been made!')
        
        else:
            return HttpResponse('You do not have exhausted your free posts')

        

    context = {
        "profile": user_profile,
        "companies": companies,
        "fields": fields,
        "roles": roles,
        "industries": industries,
        "disciplines": disciplines,
        "states": states,
        "regions": regions,
        "qualifications": qualifications
        }

    return render(request, 'freepost.html', context)

def postDetail(request, post_id):

    post = Post.objects.get(id=post_id)
    pinned_posts = Post.objects.filter(pinned_post=True)
    comments = Comment.objects.filter(post_id=post_id)
    comment_count = len(comments)

    context = {
        'post': post,
        'pinned_posts': pinned_posts,
        'comments': comments,
        'comment_count': comment_count
        }

    return render(request, 'postDetail.html', context)

def postComment(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':

        user_name = request.POST['name']
        email = request.POST['email']
        comment_content = request.POST['comment']

        comment = Comment(
            post=post, user_name=user_name,
            email=email, comment_content=comment_content
        )
        comment.save()

    return redirect(f'/post/{post_id}')

@csrf_exempt
@login_required(login_url='login')
def manageCompanies(request):

    companies = Company.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'DELETE':
        data = json.loads(request.body)
        Company.objects.get(id=data['id']).delete()

    context = {
        'companies': companies,
        'profile': user_profile
    }

    return render(request, 'manageCompanies.html', context)

@login_required(login_url='login')
def manageInvoice(request):

    profile = UserProfile.objects.get(user=request.user)
    records = Payment.objects.filter(user=request.user)
    context = {
        'profile': profile,
        'records': records
    }

    return render(request, 'manageInvoice.html', context)

@login_required(login_url='login')
def invoiceItem(request, inv_id):

    profile = UserProfile.objects.get(user=request.user)
    item = Payment.objects.get(id=inv_id)
    context = {
        'item': item,
        'profile': profile
        }

    return render(request, 'invoiceItem.html', context)

def test(request):
    return render(request, 'success.html')
    import os
    import platform

    opSys = platform.platform().split('-', 1)[0]

    if(opSys == 'Windows'):
        os.system(f'Taskkill /F /PID {os.getpid()}')
    else:
        os.system(f'kill {os.getpid()}')
        
@csrf_exempt
@login_required(login_url='login')
def dashboard(request):
    
    user = Account.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    if request.method == 'POST':
        user_profile.profile_pic = request.FILES['img']
        user_profile.save()

    if request.method == 'DELETE':
        data = json.loads(request.body)
        Post.objects.get(id=data['id']).delete()


    context = {
        'user': user,
        'profile': user_profile,
        'posts': posts 
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def personalInfo(request):

    profile = UserProfile.objects.get(user=request.user)

    return render(request, 'personalInfo.html', {"profile": profile})

def editPersonalInfo(request):

    if request.method == 'POST':
        email  = request.POST['email']
        number = request.POST['number']

        user = Account.objects.get(id=request.user.id)
        user.email = email
        user.number=number
        user.save()
        return render(request, 'success.html')

    return render(request, 'editProfileInfo.html')

def changePassword(request):

    if request.method == 'POST':
        email        = request.POST['email']
        old_pass     = request.POST['old_pass']
        new_pass     = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']

        user = Account.objects.get(email=email)
        password_check = user.check_password(old_pass)
        password_same = new_pass == confirm_pass

        print(password_check, password_same)

        if password_check and password_same: 
            user.set_password(new_pass)
            user.save()
            return render(request, 'success.html')


    return render(request, 'changePassword.html')

@login_required(login_url='login')
def buyCredit(request):

    credits = Credit.objects.all()
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        amount = request.POST['credPrice']
            
        return redirect(reverse('creditinvoice', kwargs={'amount':amount}))

    return render(request, 'buyCredit.html', {'credits':credits, 'profile': profile})

@login_required(login_url='login')
def creditInvoice(request, amount):
    
    credit = Credit.objects.get(price=amount)
    user = Account.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=request.user)
    todays_date = datetime.now().date()

    if request.method == 'POST':
        if request.POST['payMethod'] == 'paystack':

            return redirect(reverse('paystatus', kwargs={'amount':credit.price}))
        else:
            return HttpResponse('Bank Account information should be here')

    context = {
        "amount": credit.price,
        "credit": credit.value,
        "date": todays_date,
        "user": user,
        "profile": profile
    }

    return render(request, 'creditInvoice.html', context)

@login_required(login_url='login')
def payStatus(request, amount):

    user = Account.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=request.user)
    
    time_now = datetime.now()
    rand_int = random.randint(0, 999)
    order_no = str(time_now)[:10].replace('-', '') + str(rand_int)

    context = {
        "profile": profile,
        "email":  user.email,
        "amount": amount * 100,
        "referrence_no": order_no,
    }

    return render(request, 'payStatus.html', context)

@login_required(login_url='login')
def paySuccess(request):

    user = Account.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':

        body = json.loads(request.body)


        order_ref = body['reference']
        status = body['order_status']
        payment_id = body['transaction_id']
        amount_paid = body['amount']

        if status == 'success':

            credit = Credit.objects.get(price=amount_paid)
            payment = Payment(
                user=user, payment_id=payment_id,
                order_ref=order_ref, payment_method='PAYSTACK',
                amount_paid=amount_paid, credits_received=credit.value, status=True,
            )
            payment.save()

            user_profile.credit += credit.value
            user_profile.save()

            return render(request, 'success.html')
        else:
            credit = Credit.objects.get(price=amount_paid)
            payment = Payment(
                user=user, payment_id=payment_id,
                order_ref=order_ref, payment_method='PAYSTACK',
                amount_paid=amount_paid, credits_received=credit.value, status=False,
            )
            payment.save()

    return HttpResponseNotFound('Unauthorized')

def blockFilt(request, field):

    objects = eval(field + ".objects.all()")
    # objects = Field.objects.all()

    return render(request, 'barFilt.html', {'objects': objects})    
    
# BLOCKLINKS

def featuredBlock(request):

    posts = Post.objects.filter(featured_post=True)

    return render(request, 'index.html', {'posts': posts})

def todayBlock(request):

    today = datetime.now().date()
    posts = Post.objects.filter(date_posted=today)
    
    return render(request, 'index.html', {'posts': posts})

def yesterdayBlock(request):

    today = datetime.now().date() 
    yesterday = today - timedelta(days=1)
    posts = Post.objects.filter(date_posted=yesterday)

    return render(request, 'index.html', {'posts': posts})

def fieldBlock(request, field):

    posts = Post.objects.filter(field=field)

    return render(request, 'index.html', {'posts': posts})

def roleBlock(request, role):

    posts = Post.objects.filter(role=role)

    return render(request, 'index.html', {'posts': posts})

def industryBlock(request, industry):

    posts = Post.objects.filter(industry=industry)

    return render(request, 'index.html', {'posts': posts})

def subjectBlock(request, discipline):

    posts = Post.objects.filter(discipline=discipline)

    return render(request, 'index.html', {'posts': posts})

def stateBlock(request, state):

    posts = Post.objects.filter(state=state)

    return render(request, 'index.html', {'posts': posts})

def regionBlock(request, region):

    posts = Post.objects.filter(region=region)

    return render(request, 'index.html', {'posts': posts})

def closeBlock(request):

    posts = None

    return render(request, 'index.html', {'posts': posts})