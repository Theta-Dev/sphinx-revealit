from setuptools import find_packages, setup

with open('README.rst') as f:
    readme_text = f.read()

setup(
    name='sphinx_revealit',
    version='0.1.0',
    py_modules=[],
    url='https://www.github.com/Theta-Dev/sphinx-revealit',
    license='Apache-2.0',
    author='ThetaDev',
    description='Sphinx extension with theme to generate Reveal.js presentation',
    long_description=readme_text,
    long_description_content_type='text/x-rst',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'docutils',
        'pygments',
        'sphinx',
        'importlib_resources'
    ],
    include_package_data=True,
    classifiers=[
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Framework :: Sphinx :: Theme',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Multimedia :: Graphics :: Presentation'
    ],
    python_requires='>=3.6',
)
