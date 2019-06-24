from django import template
import requests
from bs4 import BeautifulSoup

register = template.Library()




def testmessage():
    return "1"


register.simple_tag(testmessage)


