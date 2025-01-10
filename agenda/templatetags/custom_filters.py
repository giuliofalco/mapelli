from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Aggiunge una classe CSS al campo di un form.
    """
    return field.as_widget(attrs={"class": css_class})
