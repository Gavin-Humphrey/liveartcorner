from decouple import config


def website_email(request):
    WEBSITE_EMAIL = config("WEBSITE_EMAIL")
    return {"WEBSITE_EMAIL": WEBSITE_EMAIL}
