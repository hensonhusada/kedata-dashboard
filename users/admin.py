from django.contrib import admin
from .models import KedataUsers, UsageKeywordListening, UsageKeywordComparison, UsageKeywordMultikey
# Register your models here.
admin.site.register(KedataUsers)
admin.site.register(UsageKeywordListening)
admin.site.register(UsageKeywordComparison)
admin.site.register(UsageKeywordMultikey)