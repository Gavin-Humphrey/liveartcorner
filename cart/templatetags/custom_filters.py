from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    print("Dictionary:", dictionary)
    print("Key:", key)

    if isinstance(dictionary, dict):
        return dictionary.get(key, None)
    return None