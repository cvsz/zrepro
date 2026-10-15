FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

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
