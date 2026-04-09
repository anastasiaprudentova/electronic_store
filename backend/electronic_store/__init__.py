# Отключаем CSRF для админки при запуске
from django.views.decorators.csrf import csrf_exempt

def patch_admin():
    try:
        from django.contrib.admin import site
        site.login = csrf_exempt(site.login)
        print("✅ CSRF protection disabled for admin")
    except:
        pass

patch_admin()