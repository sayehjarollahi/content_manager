from datetime import datetime
from os.path import basename
from zipfile import ZipFile

from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.models import Category, Account, Suffix, File, Content, ContentAttributeKey, \
    ContentAttribute, Attachment, Library


@csrf_exempt
@transaction.atomic
def add_content(request):
    if request.method == 'GET':
        return get_add_content(request, "None")
    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title == '':
            return error(request, "Title is required")

        category_title = request.POST.get('category', None)

        category = Category.objects.get(title=category_title)
        if category is None:
            return error(request, "Category does not exist")

        user = User.objects.filter(pk=request.user.id).first()
        if user is None:
            return error(request, "User does not exist")
        try:
            creator_account = Account.objects.filter(user=user).first()
            if creator_account is None:
                return error(request, "Account creator does not exist")
        except ValueError:
            return error(request, "Account is required")

        file = (request.FILES.get('file', None))
        if file is None:
            return error(request, 'File is required')

        idx_suffix = file.name.rfind('.')
        if idx_suffix == -1:
            return error(request, "File does not have suffix")
        suffix_title = file.name[idx_suffix + 1:]
        if len(suffix_title) == 0:
            return error(request, "File does not have proper suffix")
        if Suffix.objects.filter(title=suffix_title).exists():
            file_suffix = Suffix.objects.get(title=suffix_title)
        else:
            return error(request, "Suffix does not exist")
        if file is not None:
            content_file = File(title=file.name, creation_date=datetime.now(), modification_date=datetime.now(),
                                bytes=file.read(), suffix=file_suffix)
        else:
            return error(request, "file-content is empty")

        content_attachments = []
        attachments = request.FILES.getlist('attachments')
        if attachments is not None:

            for i in range(len(attachments)):
                attachment = attachments[i]
                idx_suffix = attachment.name.rfind('.')
                if idx_suffix == -1:
                    return error(request, "Attachment " + str(i) + " does not have suffix")
                suffix_title = attachment.name[idx_suffix + 1:]
                if len(suffix_title) == 0:
                    return error(request, "Attachment " + str(i) + " does not have proper suffix")
                if Suffix.objects.filter(title=suffix_title).exists():
                    attach_suffix = Suffix.objects.get(title=suffix_title)
                else:
                    return error(request, "Suffix does not exist")
                if attachment is not None:
                    attachment_file = File(title=attachment.name, creation_date=datetime.now(),
                                           modification_date=datetime.now(),
                                           bytes=attachment.read(), suffix=attach_suffix)

                    content_attachment = Attachment(title=attachment_file.title, file=attachment_file)
                    content_attachments.append(content_attachment)

        if content_file.suffix not in category.allowed_suffixes.all():
            return error(request, "Suffix is not proper for content file")

        content_file.save()
        content = Content(title=title, category=category, file=content_file, creator_account=creator_account)
        content.save()

        for content_attachment in content_attachments:
            content_attachment.content = content
            content_attachment.file.save()
            content_attachment.save()
        attr_keys = ContentAttributeKey.objects.filter(category=content.category)
        for key in attr_keys:
            content_attribute = ContentAttribute(key=key, value="", content=content)
            content_attribute.save()

    else:
        return error(request, "request is not defined")
    return render(request, 'index.html')


def error(request, str, content_id=0, kind=False):
    if kind:
        return get_content(request, content_id, str)
    return get_add_content(request, str)


def get_content(request, content_id, str):
    content = Content.objects.get(pk=content_id)
    context = {}
    context['content_id'] = content_id
    context['title'] = content.title
    context['category'] = content.category.title
    context['categoryID'] = content.category.pk
    context['creator_user'] = content.creator_account.user.username
    context['creation_date'] = content.file.creation_date

    attachments = list(Attachment.objects.filter(content=content))
    attachments_send = []
    for attachment in attachments:
        attachments_send.append({'file': "", 'title': attachment.title})

    context['attachments'] = attachments_send

    attribute_keys_values = list(ContentAttribute.objects.filter(content=content))
    used_attribute_keys = []
    for akv in attribute_keys_values:
        used_attribute_keys.append(akv.key.key)
    attribute_keys = list(ContentAttributeKey.objects.filter(category=content.category))
    attribute_key_values_send = []
    counter = 0
    for ak in attribute_keys:
        if ak.key in used_attribute_keys:
            attribute_key_values_send.append({"key": ak.key, "value": attribute_keys_values[counter].value})
            counter += 1
        else:
            attribute_key_values_send.append({"key": ak.key, "value": ""})

    context["attribute_key_values"] = attribute_key_values_send
    context['error'] = "None"
    l = list(Library.objects.filter(category=content.category))
    ll = []
    for item in l:
        ll.append({'title': item.title, 'value': item.pk})
    context['libraries'] = ll
    usernames_values = []
    for user in list(User.objects.all()):
        usernames_values.append(user.username)
    context['usernames_values'] = usernames_values
    context['error'] = str
    return render(request, 'content.html', context)


