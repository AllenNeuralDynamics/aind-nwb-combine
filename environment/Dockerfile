# hash:sha256:a85dc3fd7fbbbc5e81680470741d6dd67a3107e3ea842fd12efcafedc6134b0e
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

RUN pip install -U --no-cache-dir \
    hdmf-zarr==0.11.0 \
    numpy==2.2.3 \
    pydantic==2.10.6 \
    pydantic-settings==2.8.1 \
    pynwb==3.0.0 \
    -e git+https://github.com/AllenNeuralDynamics/aind-nwb-utils.git@fcce1d4d6d9d4736c58532d88c31ec1989b05e83#egg=aind-nwb-utils

COPY postInstall /
RUN /postInstall
