from django.db.models import Q
from django.shortcuts import render

from account.models import Content, Category, Library
from account.views.utils import redirect_not_authenticated


def my_page(request, page_type, categoryTitle):
    auth_result = redirect_not_authenticated(request)
    if auth_result is not None:
        return auth_result

    account = request.user.account

    if page_type == 'files':
        if categoryTitle == 'all':
            items = Content.objects.filter(Q(creator_account=account))
        else:
            category = Category.objects.get(title=categoryTitle)

            items = Content.objects.filter(
                Q(creator_account=account, category=category) | Q(category=category)
            )

        file_or_lib = 'file'

    elif page_type == 'libraries':
        if categoryTitle == 'all':
            items = Library.objects.filter(account=account)
        else:
            category = Category.objects.get(title=categoryTitle)
            items = Library.objects.filter(category=category, account=account)

        file_or_lib = 'lib'

    elif page_type == 'shared':
        contents = account.shared_with_contents.all()
        if categoryTitle == 'all':
            items = contents
        else:

            category = Category.objects.get(title=categoryTitle)
            items = contents.filter(category=category)
        file_or_lib = 'file'
    else:
        raise LookupError('page_type is not valid!')

    categories = Category.objects.all()

    return render(request, 'my-page.html', {
        'view': 'my-page',
        'file_or_lib': file_or_lib,
        'items': items,
        'categories': categories,
        'categoryTitle': categoryTitle,
        'type': page_type
    })