def handle_uploaded_file(f):
    with open('test-file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def get_add_content(request, err_str="None"):
    return render(
        request,
        'add_content.html',
        {'categories': Category.objects.all(), 'error': err_str}
    )


def content_main_page(request, content_id):
    content = Content.objects.get(pk=content_id)
    context = {}
    context['content_id'] = content_id
    context['title'] = content.title
    context['category'] = content.category.title
    context['categoryID'] = content.category.pk
    context['creator_user'] = content.creator_account.user.username
    context['creation_date'] = content.file.creation_date

    attachments = list(Attachment.objects.filter(content=content))
    attachments_send = []
    for attachment in attachments:
        attachments_send.append(attachment.title)

    context['attachments'] = attachments_send

    attribute_keys_values = list(ContentAttribute.objects.filter(content=content))
    used_attribute_keys = []
    for akv in attribute_keys_values:
        used_attribute_keys.append(akv.key.key)
    attribute_keys = list(ContentAttributeKey.objects.filter(category=content.category))
    attribute_key_values_send = []
    counter = 0
    for ak in attribute_keys:
        if ak.key in used_attribute_keys:
            attribute_key_values_send.append({"key": ak.key, "value": attribute_keys_values[counter].value})
            counter += 1
        else:
            attribute_key_values_send.append({"key": ak.key, "value": ""})

    context["attribute_key_values"] = attribute_key_values_send
    context['error'] = "None"
    l = list(Library.objects.filter(category=content.category))
    ll = []
    for item in l:
        ll.append({'title': item.title, 'value': item.pk})
    context['libraries'] = ll
    usernames_values = []
    for user in list(User.objects.all()):
        usernames_values.append(user.username)
    context['usernames_values'] = usernames_values
    context['username_login'] = User.objects.get(pk=request.user.id).username

    print(context)
    return render(request, 'content.html', context)


def create_download_link(request, content_id):
    file_paths = []
    content = Content.objects.all().get(pk=content_id)
    file = open(f'static/content/Downloads/content/{content.pk}_{content.title}.{content.file.suffix.title}', 'wb')
    file.write(content.file.bytes)
    file.close()

    file_paths.append(f'static/content/Downloads/content/{content.pk}_{content.title}.{content.file.suffix.title}')
    for attachment in Attachment.objects.filter(content=content):
        if attachment is not None:
            path = f'static/content/Downloads/attachment/{attachment.pk}_{attachment.title}.{attachment.file.suffix.title}'
            file = open(path, 'wb')
            file.write(attachment.file.bytes)
            file.close()
            file_paths.append(path)
    with ZipFile(f'static/content/Downloads/{content.title}_{content_id}.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file, basename(file))
        print(zip)
    return HttpResponse(f'/static/content/Downloads/{content.title}_{content_id}.zip')


def add_to_library(request, content_id):
    library_id = request.POST['library_id']
    content = Content.objects.get(pk=content_id)
    library = Library.objects.get(pk=library_id)
    content.library = library
    content.save()
    return redirect('/my-page/libraries/all/')


def share_content(request, content_id):
    username = request.POST['username']
    content = Content.objects.get(pk=content_id)
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)
    content.shared_with_accounts.add(account)
    content.save()
    account.save()
    user.save()
    return redirect('/my-page/files/all/')


def delete_content(request):
    if request.method == 'POST':
        content_id = request.POST['content_id']
        content = Content.objects.get(pk=content_id)
        if request.user.account == content.creator_account:
            file = content.file
            file.delete()
            content.delete()
        return redirect('/my-page/files/all/')
