from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Story
from places.models import Place

def story(request, place_slug, story_slug=None, owner_id=None):
    place = get_object_or_404(Place, slug=place_slug)

    place_stories = place.datastories.all()

    # Maybe return an alternate rendering if place_stories.count == 0?

    if story_slug is None:
        try:
            story = place_stories[0]
        except Story.DoesNotExist, IndexError:
            raise Http404
    elif owner_id is None:
        story = get_object_or_404(place_stories,
                                  slug=story_slug,
                                  owner__isnull=True)
    else:
        story = get_object_or_404(place_stories,
                                  slug_id=Noneslug,
                                  owner__isnull=False,
                                  owner__id=owner_id)

    pages = story.pages.order_by('storypage__page_number')

    paginator = Paginator(pages, 1)

    page_count = paginator.num_pages

    page_num = request.GET.get('page_num')
    try:
        pgpg = paginator.page(page_num)
    except PageNotAnInteger:
        pgpg = paginator.page(1)
    except EmptyPage:
        pgpg = paginator.page(page_count)

    if not pgpg.object_list:
        # No pages
        page = None
        page_num = 0
        page_next = 0
        page_prev = 0
        page_count = 0
    else:
        page = pgpg.object_list[0]
        page_num = pgpg.number
        page_next = pgpg.next_page_number() if pgpg.has_next() else 0
        page_prev = pgpg.previous_page_number() if pgpg.has_previous() else 0

#     page_count = pages.count()

#     if page_count == 0:
#         # No pages
#         page = None
#         page_num = 0
#         page_next = 0
#         page_prev = 0
#     else:
#         page_num = request.GET.get('page_num', '1')

#         try:
#             page_num = int(page_num)
#         except ValueError:
#             page_num = 1

#         if page_num < 1:
#             page_num = 1
#         elif page_num > page_count:
#             page_num = page_count

#         page_prev = page_num - 1  # Will be 0 if no previous page
#         page_next = page_num + 1
#         if page_next > page_count:
#             page_next = 0  # There is no next page

#         page = pages[page_prev] # page 1 is at index 0, etc.

    return render_to_response('datastories/story.html',
                              dict(story=story,
                                   page=page,
                                   page_num=page_num,
                                   page_count=page_count,
                                   page_prev=page_prev,
                                   page_next=page_next,
                                   paginator=paginator,
                                   paginator_page=pgpg,
                                   place=place,
                                   datastories=place_stories),
                              context_instance=RequestContext(request))
