# hash:sha256:0ddbb01ce0ce20389d22216d6f13359f81a8978c2f6aad370677d4cbde9b2722
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG API_KEY
ARG API_SECRET
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY

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
    pydantic==2.10.6 \
    pydantic-settings==2.8.1 \
    pynwb==3.0.0 \
    -e git+https://github.com/AllenNeuralDynamics/aind-nwb-utils.git@fcce1d4d6d9d4736c58532d88c31ec1989b05e83#egg=aind-nwb-utils

COPY postInstall /
RUN /postInstall
