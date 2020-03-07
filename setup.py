from setuptools import find_packages, setup

setup(
    name='dojo_pandas',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'pandas==0.24.2',
        'plotly==3.10.0',
        'scipy',
        'xlrd',
        'workalendar',
        'Flask-Mail',
        'celery==4.2.2',
        'redis==2.10.6',
        'gunicorn',
        'adal',
        'itsdangerous',
        'pytz',
        'tzlocal'
    ],
)
