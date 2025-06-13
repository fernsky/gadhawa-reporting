"""
Quick script to create basic app structures
"""

import os

apps = ['social', 'environment', 'infrastructure', 'governance', 'reports', 'demographics']

for app in apps:
    app_dir = f'apps/{app}'
    
    # Create __init__.py
    with open(f'{app_dir}/__init__.py', 'w') as f:
        f.write('')
    
    # Create apps.py
    with open(f'{app_dir}/apps.py', 'w') as f:
        f.write(f"""from django.apps import AppConfig


class {app.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
    verbose_name = '{app.capitalize()}'
""")
    
    # Create models.py
    with open(f'{app_dir}/models.py', 'w') as f:
        f.write(f'# {app.capitalize()} models will be defined here after user confirmation\n')
    
    # Create urls.py
    with open(f'{app_dir}/urls.py', 'w') as f:
        f.write(f"""from django.urls import path

app_name = '{app}'
urlpatterns = []
""")

print("All app structures created!")
