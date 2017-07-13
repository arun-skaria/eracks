# -*- coding: utf-8 -*-

import os
import urllib
import json
import requests

from django.conf import settings
from django.conf.urls import url, patterns, include
from django.contrib.admin.views.decorators import staff_member_required

from home.models import FeaturedImage,IpAddress

#Email signup box
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

#from obdjects.classes import Obdject

#from apps.utils import minitags as tags
from utils import minitags as tags
from forms import *  # contact-us page forms


#for social login test
from django.contrib.auth import login
from social.apps.django_app.utils import psa

from django.template import RequestContext
from django.core.mail import send_mail
from utils.splituser import get_first_name,get_last_name
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
from bs4 import BeautifulSoup
## Create user & send email - called from two places

new_user_welcome_template = '''
Welcome to eRacks!

Dear %s,

Thank you for signing up at eracks.com

- Your login is: %s (May be the same as your email)
- Your email is: %s (You may also use this to login)
%s
You can manage your profile anytime by logging in to eRacks at:

http://%s/accounts/login

Sincerely,

The eRacks Team
info@eracks.com
'''


def create_new_user(form,request, first_name = "", last_name = ""):
    email = form.cleaned_data['email']  # required
    username = form.cleaned_data.get ('username', None)
    password1 = form.cleaned_data.get ('password1', None)

    if password1:
        password_entered = True
        password_msg = ""
    else:
        password1 = User.objects.make_random_password (length=8)
        password_entered = False
        password_msg = "\n- Your password is: %s \n"%(password1)

    if username:
        user = User.objects.create_user (username, email, password1)
    else:
        username = email
        user = User.objects.create_user (username, email, password1)
        
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
        
    user.save()

    user.email_user ('Welcome to eRacks!', new_user_welcome_template % (first_name or username, username, email, password_msg, request.get_host()), settings.INFO_EMAIL)

    return user,password_entered


## Contact-us page

contact_email_template = '''
{s.HOST_NAME} user contact form:

Name: {f[name]}
User: {u}
eMail: {f[email]}

Topic: {f[topic]}
Description (if other): {f[description]}

Body of message: {f[body]}

'''

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            email = request.POST.get('email', '')
            users = User.objects.filter(email=email)

            if users:
                user = users [0]  # pick first one, although there shouldn't be more than 1
                result = 'Thank you for contacting us "%s"' % user.username
            else:
                user, password_entered = create_new_user(form,request)
                result = 'Thank you for contacting us and welcome to eRacks!  Your user is "%s", and your password has been sent to you.' % user.username

            try:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ipaddress = x_forwarded_for.split(',')[-1].strip()
                else:
                    ipaddress = request.META.get('REMOTE_ADDR')

                if ipaddress:
                    activity_name = 'Contact-us'
                    customer_user = Customer.objects.get(user=user)
                    ip_add = IpAddress()
                    ip_add.customer = customer_user
                    ip_add.ip_address = ipaddress
                    ip_add.comments = "saved Contact-us user %s IP-Address" % user.username
                    ip_add.activity = activity_name
                    ip_add.save()

            except:
                pass

            subject = "%s user contact from %s about %s" % (settings.HOST_NAME, user, form.cleaned_data['topic'])
            message = contact_email_template.format (s = settings, f = form.cleaned_data, u = user)
            to = settings.CONTACT_EMAILS
            fm = user.email
            send_mail (subject, message, fm, to, fail_silently=False)

            return render (request, 'base.html', {'content': mark_safe (tags.h3(result))})

        return render (request, 'contact.html', {'form': form}, context_instance = RequestContext(request))

    form = ContactForm()

    return  render (request, 'contact.html',
        dict (
            form=form,
            meta_title='Contact with eRacks - Contact Us',
            meta_keywords='Rack Mount Server, Open Source Systems',
            meta_description='We are always interested in hearing from you, for all of your queries please stay in touch on info@eracks.com or you can call us on (408)455-0010',
        ),
        context_instance = RequestContext(request))


## Email signup box

