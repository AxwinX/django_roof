from django.core.paginator import Paginator

PER_PAGE_OPTIONS = (10, 15, 25, 50)


def paginate(request, queryset, default_per_page=10):
    """
    Paginate `queryset` using ?page= and ?per_page= from the request.

    Returns a dict to merge into the template context:
      page_obj, per_page, per_page_options, page_range (with ellipses),
      query_string (current filters, URL-encoded, without page),
      hidden_params (current filters as pairs, for the per-page form)
    """
    # per_page: only allow known values so ?per_page=1000000 can't be abused
    try:
        per_page = int(request.GET.get("per_page", default_per_page))
    except (TypeError, ValueError):
        per_page = default_per_page
    if per_page not in PER_PAGE_OPTIONS:
        per_page = default_per_page

    paginator = Paginator(queryset, per_page)
    # get_page() never raises: bad/out-of-range page numbers fall back to
    # the first/last page.
    page_obj = paginator.get_page(request.GET.get("page"))

    page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=2, on_ends=1
    )

    params = request.GET.copy()
    params.pop("page", None)
    query_string = params.urlencode()          # includes status/search/per_page

    params.pop("per_page", None)
    hidden_params = [(k, v) for k, vals in params.lists() for v in vals]

    return {
        "page_obj": page_obj,
        "per_page": per_page,
        "per_page_options": PER_PAGE_OPTIONS,
        "page_range": page_range,
        "query_string": query_string,
        "hidden_params": hidden_params,
    }
