[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_mpt-tool&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_mpt-tool)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_mpt-tool&metric=coverage)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_mpt-tool)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# SoftwareONE MPT Tool

A Python-based migration tool for extensions that standardizes migration execution. It provides a CLI-based interface
to manage both schema and data migrations across multiple backends, ensuring consistent behavior in all environments.

## Getting started

### Prerequisites

- Docker and Docker Compose plugin (`docker compose` CLI)
- `make`
- [CodeRabbit CLI](https://www.coderabbit.ai/cli) (optional. Used for running review check locally)

### Make targets overview

Common development workflows are wrapped in the `makefile`:

- `make help` – list available commands
- `make bash` – start the app container and open a bash shell
- `make build` – build the application image for development
- `make check` – run code quality checks (ruff, flake8, lockfile check)
- `make check-all` – run checks, formatting, and tests
- `make format` – apply formatting and import fixes
- `make down` – stop and remove containers
- `make review` –  check the code in the cli by running CodeRabbit
- `make run` – run the CLI tool
- `make test` – run the test suite with pytest

## Running CLI commands

Run the CLI tool:
```bash
make run
```

## Running tests

Tests run inside Docker using the dev configuration.

Run the full test suite:

```bash
make test
```

Pass additional arguments to pytest using the `args` variable:

```bash
make test args="-k test_cli -vv"
make test args="tests/test_cli.py"
```

## Developer utilities

Useful helper targets during development:

```bash
make bash      # open a bash shell in the app container
make check     # run ruff, flake8, and lockfile checks
make check-all # run checks and tests
make format    # auto-format code and imports
make review    # check the code in the cli by running CodeRabbit
```