def user_signup(request,template_name='userena/signup_form.html', success_url=None):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user,password_entered = create_new_user(form,request)

            if password_entered:
                result = 'Thank you for signing up and welcome to eRacks - your username is "%s"' % user.username
            else:
                result = 'Thank you for signing up and welcome to eRacks - your username is "%s", and your password has been sent to your email' % user.username

            try:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ipaddress = x_forwarded_for.split(',')[-1].strip()
                else:
                    ipaddress = request.META.get('REMOTE_ADDR')

                if ipaddress:
                    activity_name = 'Sign-up'
                    customer_user = Customer.objects.get(user=user)
                    ip_add = IpAddress()
                    ip_add.customer = customer_user
                    ip_add.ip_address = ipaddress
                    ip_add.comments = "saved sign-up user %s IP-Address" % user.username
                    ip_add.activity = activity_name
                    ip_add.save()

            except:
                pass

            return render (request, 'base.html', {'content': mark_safe(tags.h3(result))})
    else:
        form = SignupForm()

    return render (request, 'userena/signup_form.html', {'form': form })







#### generate_xml section - MANI: let's move this to a utils module, or a script, yes?

from xml.dom import minidom
import datetime
from time import strftime
from products.models import Product

def generate_xml():
    doc = minidom.Document()
    root = doc.createElement('urlset')
    doc.appendChild(root)
    all_products = Product.objects.all()
    for l in all_products:
        leaf = doc.createElement('loc')
        lastmod = doc.createElement('lastmod')
        changefreq = doc.createElement('changefreq')
        priority = doc.createElement('priority')
        branch = doc.createElement('url')
        text = doc.createTextNode('https://eracks.com%s' % l.url)
        dateandtime = doc.createTextNode(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"+00:00")
        changefreq_text = doc.createTextNode('daily')
        priority_text = doc.createTextNode('1.0000')
        lastmod.appendChild(dateandtime)
        leaf.appendChild(text)
        changefreq.appendChild(changefreq_text)
        priority.appendChild(priority_text)
        branch.appendChild(leaf.cloneNode(True))
        branch.appendChild(lastmod)
        branch.appendChild(changefreq)
        branch.appendChild(priority)
        root.appendChild(branch)
    xml_str = doc.toprettyxml(indent="  ")
    with open("apps/home/static/sitemap_generated.xml", "w") as f:
        f.write(xml_str)

#### End generate_xml


@staff_member_required
def testresults(request):
    path=settings.MEDIA_ROOT+"/test_results_screens"
    img_list =os.listdir(path)
    return render_to_response('test_results.html',{'images':img_list})


def index (request):
    return  render (request, 'home.html',
        dict (
            featured_images = FeaturedImage.objects.published,
            #? title = 'Rackmount Server, Open Source Systems, Linux Rackmount',
            meta_title = 'Rackmount Server, Open Source Systems, Linux Rackmount',
            meta_keywords ='Rackmount Server, Rack Mount Server, Open Source Systems, Linux Rackmount',
            meta_description ='We are the leading Open Source Systems provider, featuring our own line of rack mount servers. We offer a wide array of services including security and network architecture services.',
        ),
        context_instance = RequestContext(request))



## legacy Obdjects stuff - TODO: refactor - 9/16/15 JJW

gone='''
index = Obdject (
    urlregex = r'^$',
    #urlpattern = (r'^$', self),
    #template = 'home.html',
    template = 'home.html',
    #CustomerImagePubObjects = CustomerImage.objects.published,
    #TestimonialPubObjects = Testimonial.objects.published,
    featured_images = FeaturedImage.objects.published,
    meta_title = 'Rackmount Server, Open Source Systems, Linux Rackmount',
    meta_keywords = 'Rackmount Server, Rack Mount Server, Open Source Systems, Linux Rackmount',
    meta_description = 'We are the leading Open Source Systems features its own line of rack mount server and offer a wide array of services including security and network architecture services.',
)

urlpatterns = patterns('',
    index.urlpattern
)

'''


