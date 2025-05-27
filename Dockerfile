#checkov:skip=CKV_DOCKER_2
#checkov:skip=CKV_DOCKER_3
FROM python:3.13-slim@sha256:56a11364ffe0fee3bd60af6d6d5209eba8a99c2c16dc4c7c5861dc06261503cc
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
    && apt-get -y install --no-install-recommends git=1:2.39.5-0+deb12u2 \
    && rm -rf /var/lib/apt/lists/*

CMD ["/action/workspace/contributors.py"]
ENTRYPOINT ["python3", "-u"]
