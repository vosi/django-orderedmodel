import os
from setuptools import setup
from orderedmodel import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
    name='django-orderedmodel',
    version=".".join(map(str, VERSION)),
    description='Admin models ordering.',
    long_description=readme,
    author="Vladimir 'fon.VoSi' Tartynskyi",
    author_email='fon.vosi@gmail.com',
    url='http://github.com/vosi/django-orderedmodel',
    packages=['orderedmodel'],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    )
