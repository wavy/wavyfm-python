from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

test_reqs = [
    'mock==2.0.0'
]

doc_reqs = [
]

extra_reqs = {
    'doc': doc_reqs,
    'test': test_reqs
}

setup(
    name='wavyfm',
    version='1.0.0',
    description='Official Python library for wavy.fm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="@aramperes",
    author_email="aram.peres@wavy.fm",
    url='https://wavy.fm/developers',
    install_requires=[
        'requests>=2.20.1'
    ],
    tests_require=test_reqs,
    extras_require=extra_reqs,
    license='LICENSE.md',
    packages=['wavyfm'])
