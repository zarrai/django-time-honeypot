from setuptools import setup, find_packages

version = __import__('honeypot').__version__

setup(
    name = 'django-time-honeypot',
    version = version,
    description = 'django-honeypot with time restriction',
    author = 'zarrai',
    url = 'https://github.com/zarrai/django-time-honeypot',
    packages = find_packages(),
    zip_safe=False,
        package_data={
        'honeypot': [
            'templates/honeypot/*.html',
        ],
    }
)