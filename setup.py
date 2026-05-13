from setuptools import setup
APP = ['rajnish_hz_meter.py']
OPTIONS = {'argv_emulation': True, 'plist': {'CFBundleName': 'Rajnish SafeGuard AI'}}
setup(app=APP, options={'py2app': OPTIONS}, setup_requires=['py2app'])
