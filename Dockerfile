FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

COPY pyproject.toml uv.lock ./mpt_tool/

WORKDIR /mpt_tool

RUN uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH=/opt/venv/bin:$PATH

FROM base AS build

COPY . .

RUN uv sync --frozen --no-cache --all-groups --active

FROM build AS dev

CMD ["bash"]
