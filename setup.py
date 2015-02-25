from setuptools import setup

setup(
    name='django-slack',
    version='0.0.1',
    packages=['django_slack'],
    url='https://github.com/lamby/django-slack',
    license='BSD',
    author='Chris Lamb',
    author_email='chris@chris-lamb.co.uk',
    description='Provides easy-to-use integration between Django projects and the Slack group chat and IM tool.',
    install_requires=['Django>=1.6.8', 'requests']
)
