import os
import sys

# Ensure project root is in path
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv.settings')
import django
django.setup()

from django.template.loader import get_template
from django.template import TemplateSyntaxError

TEMPLATES_DIR = os.path.join(BASE, 'main', 'templates', 'main')
print('Checking templates in', TEMPLATES_DIR)
errors = []
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for f in files:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), os.path.join(BASE, 'templates'))
            tpl_name = os.path.relpath(os.path.join(root, f), os.path.join(BASE, 'main', 'templates'))
            tpl_name = os.path.join('main', os.path.relpath(os.path.join(root, f), TEMPLATES_DIR))
            tpl_name = tpl_name.replace('\\\\', '/').replace('\\', '/')
            print('->', tpl_name)
            try:
                get_template(tpl_name)
            except Exception as e:
                errors.append((tpl_name, repr(e)))

print('\nDone. Errors:')
for tpl, err in errors:
    print(tpl, err)

if not errors:
    print('No template errors detected.')
