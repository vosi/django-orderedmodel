from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _


class OrderedModelAdmin(admin.ModelAdmin):
    ordering = ['order']
    exclude = ['order']

    def get_urls(self):
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/move_up/$', self.admin_site.admin_view(self.move_up)),
            (r'^(?P<pk>\d+)/move_down/$', self.admin_site.admin_view(self.move_down)),
        )
        return my_urls + super(OrderedModelAdmin, self).get_urls()

    def reorder(self, item):
        button = '<a href="{{0}}/move_{{1}}/"><img class="ctl arr_{{1}}" src="{0}admin/img/arrow-{{1}}.gif" border="0" /></a>'.format(
            settings.STATIC_URL)

        html = '<style type="text/css"> '\
               '.ctl {{ width: 14px; height: 12px; display: inline-block; }} '\
               '.arr_up {{ background: url(\'{0}admin/img/sorting-icons.gif\') -5px -50px no-repeat; }} '\
               '.arr_down {{ background: url(\'{0}admin/img/sorting-icons.gif\') -5px -94px no-repeat; }} '\
               '</style>'.format(settings.STATIC_URL)
        html += button.format(item.pk, 'down')
        html += '&nbsp;' + button.format(item.pk, 'up')
        return html

    reorder.allow_tags = True
    reorder.short_description = _('Reorder')
    reorder.admin_order_field = 'order'

    def move_down(self, request, pk):
        if self.has_change_permission(request):
            item = get_object_or_404(self.model, pk=pk)
            try:
                next_item = self.model.objects.filter(order__gt=item.order).order_by('order')[0]
            except IndexError:
                pass
            else:
                self.model.swap(item, next_item)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../../'))

    def move_up(self, request, pk):
        if self.has_change_permission(request):
            item = get_object_or_404(self.model, pk=pk)
            try:
                prev_item = self.model.objects.filter(order__lt=item.order).order_by('-order')[0]
            except IndexError:
                pass
            else:
                self.model.swap(item, prev_item)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../../'))
