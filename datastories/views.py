from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Story

def story(request, slug, owner_id=None):
    # For now slug must be unique
    if owner_id is None:
        story = get_object_or_404(Story, slug=slug, owner__isnull=True)
    else:
        story = get_object_or_404(Story, slug=slug, owner__isnull=False,
                                  owner__id=owner_id)

    pages = story.pages.order_by('storypage__page_number')

    page_count = pages.count()

    if page_count == 0:
        # No pages
        page = None
        page_num = 0
        page_next = 0
        page_prev = 0
    else:
        page_num = request.GET.get('page_num', '1')

        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1

        if page_num < 1:
            page_num = 1
        elif page_num > page_count:
            page_num = page_count

        page_prev = page_num - 1  # Will be 0 if no previous page
        page_next = page_num + 1
        if page_next > page_count:
            page_next = 0  # There is no next page

        page = pages[page_prev] # page 1 is at index 0, etc.

    return render_to_response('datastories/story.html',
                              dict(story=story,
                                   page=page,
                                   page_num=page_num,
                                   page_count=page_count,
                                   page_prev=page_prev,
                                   page_next=page_next),
                              context_instance=RequestContext(request))
