FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home tester
WORKDIR /work
COPY . .

USER tester
CMD ["bash", "-c", "python3 -m unittest discover -s tests -v && python3 scripts/check_context.py"]
