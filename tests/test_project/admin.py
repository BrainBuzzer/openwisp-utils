from django.contrib import admin
from openwisp_utils.admin import (MultitenantAdminMixin, MultitenantOrgFilter,
                                  MultitenantRelatedOrgFilter,
                                  TimeReadonlyAdminMixin)

from .models import Book, Shelf


class BaseAdmin(MultitenantAdminMixin, TimeReadonlyAdminMixin, admin.ModelAdmin):
    pass


class ShelfAdmin(BaseAdmin):
    list_display = ['name', 'organization']
    list_filter = [('organization', MultitenantOrgFilter)]
    fields = ['name', 'organization', 'created', 'modified']


class BookAdmin(BaseAdmin):
    list_display = ['name', 'author', 'organization', 'shelf']
    list_filter = [('organization', MultitenantOrgFilter),
                   ('shelf', MultitenantRelatedOrgFilter)]
    fields = ['name', 'author', 'organization', 'shelf', 'created', 'modified']
    multitenant_shared_relations = ['shelf']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'additional_buttons': [
                {
                    'type': 'button',
                    'url': 'DUMMY',
                    'class': 'previewbook',
                    'value': 'Preview book',
                },
                {
                    'type': 'button',
                    'url': 'DUMMY',
                    'class': 'downloadbook',
                    'value': 'Download book',
                }
            ]
        })
        return super(BookAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Shelf, ShelfAdmin)
admin.site.register(Book, BookAdmin)
