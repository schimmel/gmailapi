from gcontacts.models import sync_user,contact
from django.contrib import admin

class contactAdmin(admin.ModelAdmin):
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

admin.site.register(sync_user)
admin.site.register(contact,contactAdmin)
