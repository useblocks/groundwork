"""
groundwork
"""
import re
from setuptools import setup, find_packages

version = 0.1

setup(
    name='groundwork',
    version=version,
    url='https://groundwork.useblocks.com',
    license='MIT',
    author='Team useblocks',
    author_email='info@useblocks.com',
    description=" groundworkdesc",
    long_description="plugin description",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=["click", "blinker"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'gw_start = groundwork:go',
        ],
        'groundwork.plugin': [
            'gw_plugin_info = groundwork.plugins.gw_plugin_info:GwPluginInfo',
            'gw_signal_info = groundwork.plugins.gw_signal_info:GwSignalInfo',
            'gw_command_info = groundwork.plugins.gw_commands_info:GwCommandInfo'
        ]
    }
)
