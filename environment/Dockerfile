# hash:sha256:d6599cab75b4e2642fbf5ca77085bd82bc1f7a71e164ff4fcd89cfc197c2713d
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        vim=2:8.2.3995-1ubuntu2.23 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U --no-cache-dir \
    hdmf-zarr==0.11.0 \
    numpy==2.2.3 \
    pydantic \
    pydantic-settings \
    pynwb==3.0.0 \
    -e git+https://github.com/AllenNeuralDynamics/aind-nwb-utils.git#egg=aind-nwb-utils

COPY postInstall /
RUN /postInstall
