FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home tester
WORKDIR /work
COPY . .

USER tester
# Build the shim cache now. The build has network. The run has none and a read-only root.
RUN python3 -c "import sys; sys.path.insert(0, 'scripts'); import check_context as c; s, k = c.pinned(); c.ensure_environment(s, k)"
CMD ["bash", "-c", "python3 -m unittest discover -s tests -v && python3 scripts/check_context.py"]
