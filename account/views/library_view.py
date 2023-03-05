from django.shortcuts import render, redirect

from account.models import Library, Account, Category


def library_page(request, libraryId):
    library = Library.objects.get(pk=libraryId)
    contents = library.contents.all()

    return render(request, 'my-page.html', {'view': 'library', 'file_or_lib': 'file', 'items': contents})


def add_library(request):
    if request.method == 'POST':
        account = Account.objects.get(user_id=request.user.id)
        category = Category.objects.get(title=request.POST['category'])
        query_set = Library.objects.filter(title=request.POST['library_name'], category_id=category.id,
                                           account_id=account.id)
        if len(query_set) == 0:
            Library.objects.create(title=request.POST['library_name'], category_id=category.id, account_id=account.id)

        return redirect('/my-page/libraries/all/')

    elif request.method == 'GET':
        categories = Category.objects.all().values()
        categories = {
            'categories': categories
        }
        return render(request, 'add-library.html', context=categories)


def delete_library(request):
    if request.method == 'POST':
        account = Account.objects.get(user_id=request.user.id)
        category = Category.objects.get(title=request.POST['category'])
        library = Library.objects.get(title=request.POST['title'], category_id=category.id, account_id=account.id)
        library.delete()

        return redirect('/my-page/libraries/all/')
