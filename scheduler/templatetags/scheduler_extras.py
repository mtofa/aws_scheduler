from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def select_tag(selected_value, arg, status, srange=24):
    wrapper = """<select name="name_%s_%s" id="id_%s_%s"> """ % (arg, status, arg, status)
    wrapper += """<option value="-1">N/A</option> """
    for i in range(0, srange):
        if i == selected_value:
            wrapper += """<option value="%s" selected >%s</option>""" % (i, i)
        else:
            wrapper += """<option value="%s" >%s</option>""" % (i, i)
    wrapper += """</select>"""
    return mark_safe(wrapper)


@register.simple_tag
def timezone_tag(timezones, selected_value):
    wrapper = """<select name="name_timezone" id="id_timezone"> """
    for timezone in timezones:
        if timezone == selected_value:
            wrapper += """<option value="%s" selected >%s</option>""" % (timezone, timezone)
        else:
            wrapper += """<option value="%s" >%s</option>""" % (timezone, timezone)
    wrapper += """</select>"""
    return mark_safe(wrapper)


register.filter('timezone_tag', timezone_tag)
register.filter('select_tag', select_tag)
