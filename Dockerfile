# Official multi-architecture Python image, pinned to its OCI index digest.
FROM docker.io/library/python:3.13-slim-bookworm@sha256:a5a7017efc5969e00ae2b91c8eb0631049a569652aa4ffc4501769049ae45c72

LABEL io.modelcontextprotocol.server.name="io.github.saddamalsalfi/secure-software-by-design" \
      org.opencontainers.image.title="Secure Software by Design" \
      org.opencontainers.image.source="https://github.com/saddamalsalfi/secure-software-by-design" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="1.1.0"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/tmp
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --require-hashes --only-binary=:all: -r requirements.txt \
    && python -m pip check

COPY server.py pyproject.toml LICENSE ./
COPY skills/secure-software-by-design/ skills/secure-software-by-design/
USER 10001:10001

ENTRYPOINT ["python", "-B", "/app/server.py"]
