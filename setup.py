from distutils.core import setup
import json
data = json.load(open('./wled/config.json'))
setup(name='WLED_light_controller',
      version=f"{data['version']}",
      description='A small WLED light controller in Python',
      author="Carson Coder",
      author_email="carsondpool@gmail.com",
      url='https://github.com/carson-coder/Python-WLED-api-Wrapper',
      license="LICENSE",
      long_description=open('README.md').read(),
      py_modules=['requests', 'json'],
     )