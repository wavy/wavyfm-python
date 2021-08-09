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
    version='1.0.3',
    description='Official Python library for wavy.fm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aram Peres",
    author_email="aram.peres@wavy.fm",
    url='https://wavy.fm/developers',
    project_urls={
        'Documentation': 'https://github.com/wavy/wavyfm-python',
        'Source': 'https://github.com/wavy/wavyfm-python',
    },
    install_requires=[
        'requests>=2.26.0'
    ],
    tests_require=test_reqs,
    extras_require=extra_reqs,
    license='LICENSE.md',
    packages=['wavyfm'])
