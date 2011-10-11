from setuptools import setup, find_packages

setup(
        name='django-mailchange',
        version='0.0.1',
        description='Chanve user\'s email addresses via verification email',
        long_description=open('README.rst').read(),
        author=u'Jesús Del Carpio',
        author_email='jjdelc@gmail.com',
        url='https://github.com/jjdelc/Django-Mailchange',
        license='BSD',
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )


