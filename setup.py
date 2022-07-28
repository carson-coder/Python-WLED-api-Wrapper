from distutils.core import setup
import json
data = json.load(open('./wled/config.json'))
setup(name='WLED_light_controller',
      version=f"{data['version']}: {(int(data['status']) * 'stable') + (int(not(data['status'])) * 'beta')}",
      description='A small WLED light controller in Python',
      author="Carson Coder",
      author_email="carsondpool@gmail.com",
      url='https://github.com/carson-coder/Python-WLED-api-Wrapper',
      packages=['requests', 'json'],
     )