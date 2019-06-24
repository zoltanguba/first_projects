from django.contrib import admin
from .models import (Translate,
                     WordDatabase,
                     DestinationLanguage)


admin.site.register(Translate)
admin.site.register(WordDatabase)
admin.site.register(DestinationLanguage)