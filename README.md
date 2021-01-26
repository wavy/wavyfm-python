# wavyfm-python

**The client library for [wavy.fm](https://wavy.fm), officially maintained by Wavy Labs.**

![Tests](https://github.com/wavy/wavyfm-python/workflows/Tests/badge.svg)

## Documentation

> Coming soon!

## Installation

This library is built with Python 3.8. You can install it from pypi:

```bash
pip install wavyfm
```

## Quick Start

To get started, install the `wavyfm` package and create an app on https://wavy.fm/developers/apps. Add your client ID
and client secret to your environment variables:

```
WAVYFM_CLIENT_ID='pub_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
WAVYFM_CLIENT_SECRET='priv_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

## Without user authentication

```python
import wavyfm

# Create the client
wavy = wavyfm.WavyClient(auth=wavyfm.WavyClientCredentials())

# Get the total listens recorded on wavy.fm
print(wavy.metrics.get_total_listens())
```

## License

This project is licenced under the MIT License.

The overall structure is heavily inspired from [Spotipy](https://github.com/plamere/spotipy), a client library for
Spotify.
