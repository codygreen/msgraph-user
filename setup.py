from setuptools import setup

setup(
    name='msgraph_user',
    packages=['msgraph_user'],
    description='Package to interact with the Microsoft Graph API User endpoint',
    version='0.1',
    url='http://github.com/codygreen/msgraph_user',
    author='Cody Green',
    author_email='cody@codygreen.com',
    keywords=['pip','msgraph','user'],
    install_requires=[
        'azure-identity',
        'msgraph-sdk'
    ]
    )