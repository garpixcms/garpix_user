from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpix_user')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpix_user',
    version='3.8.2',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/garpixcms/garpix_user',
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 3.1, < 4',
        'djangorestframework >= 3.8',
        'django-oauth-toolkit >= 1.1.2',
        'social-auth-app-django >= 2.1.0',
        'social-auth-core == 4.3.0',
        'django-rest-framework-social-oauth2 >= 1.1.0',
        'django-phonenumber-field-for-garpix_user >= 8.0.0',
        'garpix-notify >= 5.12.5',
        'garpix-utils >= 1.5.1',
        'drf-spectacular >= 0.24.2'
    ]
)
