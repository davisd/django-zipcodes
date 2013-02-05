from distutils.core import setup

setup(
    name='django-zipcodes',
    version='1.0',
    author='David Davis',
    author_email='davisd@davisd.com',
    packages=['zipcodes',],
    url='http://github.com/davisd/django-zipcodes/',
    data_files=[('.',['LICENSE'])],
    license='LICENSE',
    description='django-zipcodes is a very simple django zipcode library.',
    long_description=open('README').read(),
)

