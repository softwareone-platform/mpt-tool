FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

COPY . /mpt_tool
WORKDIR /mpt_tool

RUN uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH=/opt/venv/bin:$PATH

RUN uv sync --frozen --no-cache --all-groups --active

CMD ["bash"]
