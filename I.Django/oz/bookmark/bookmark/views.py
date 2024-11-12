from django.http import HttpResponse, Http404
from django.shortcuts import render
from bookmark.models import Bookmark


# Create your views here.
def bookmark_list(request):
    # bookmarks = Bookmark.objects.all()
    bookmarks = Bookmark.objects.filter(id__gte=50)
    #  SELECT * FROM bookmark
    context = {
        'bookmarks': bookmarks
    }
    # return HttpResponse('<h1>북마크 리스트 페이지 입니다.</h>')
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     # from django.http import Http404
    #     raise Http404

    from django.shortcuts import get_object_or_404
    bookmark = get_object_or_404(Bookmark, pk=pk)

    context = {'bookmark': bookmark}
    return render(request, 'bookmark_detail.html', context)