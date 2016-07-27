from setuptools import setup, find_packages

setup(
    name='ITF',
    version='0.1',
    description='TaekwonDo competition portal',
    long_description=__doc__,
    url='https://github.com/valasek/taekwondo',
    license='GPL 3.0',
    author='Stanislav Valasek',
    author_email='valasek@gmail.com',
    install_requires=[
        'blinker>=1.4',
        'click>=6.6',
        'Flask>=0.11.1',
        'Flask-DebugToolbar>=0.10.0',
        'Flask-SQLAlchemy>=2.1',
        'itsdangerous>=0.24',
        'Jinja2>=2.8',
        'jsonify>=0.5',
        'MarkupSafe>=0.23',
        'SQLAlchemy>=1.0.14',
        'Werkzeug>=0.11.10',
        'WTForms>=2.1',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: Beta',
        'Environment :: Web Environment',
        'Intended Audience :: End Users',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)