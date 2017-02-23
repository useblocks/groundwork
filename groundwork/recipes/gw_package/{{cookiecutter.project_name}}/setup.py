"""
{{cookiecutter.project_name}}
{{ "=" * cookiecutter.project_name|length}}
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('{{cookiecutter.project_slug}}/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='{{cookiecutter.project_slug}}',
    version=version,
    url='http://{{cookiecutter.project_slug}}.readthedocs.org',
    license='{{cookiecutter.license}}',
    author='{{cookiecutter.full_name}}',
    author_email='{{cookiecutter.email}}',
    description="{{cookiecutter.project_short_description}}",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=[],
    tests_require=[],
    install_requires=['groundwork', ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': ["{{cookiecutter.project_slug}} = "
                            "{{cookiecutter.project_slug}}.applications.{{cookiecutter.project_app}}:start_app"],
        'groundwork.plugin': ["{{cookiecutter.project_slug}}_plugin = "
                              "{{cookiecutter.project_slug}}.plugins.{{cookiecutter.project_plugin}}:"
                              "{{cookiecutter.project_plugin}}"],
    }
)
