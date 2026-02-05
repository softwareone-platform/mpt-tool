# AI Agent Instructions for mpt-tool

This document provides context and guidelines for AI coding assistants working on the **mpt-tool** project.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Development Workflows](#development-workflows)
- [Code Quality Standards](#code-quality-standards)
- [Environment Variables](#environment-variables)
- [Common Tasks](#common-tasks)
- [Key Principles](#key-principles)
- [Error Handling](#error-handling)
- [Storage Backends](#storage-backends)
- [Additional Resources](#additional-resources)
- [Quick Reference](#quick-reference)
- [Git Conventions](#git-conventions)
- [Notes for AI Assistants](#notes-for-ai-assistants)

## Project Overview

**mpt-tool** is a Python-based CLI migration tool for MPT (SoftwareONE Marketplace Platform) extensions. It provides a standardized way to create, validate, run, and track data and schema migrations across multiple storage backends.

### Key Capabilities
- **Migration scaffolding**: Generate timestamped migration files with pre-built templates
- **Migration execution**: Run data and schema migrations with state tracking
- **Validation**: Check for duplicate migration_id and other structural issues
- **Multiple backends**: Support for local file storage and Airtable
- **Status tracking**: Monitor migration progress and execution state via CLI commands

### Technology Stack
- **Language**: Python 3.12+
- **CLI Framework**: Typer
- **Testing**: pytest with AAA pattern
- **Code Quality**: ruff (primary linter), flake8 + wemake-python-styleguide
- **Type Checking**: mypy with strict annotations
- **Dependency Management**: uv
- **Containerization**: Docker Compose

## Architecture

### Core Components

1. **CLI Layer** (`mpt_tool/cli.py`)
   - Entry point for all user commands
   - Uses Typer for command-line interface
   - Single command: `migrate` with multiple flags (`--check`, `--data`, `--schema`, `--fake`, `--new-data`, `--new-schema`, `--list`)

2. **Commands** (`mpt_tool/commands/`)
   - Command pattern implementation
   - Factory pattern for command instantiation
   - Commands: `check`, `data`, `schema`, `fake`, `list`, `new_data`, `new_schema`
   - Validator for parameter validation

3. **Use Cases** (`mpt_tool/use_cases/`)
   - Business logic layer
   - Use cases: `apply_migration`, `check_migrations`, `list_migrations`, `new_migration`, `run_migrations`
   - Error handling via `UseCaseError`

4. **Migration Base Classes** (`mpt_tool/migration/`)
   - `BaseMigration`: Abstract base for all migrations
   - `DataBaseMigration`: Base class for data migrations
   - `SchemaBaseMigration`: Base class for schema migrations
   - Mixins: `MPTAPIClientMixin`, `AirtableAPIClientMixin`

5. **State Management** (`mpt_tool/managers/`)
   - `FileMigrationManager`: Local file storage backend
   - State managers for Airtable backend
   - JSON encoding/decoding utilities

6. **Configuration** (`mpt_tool/config.py`)
   - All configuration via environment variables
   - No hardcoded values allowed
   - Config getters for Airtable, MPT API, and storage type

### Migration Types

- **Data migrations**: Run after deployment, can take hours/days, executed while MPT is running
  - Examples: updating product parameters, syncing assets with external systems
- **Schema migrations**: Run before deployment, must be fast (<15 min), executed without MPT running
  - Examples: adding Airtable columns, updating table structures

### Migration File Structure
```text
migrations/
  20260113180013_sync_users.py       # Timestamped prefix + user-provided name
  20260214121033_add_columns.py
  ...
```

Each migration file contains a `Migration` class that inherits from `DataBaseMigration` or `SchemaBaseMigration`.

## Development Workflows

### Running Commands
All development workflows are managed via the **makefile**. Always prefer makefile targets:

```bash
make help         # List available commands
make build        # Build Docker images
make bash         # Open bash shell in container
make run          # Run CLI tool
make test         # Run test suite
make check        # Run code quality checks (ruff, flake8, mypy, lockfile)
make check-all    # Run checks + tests
make format       # Auto-format code
make review       # Run CodeRabbit review
make down         # Stop containers
```

### Testing
```bash
make test                              # Run all tests
make test args="-k test_cli -vv"       # Run specific tests with verbose output
make test args="tests/test_cli.py"     # Run specific test file
```

## Code Quality Standards

### Python Conventions

1. **Type Annotations**
   - Required for all code (PEP 484)
   - Exception: tests/ folder does not require type hints
   - Use mypy for validation

2. **Documentation**
   - All public functions, methods, and classes **must** have Google-style docstrings
   - No inline comments - rely on clear code and docstrings
   - Function and variable names must be explicit and intention-revealing

3. **Configuration**
   - All configuration **must** use environment variables
   - No hardcoded values allowed
   - See `mpt_tool/config.py` for patterns

4. **Dependency Versioning** (in `pyproject.toml`)
   - Use `*` for minor versions only
   - ✅ `django==4.2.*`
   - ❌ `django==^4.2.2`

5. **Linting & Formatting**
   - **ruff**: Primary linter for general Python style
   - **flake8**: Runs wemake-python-styleguide and flake8-aaa (for tests)
   - Follow PEP 8 unless overridden by ruff
   - `pyproject.toml` is the source of truth for all rules
   - Generated code must not violate configured rules

### Testing Standards

1. **Framework**: pytest only
2. **Structure**: Tests must be functions, not classes
3. **Naming**: Use `test_` prefix for files and functions
4. **Pattern**: Strictly follow **AAA (Arrange-Act-Assert)** pattern (enforced by flake8-aaa)
5. **No branching**: Do not use `if` statements or branching logic in tests
6. **Fixtures over mocks**: Prefer fixtures; use mocks only when unavoidable
7. **Mocking**:
   - Use `pytest-mock` (`mocker` fixture)
   - Never use `unittest.mock` directly
   - Always use `spec` or `autospec`
8. **Parametrization**: Use `@pytest.mark.parametrize` for testing behavior permutations
9. **No duplication**: Extract shared setup into fixtures

### File Organization
- Tests mirror the source structure: `tests/commands/`, `tests/use_cases/`, etc.
- Each module has a corresponding test file: `cli.py` → `test_cli.py`
- Use `conftest.py` for shared fixtures

## Environment Variables

Required environment variables (see `mpt_tool/config.py`):

### Core Configuration
- `MPT_TOOL_STORAGE_TYPE`: Storage backend (`local` or `airtable`, default: `local`)

### Airtable Storage (when `MPT_TOOL_STORAGE_TYPE=airtable`)
- `MPT_TOOL_STORAGE_AIRTABLE_API_KEY`: Airtable API key (required)
- `MPT_TOOL_STORAGE_AIRTABLE_BASE_ID`: Airtable base ID (required)
- `MPT_TOOL_STORAGE_AIRTABLE_TABLE_NAME`: Table name (default: `Migrations`)

### MPT API Integration (when using `MPTAPIClientMixin`)
- `MPT_API_TOKEN`: MPT API key (required)
- `MPT_API_BASE_URL`: MPT API base URL (required)

## Common Tasks

### Adding a New CLI Command

1. Create a command class in `mpt_tool/commands/` inheriting from `BaseCommand`
2. Implement `run()`, `start_message`, `success_message`, and `name` properties
3. Update `CommandFactory.get_instance()` to handle the new parameter
4. Update `MigrateCommandValidator.validate()` if needed
5. Add CLI parameter to `migrate()` function in `cli.py`
6. Write tests in `tests/commands/`

### Adding a New Use Case

1. Create use case in `mpt_tool/use_cases/`
2. Define clear input/output contracts
3. Raise `UseCaseError` for business logic errors
4. Document with Google-style docstrings
5. Write comprehensive tests with AAA pattern

### Adding a New Migration Mixin

1. Create mixin in `mpt_tool/migration/mixins/`
2. Add necessary configuration getters in `config.py`
3. Document required environment variables
4. Export from `mpt_tool/migration/mixins/__init__.py`
5. Update documentation with usage examples

### Modifying State Management

1. Changes should support both local and Airtable backends
2. Ensure backward compatibility with existing state files
3. Update migration state model in `mpt_tool/models.py`
4. Add migration logic if state format changes

## Key Principles

1. **Maintainability**: Write code that is easy to read and modify
2. **Predictability**: Avoid clever or compact implementations; prefer explicit code
3. **Simplicity**: Simple solutions over complex ones
4. **Configuration**: All config via environment variables
5. **Testing**: Comprehensive test coverage with AAA pattern
6. **Type Safety**: Use type annotations everywhere (except tests)
7. **Documentation**: Google-style docstrings for all public APIs

## Error Handling

- **CLI Layer**: Use `typer.BadParameter` and `typer.Abort`
- **Commands Layer**: Catch use case errors and display user-friendly messages
- **Use Cases Layer**: Raise `UseCaseError` with descriptive messages
- **Migration Layer**: Log errors and let use cases handle them

## Storage Backends

### Local Storage
- State stored in `.migrations-state.json` in project root
- Suitable for development and testing
- No external dependencies

### Airtable Storage
- State stored in Airtable table with columns: `order_id`, `migration_id`, `started_at`, `applied_at`, `type`
- Recommended for production
- Allows tracking across multiple deployments
- Requires `AIRTABLE_API_KEY` and table configuration

## Additional Resources

- **Complete Usage Guide**: `docs/PROJECT_DESCRIPTION.md`
- **README**: High-level overview and quick start
- **Code Quality Config**: `pyproject.toml` (ruff, flake8, pytest settings)
- **Makefile**: All available development commands
- **Migration Examples**: `migrations/` folder

## Quick Reference

### Create New Migration
```bash
mpt-tool migrate --new-data "sync_users"    # Data migration
mpt-tool migrate --new-schema "add_columns" # Schema migration
```

### Run Migrations
```bash
mpt-tool migrate --check   # Validate migrations
mpt-tool migrate --data    # Run data migrations
mpt-tool migrate --schema  # Run schema migrations
mpt-tool migrate --list    # List all migrations
mpt-tool migrate --fake migration_id  # Mark as applied without running
```

### Development
```bash
make build      # Build images
make bash       # Open shell
make test       # Run tests
make check      # Run linters
make format     # Auto-format code
```

## Git Conventions

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for all commit messages.

**Format:**
```text
<type>: <subject>
```

**Commit Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, no logic change)
- `refactor` - Code refactoring (no feature or bug fix)
- `perf` - Performance improvements
- `test` - Adding or updating tests
- `chore` - Maintenance tasks (dependencies, build, etc.)
- `ci` - CI/CD pipeline changes

**Examples:**
```text
feat: add rollback command for migrations
fix: handle missing state file gracefully
docs: update AGENTS.md with git conventions
test: add coverage for check command validation
chore: update dependencies to latest versions
```

**Guidelines:**
- Use imperative mood ("add" not "added" or "adds")
- Keep subject line under 72 characters
- Capitalize first letter of subject
- No period at end of subject line
- Be specific and descriptive

### Pull Requests

**PR Title Format:**
- Follow conventional commit format: `<type>: <description>`
- Use the most significant change as the type
- Be descriptive and specific

**Before Submitting:**
- Run `make check-all` to ensure all checks pass
- Verify all tests pass locally
- Review your own changes first
- Update documentation if needed
- Add or update tests for new functionality

**PR Best Practices:**
- Keep PRs focused on a single feature or fix
- Aim for under 500 lines of changes
- Split large features into smaller, reviewable PRs
- Each PR should be independently deployable when possible
- Keep your branch up to date with main
- Address review comments promptly
- Resolve all conversations before merging

**Review Requirements:**
- At least two approvals required
- Code owner approval for significant changes
- All CI/CD checks must pass (tests, linting, coverage)
- All conversations must be resolved
- Squash commits when merging

## Notes for AI Assistants

When working on this project, always:

- **Check the makefile first** for available commands - don't suggest manual Docker commands
- **Run `make check` after code changes** to validate quality before committing
- **Use conventional commit format** when describing changes or suggesting commits
- **Follow the AAA pattern** strictly in tests (enforced by flake8-aaa)
- **Never hardcode configuration** - always use environment variables via `config.py`
- **Add type annotations** to all production code (not required in tests/)
- **Write Google-style docstrings** for all public functions, methods, and classes
- **Follow existing patterns** - review similar code before implementing new features
- **Use Docker Compose** for all operations via makefile targets
- **Respect exclusions** - migrations in `migrations/` folder are user-generated and excluded from linting

When suggesting changes:
- Provide specific file paths and function names
- Explain the reasoning behind the change
- Consider backward compatibility
- Mention if tests need to be updated
- Note if documentation needs updates


---

**Last Updated**: February 5, 2026
**Maintainer**: SoftwareOne AG
