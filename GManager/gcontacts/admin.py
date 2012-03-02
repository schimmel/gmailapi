from gcontacts.models import SyncUser,Contact
from django.contrib import admin

class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Name', 
                {'fields':
                    ['prname','firstname','addname','lastname','suname']
                    }
                ),
            ('Kontaktdaten',
                {'fields':
                    ['email','phone','bday','website'],
                'classes':
                    ['collapse']
                    }
                ),
            ('Adresse',
                {'fields':
                    ['street','pob','zip','city','state','country'],
                    'classes':
                    ['collapse']
                    }
                ),
            ]

admin.site.register(SyncUser)
admin.site.register(Contact,ContactAdmin)
