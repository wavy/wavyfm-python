# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

No changes

## [1.0.2] - 2021-03-26
### Added
- Added utility for parsing wavy.fm date strings (RFC3339): `wavyfm.util.datetime_from_string` (GH-5)
- Added __repr__ to `wavfym.users._WavyProfileEndpoints`

## [1.0.1] - 2021-01-25
### Fixes
- Fix setup.py project metadata

## [1.0.0] - 2021-01-25
### Added
- Authentication through Client Credentials
- v1beta metrics: get total listens
- v1beta metrics: get total users
- v1beta metrics: get user listens leaderboard
- v1beta users: get user by username, user ID, discord ID, and URI
- v1beta users: get user profile
- v1beta users: get user history stats (total listens, total artists)
- v1beta users: get recently played
- v1beta users: get currently playing
