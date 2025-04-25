"""Setting up requirements, run `python setup.py install`"""
from setuptools import setup, find_packages


# Function to read the contents of the requirements file
def read_requirements():
    """Get all project requirements from requirements.txt file"""
    with open('requirements.txt', 'r', encoding="utf-8") as req:
        # Exclude any comments or empty lines
        return [line.strip() for line in req if line.strip() and not line.startswith('#')]

def read_readme():
    """Read README file"""
    return "adkbq"
    # with open('README.md', 'r', encoding="utf-8") as readme:
    #     return readme.read()

# Call the function and store the requirements list
install_requires = read_requirements()
long_description = read_readme()

setup(
    name='adkbq',
    version='0.1.0',
    packages=find_packages(),
    description='Wrapper To Create BigQuery Agent For Agents Implemented With ADK',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Viacheslav Kovalevskyi',
    author_email='viacheslav@kovalevskyi.com',
    license='MIT',
    install_requires=install_requires
)