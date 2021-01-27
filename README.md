<p align="center">
  <br />
  <a href="https://wavy.fm" target="_blank" align="center">
    <img src="https://wavy.fm/_assets/wavy-logo.png" width="280">
  </a>
  <br />
</p>

# wavyfm-python

**The Python client library for [wavy.fm](https://wavy.fm), officially maintained by Wavy Labs.**

![Tests](https://github.com/wavy/wavyfm-python/workflows/Tests/badge.svg) [![wavyfm on pypi](https://img.shields.io/pypi/v/wavyfm)](https://pypi.org/project/wavyfm/) [![Discord](https://img.shields.io/discord/742178434243100752?color=%237289DA&label=discord)](https://wavy.fm/discord)

## Documentation

All endpoints are documented in the [wavy.fm developer docs](https://wavy.fm/developers). You can contribute to the docs
and suggest API changes in the corresponding [Github repository](https://github.com/wavy/wavyfm-docs/).

> Client library documentation coming soon!

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
wavy = wavyfm.WavyClient(auth_manager=wavyfm.WavyClientCredentials())

# Get the total listens recorded on wavy.fm
print(wavy.metrics.get_total_listens())

# Get the total amount of registered users on wavy.fm
print(wavy.metrics.get_total_users())

# Get the top 10 registered users on wavy.fm by listen count
print(wavy.metrics.get_user_listens_leaderboard())

# Get a user's public profile
print(wavy.users.by_username("Aram").get_profile())

# Get a user's total listens
print(wavy.users.by_username("Aram").get_total_listens())

# Get a user's total artists
print(wavy.users.by_username("Aram").get_total_artists())

# Get a user's currently listening track
print(wavy.users.by_username("Aram").get_currently_listening())

# Get a user's last 10 recorded listens
print(wavy.users.by_username("Aram").get_recent_listens(10))
```

## License

This project is licenced under the MIT License.

The overall structure is heavily inspired from [Spotipy](https://github.com/plamere/spotipy), a client library for
Spotify.
