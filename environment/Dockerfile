# hash:sha256:df25319dc1b6291c01a8d09b9853457048d638a395cf2b29025948e3060041e1
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    hdmf-zarr==0.11.0 \
    numpy==2.2.3 \
    pydantic==2.10.6 \
    pydantic-settings==2.8.1 \
    pynwb==3.0.0

COPY postInstall /
RUN --mount=type=secret,id=secrets . /run/secrets/secrets \
    && /postInstall
