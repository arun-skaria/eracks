from django.contrib import admin
from .models import Quote, QuoteLineItem
from home.models import IpAddress




### IP-ADDRESS LOG FOR AN QUOTE REQUEST + CUSTOMER

class IpAddressAdminOrderinline(admin.StackedInline):
    
    model = IpAddress
    readonly_fields = ('quote','customer_email','ipaddress_url','ip_address','customer','comments', 'activity')
    exclude = ['order']
          
    def customer_email(self,obj):
        return obj.customer.user.email
    
    def has_add_permission(self, request):
        return False    
    
    def ipaddress_url(self, obj):
        return '<a href="/admin/home/ipaddress/%s/details/" target="_blank" title="More Details">%s</a>' % (obj.id,obj.ip_address)
    ipaddress_url.allow_tags = True




#class LineItemInline(admin.TabularInline):
class LineItemInline(admin.StackedInline):
    model = QuoteLineItem
    extra = 1

class QuoteAdmin (admin.ModelAdmin):
    list_display = ('quote_number', 'customer','valid_for','customer_reference','target','created','modified')
    list_filter = ('created','modified','approved_by','customer',)
    #list_editable = ('closed','purchase_order')
    search_fields = ('quote_number', 'customer__user__username','customer__email','purchase_order',
                     'customer_reference','comments','quotelineitem__description', 'quotelineitem__comments')
    list_per_page = 50
    save_as = True

    fieldsets = (
        (None, { 'fields': (('customer', 'quote_number', 'approved_by',),
                            ('valid_for', 'purchase_order', 'customer_reference',),
                            ('terms', 'discount', 'discount_type'),
                            ('shipping', 'shipping_method','comments'),
                            ('target','image')
                            )   }),
        #('Description', { 'fields': ('description',), 'classes': ('collapse', 'edit'), }),
    )

    inlines = [LineItemInline,IpAddressAdminOrderinline]


# register admin objs

admin.site.register (Quote, QuoteAdmin)
#admin.site.register (Customer, CustomerAdmin)
#admin.site.register (QuoteLineItem, QuoteLineItemAdmin)