# ##request view for python-social-auth-test ('facebook','linkedin','github','google')
@psa('social:complete')
def testing_social_auth_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    if backend == 'facebook':
        print('Running TestCase For Facebook')
        test_user_token = get_facebook_user_access_token()
    elif backend == 'github':
        print('Running TestCase For Github')
        test_user_token = '251a3c90f801869dcc39a72fd2adc656a9e04e58'
    elif backend == 'linkedin':
        print('Running TestCase For Linkedin')
        oauth_t,oauth_v = get_linkedin_access_token() 
        test_user_token = { 'oauth_token': oauth_t, 'oauth_token_secret': oauth_v, 'oauth_verifier': oauth_v}
    else:
        print('')
        test_user_token = ''

    user = request.backend.do_auth(test_user_token)
    if user:
        login(request, user)
        if user.is_authenticated():
            if backend == 'facebook':
                return HttpResponse(content='facebook')
            elif backend == 'github':
                return HttpResponse(content='github')
            elif backend == 'linkedin':
                return HttpResponse(content='linkedin')
            # elif backend == 'google-oauth2':
            #     return HttpResponse(content='google')

            else:
                return HttpResponse(content='')


    else:
        return HttpResponse(content='ERROR')


def get_linkedin_access_token():
    client = requests.Session()
    o_token_url = client.get('https://eracks.com/login/linkedin/')
    o_token = o_token_url.url.split('=')[1].split('&')[0]
    html = client.get('https://www.linkedin.com').content
    soup = BeautifulSoup(html)
    csrf = soup.find(id="loginCsrfParam-login")['value']

    login_information = {
        'session_key': '',
        'session_password': '',
        'loginCsrfParam': csrf,
    }

    client.post('https://www.linkedin.com/uas/login-submit', data=login_information, verify=False)

    response = client.get('https://www.linkedin.com/uas/oauth/authenticate?scope=r_basicprofile%2Br_emailaddress&redirect_uri=https%3A%2F%2Feracks.com%2Fcomplete%2Flinkedin%2F&oauth_token='+o_token, verify=False)
    # authorization_code = response.url.split('=')[1].split('&')[0]
    # params = {
    #           'grant_type' : 'authorization_code',
    #           'code' : authorization_code,
    #           'redirect_uri' : 'http://eracks.com',
    #           'client_id' : settings.SOCIAL_AUTH_LINKEDIN_KEY,
    #           'client_secret' : settings.SOCIAL_AUTH_LINKEDIN_SECRET,
    # }
    # params = urllib.urlencode(params)
    # token_req = client.get("https://www.linkedin.com/oauth/v2/accessToken", params)
    # return json.loads(token_req.readlines()[0])['access_token']
    return  o_token,response.history[1].url.split('&')[1].split('=')[1]

def get_facebook_user_access_token():
    session = requests.Session()
    r = session.get('https://www.facebook.com/', allow_redirects=False)
    soup = BeautifulSoup(r.text)
    action_url = soup.find('form', id='login_form')['action']
    inputs = soup.find('form', id='login_form').findAll('input', {'type': ['hidden', 'submit']})
    post_data = {input.get('name'): input.get('value')  for input in inputs}
    post_data['email'] = 'nijap.techversant@gmail.com'
    post_data['pass'] = 'nijap@password'
    scripts = soup.findAll('script')
    scripts_string = '/n/'.join([script.text for script in scripts])
    datr_search = re.search('\["_js_datr","([^"]*)"', scripts_string, re.DOTALL)
    if datr_search:
        datr = datr_search.group(1)
        cookies = {'_js_datr' : datr}
    else:
        return False
    session.post(action_url, data=post_data, cookies=cookies, allow_redirects=False)
    response_access_token = session.get('https://www.facebook.com/v2.8/dialog/oauth?client_id='+settings.SOCIAL_AUTH_FACEBOOK_KEY+' &redirect_uri=https%3A%2F%2Feracks.com%2Fcomplete%2Ffacebook%2F%3Fredirect_state%3DjZrlke51xLisxi6SmKftj5VpVDTN3081', verify=False)
    response_user_token = session.get('https://graph.facebook.com/v2.8/oauth/access_token?client_id='+settings.SOCIAL_AUTH_FACEBOOK_KEY+'&redirect_uri=https%3A%2F%2Feracks.com%2Fcomplete%2Ffacebook%2F%3Fredirect_state%3DjZrlke51xLisxi6SmKftj5VpVDTN3081&client_secret='+settings.SOCIAL_AUTH_FACEBOOK_SECRET+'&code='+response_access_token.url.split('=')[2])
    return json.loads(response_user_token.text)['access_token']