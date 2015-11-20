GRAPPELLI_ADMIN_TITLE = 'MetalTrenches Admin'

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    'music': {
        'band': ('id__iexact', 'name__icontains',),
        'album': ('id__iexact', 'title__icontains', 'band__name__icontains',),
        'event': ('id__iexact', 'name__icontains',),
    },
}
