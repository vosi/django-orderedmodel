from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _


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
    button = '<a href="{{0}}/move_{{1}}"><img class="ctl arr_{{1}}" src="{0}admin/img/arrow-{{1}}.gif" border="0" alt="{{1}}" /></a>'.format(settings.STATIC_URL)

    html = ''
    html += button.format(item.pk, 'down')
    html += '&nbsp;' + button.format(item.pk, 'up')
    return html
  reorder.allow_tags = True
  reorder.short_description = _('Reorder')

  def move_down(self, request, pk):
    if self.has_change_permission(request):
      item = get_object_or_404(self.model, pk=pk)
      try:
        next_item = self.model.objects.filter(order__gt=item.order).order_by('order')[0]
      except IndexError:
        pass
      else:
        self.model.swap(item, next_item)
    return HttpResponseRedirect('../../')

  def move_up(self, request, pk):
    if self.has_change_permission(request):
      item = get_object_or_404(self.model, pk=pk)
      try:
        prev_item = self.model.objects.filter(order__lt=item.order).order_by('-order')[0]
      except IndexError:
        pass
      else:
        self.model.swap(item, prev_item)
    return HttpResponseRedirect('../../')

