#checkov:skip=CKV_DOCKER_2
#checkov:skip=CKV_DOCKER_3
FROM python:3.12-slim@sha256:a3e58f9399353be051735f09be0316bfdeab571a5c6a24fd78b92df85bcb2d85
LABEL com.github.actions.name="contributors" \
    com.github.actions.description="GitHub Action that given an organization or repository, produces information about the contributors over the specified time period." \
    com.github.actions.icon="users" \
    com.github.actions.color="green" \
    maintainer="@zkoppert" \
    org.opencontainers.image.url="https://github.com/github/contributors" \
    org.opencontainers.image.source="https://github.com/github/contributors" \
    org.opencontainers.image.documentation="https://github.com/github/contributors" \
    org.opencontainers.image.vendor="GitHub" \
    org.opencontainers.image.description="GitHub Action that given an organization or repository, produces information about the contributors over the specified time period."

WORKDIR /action/workspace
COPY requirements.txt *.py /action/workspace/

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends git-all=1:2.39.2-1.1 \
    && rm -rf /var/lib/apt/lists/*

CMD ["/action/workspace/contributors.py"]
ENTRYPOINT ["python3", "-u"]
