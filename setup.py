from setuptools import setup

setup(
    name='unfi_api',
    version='',
    packages=['QueryGui', 'QueryGui.pages', 'QueryGui.widgets', 'unfi_api', 'unfi_api.tests', 'unfi_api.tests.Product',
              'unfi_api.utils', '', 'tests', 'tests.Product', 'utils'],
    package_dir={'': 'unfi_api'},
    url='',
    license='',
    author='Administrator',
    author_email='',
    description='',
    install_requires=['openpyxl', 'xlrd', 'titlecase', 'bs4',
                      'requests', 'mock', 'future', 'tqdm', 'psutil', 'selenium', 'selenium-requests'],

)
