from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      python_requires='>=3.9',
      version='1',
      description='package of file sorting',
      url='https://github.com/dCrowb/Python_course_HW_7.0.git',
      author='Oleksandr Shevchenko',
      author_email='oishevchenko94@gmail.com',
      license='oishevchenko',
      packages=find_namespace_packages(),
      install_requires=['patool==1.12'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:start']})