# Contributing

Thanks for your interest in contributing to the wavy.fm Python library! The project is still in its early stages, so we
apologize if this document is skipping some important stuff. If you have any questions, you can reach out via the GitHub
issues on this repository, or through [Discord](https://wavy.fm/discord).

This project is maintained officially by wavy.fm and by the Developer Working Group.

## Creating environment

You can use either `pipenv` or `virtualenv` to initialize the developer environment. I personally prefer pipenv for
this.

```bash
# Pipenv creates the environment and fetches the dependencies
pipenv install --dev
pipenv shell
```

```bash
# Alternatively, using virtualenv
virtualenv venv
./venv/bin/activate
pip install -e .
pip install mock==2.0.0 flake8
```

## Run tests

To run the unit tests and lint, use

```bash
# With pipenv
pipenv run tests
pipenv run lint

# With virtualenv
python -m unittest discover -v tests
flake8 . --count --show-source --statistics
```

## Integration tests

Some tests require valid app credentials to run, and are not run in CI. To enable them, set these in your environment
variables (substituting with valid credentials):

```bash
WAVYFM_RUN_INTEGRATION_TESTS=1
WAVYFM_CLIENT_ID='pub_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
WAVYFM_CLIENT_SECRET='priv_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

Then run the tests like described before.
