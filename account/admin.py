from django.contrib import admin

from account.models import Category, Content, Suffix, Account, Attachment, Library, File, \
    ContentAttribute, ContentAttributeKey, AttachCategory

admin.site.register(Category)
admin.site.register(Content)
admin.site.register(Suffix)
admin.site.register(AttachCategory)
admin.site.register(Attachment)
admin.site.register(Account)
admin.site.register(Library)
admin.site.register(File)
admin.site.register(ContentAttribute)
admin.site.register(ContentAttributeKey)
