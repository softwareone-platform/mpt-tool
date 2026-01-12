FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

COPY pyproject.toml uv.lock README.md ./mpt_tool/

WORKDIR /mpt_tool

RUN uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH=/opt/venv/bin:$PATH

FROM base AS build

RUN uv sync --frozen --no-cache --all-groups --active

COPY . .

FROM build AS dev

CMD ["bash"]
