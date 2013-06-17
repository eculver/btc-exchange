from django.conf import settings


def default(request):
    "Returns context variables specific to views"

    context_extras = {
        "DEBUG": settings.DEBUG,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
    }

    return context_extras
