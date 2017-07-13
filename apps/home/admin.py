from django.contrib import admin
from functools import update_wrapper
from django.conf.urls import url  
from django.template import RequestContext  
from django.shortcuts import render_to_response
from django.contrib.gis.geoip import GeoIP
from apps.utils import created, updated, publish, unpublish

from .models import FeaturedImage,IpAddress



class FeaturedImageAdmin (admin.ModelAdmin):
    list_display = ('image', 'link', 'title', 'caption', 'published', 'sortorder', created, updated)
    list_filter = ('published','created','updated')
    search_fields = ('link', 'title', 'caption', 'image')
    list_editable = ('link', 'title', 'caption', 'published', 'sortorder',)
    list_per_page = 50
    save_as = True
    actions = [publish, unpublish]


class IpAddressAdmin(admin.ModelAdmin):
    list_display =('customer_email','ipaddress_url','comments','activity','created_date')
    list_per_page = 50
    review_template = 'ipaddress_review.html'
    readonly_fields = ('ip_address','customer','comments', 'activity')
    search_fields = ('ip_address','customer__user__username', 'activity' )
    list_filter = ('ip_address','customer__user__username','activity','created_date')
    
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
    
        urls = super(IpAddressAdmin, self).get_urls()
    
        info = self.model._meta.app_label, self.model._meta.model_name
    
        my_urls = [
            url(r'(?P<id>\d+)/details/$', wrap(self.review), name='%s_%s_details' % info),
        ]
    
        return my_urls + urls
    
    def review(self, request, id):
        entry = IpAddress.objects.get(pk=id)
        ip_add = entry.ip_address
        geo = GeoIP()
        geo_address = geo.city(ip_add)
        try:
            area_code = geo_address['area_code']
        except:
            area_code = "NONE"
        try:
            city = geo_address['city']
        except:
            city = "NONE"
        try:
            continent_code = geo_address['continent_code']
        except:
            continent_code = "NONE"
        try:
            country_code = geo_address['country_code']
        except:
            country_code = "NONE"
        try:
            country_name = geo_address['country_name']
        except:
            country_name = "NONE"
        try:
            dma_code = geo_address['dma_code']
        except:
            dma_code = "NONE"
        try:
            latitude = geo_address['latitude']
        except:
            latitude = "NONE"
        try:
            longitude = geo_address['longitude']
        except:
            longitude = "NONE"
        try:
            postal_code = geo_address['postal_code']
        except:
            postal_code = "NONE"
            
        try:
            region = geo_address['region']
        except:
            region = "NONE"
            
        return render_to_response(self.review_template, {
            'title': 'Review IP-ADDRESS: %s' % entry.ip_address,
            'entry': entry,
            'area_code':area_code,
            'city':city,
            'continent_code':continent_code,
            'country_name':country_name,
            'dma_code':dma_code,
            'latitude':latitude,
            'longitude':longitude,
            'postal_code':postal_code,
            'region':region,
            'opts': self.model._meta,
            }, context_instance=RequestContext(request)) 
    
    def customer_email(self,obj):
        return obj.customer.user.email
    
    def has_add_permission(self, request):
        return False    
    
    def ipaddress_url(self, obj):
        return '<a href="%s/details/" title="View Details">%s</a>' % (obj.id, obj.ip_address)
    ipaddress_url.allow_tags = True    


# register admin objs
admin.site.register(FeaturedImage,FeaturedImageAdmin)
admin.site.register(IpAddress,IpAddressAdmin)

