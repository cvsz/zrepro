FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY services/mcp /app/services/mcp
COPY catalog /app/catalog
COPY schemas /app/schemas
COPY skills /app/skills
COPY fixtures /app/fixtures

RUN python -m pip install --upgrade pip && \
    python -m pip install /app/services/mcp && \
    useradd --create-home --uid 10001 --shell /usr/sbin/nologin zrepro && \
    chown -R zrepro:zrepro /app

USER 10001:10001

ENV ZREPRO_ROOT=/app \
    ZREPRO_MCP_HOST=0.0.0.0 \
    ZREPRO_MCP_PORT=8787

EXPOSE 8787

ENTRYPOINT ["zrepro-mcp"]
