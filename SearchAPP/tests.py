from django.test import TestCase

# Create your tests here.

from SearchAPP import globalvar as gl

from SearchAPP import views

def get_user():

    gl_dict = gl.get_all()    # 获取全部
    user = gl.get_value('urllist')     # 获取单个 
    print(gl_dict, user)	# {'username': 'admin'}  admin
    
get_user()
