FROM python:3.14-slim@sha256:51dafde81dbdb6ebde285137a295cf18a47ca95234fe388a343719cb97305b3d

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
