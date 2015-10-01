from setuptools import setup

setup(
    name='django-slack',
    version='3',
    packages=['django_slack'],
    include_package_data=True,
    url='https://chris-lamb.co.uk/projects/django-slack',
    license='BSD License',
    author='Chris Lamb',
    author_email='chris@chris-lamb.co.uk',
    description='Provides easy-to-use integration between Django projects and the Slack group chat and IM tool.',
    install_requires=[
        'Django>=1.6.8',
        'requests',
    ],
)
