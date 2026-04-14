# SoftwareONE MPT Tool

`mpt-tool` is the migration toolkit used by SoftwareOne extensions to scaffold, validate, and execute schema and data migrations through the `mpt-service-cli` entry point.

## Documentation

Start here:

- [AGENTS.md](AGENTS.md): entry point for AI agents
- [docs/architecture.md](docs/architecture.md): package structure, execution flow, and storage model
- [docs/contributing.md](docs/contributing.md): repository-specific workflow and validation commands
- [docs/testing.md](docs/testing.md): test scope and quality checks
- [docs/migrations.md](docs/migrations.md): migration lifecycle and repository-specific migration rules
- [docs/documentation.md](docs/documentation.md): repository documentation rules
- [docs/usage.md](docs/usage.md): end-user CLI usage guide and installation instructions

## Quick Start

Prerequisites:

- Docker with the `docker compose` plugin
- `make`

Recommended local setup:

```bash
cp .env.sample .env
make build
make run
```

`make run` opens the container with `mpt-service-cli` available. Use `mpt-service-cli migrate --help` there to inspect supported commands.

## Repository Layout

- [`mpt_tool/`](mpt_tool): CLI, command layer, migration base classes, managers, and use cases
- [`migrations/`](migrations): generated migration scripts for local development and examples
- [`tests/`](tests): pytest suite
- [`make/`](make): modular make targets
- [`docs/`](docs): repository documentation
