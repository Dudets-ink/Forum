def check_user_ownership(request, place):
    """Compares user and place owner ids, if it different, raises a 404 error"""

    if place.owner.id != request.user.id:
        raise Http404
