[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_mpt-tool&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_mpt-tool)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_mpt-tool&metric=coverage)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_mpt-tool)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# SoftwareONE MPT Tool

A Python-based migration tool for extensions that standardizes migration execution. It provides a CLI-based interface
to manage both schema and data migrations across multiple backends, ensuring consistent behavior in all environments.

## Documentation

📚 **[Complete Usage Guide](docs/PROJECT_DESCRIPTION.md)**

## Getting started

### Prerequisites

- Docker and Docker Compose plugin (`docker compose` CLI)
- `make`
- [CodeRabbit CLI](https://www.coderabbit.ai/cli) (optional. Used for running review check locally)


### Make targets overview

Common development workflows are wrapped in the `Makefile`. Run `make help` to see the list of available commands.

### How the Makefile works

The project uses a modular Makefile structure that organizes commands into logical groups:

- **Main Makefile** (`Makefile`): Entry point that automatically includes all `.mk` files from the `make/` directory
- **Modular includes** (`make/*.mk`): Commands are organized by category:
  - `common.mk` - Core development commands (build, test, format, etc.)
  - `repo.mk` - Repository management and dependency commands
  - `migrations.mk` - Database migration commands (Only available in extension repositories)
  - `external_tools.mk` - Integration with external tools


You can extend the Makefile with your own custom commands creating a `local.mk` file inside make folder. This file is
automatically ignored by git, so your personal commands won't affect other developers or appear in version control.


### Setup

Follow these steps to set up the development environment:

#### 1. Clone the repository

```bash
git clone <repository-url>
```
```bash
cd mpt-tool
```

#### 2. Create environment configuration

Copy the sample environment file and update it with your values:

```bash
cp .env.sample .env
```

Edit the `.env` file with your actual configuration values. See the [Configuration](#configuration) section for details on available variables.

#### 3. Build the Docker images

Build the development environment:

```bash
make build
```

This will create the Docker images with all required dependencies and the virtualenv.

#### 4. Verify the setup

Run the test suite to ensure everything is configured correctly:

```bash
make test
```

You're now ready to start developing! See [Running the cli](#running-the-cli) for next steps.


## Running the cli

Before running, ensure your `.env` file is populated.

Start the cli:

```bash
make run
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

## Configuration

The following environment variables are typically set in `.env`. Docker Compose reads them when using the Make targets described above.

### Application

| Environment Variable                   | Default                 | Example                                   | Description                                                                               |
|----------------------------------------|-------------------------|-------------------------------------------|-------------------------------------------------------------------------------------------|
| `MPT_API_BASE_URL`                     | `http://localhost:8000` | `https://portal.softwareone.com/mpt`      | SoftwareONE Marketplace API URL                                                           |
| `MPT_API_TOKEN`                        | -                       | eyJhbGciOiJSUzI1N...                      | SoftwareONE Marketplace API Token                                                         |
| `MPT_TOOL_STORAGE_TYPE`                | `local`                 | `airtable`                                | Storage type for MPT tools (local or airtable)                                            |
| `MPT_TOOL_STORAGE_AIRTABLE_API_KEY`    | -                       | patXXXXXXXXXXXXXX                         | Airtable API key for MPT tool storage (required when storage type is airtable)            |
| `MPT_TOOL_STORAGE_AIRTABLE_BASE_ID`    | -                       | appXXXXXXXXXXXXXX                         | Airtable base ID for MPT tool storage (required when storage type is airtable)            |
| `MPT_TOOL_STORAGE_AIRTABLE_TABLE_NAME` | -                       | MigrationTracking                         | Airtable table name for MPT tool storage (required when storage type is airtable)         |
