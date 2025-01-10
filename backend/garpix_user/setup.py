from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpix_user')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpix_user',
    version='3.10.0-rc28',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/garpixcms/garpix_user',
    project_urls={
        'Documentation': 'https://docs.garpixcms.ru/packages/garpix_user/',
        'GitHub': 'https://github.com/garpixcms/garpix_user/',
        'Changelog': 'https://github.com/garpixcms/garpix_user/blob/master/CHANGELOG.md/',
    },
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
        'Django >= 3.1, < 5',
        'djangorestframework >= 3.8',
        'django-oauth-toolkit >= 1.1.2',
        'social-auth-app-django >= 2.1.0',
        'social-auth-core == 4.3.0',
        'django-rest-framework-social-oauth2 == 1.2.0',
        'django-phonenumber-field-for-garpix_user >= 8.0.1',
        'garpix-notify >= 5.17.0rc1',
        'garpix-utils >= 1.10.0-rc24',
        'drf-spectacular >= 0.24.2'
    ]
)
