# hash:sha256:6711ab678cb7e07061a38b543091c3424e72b00316ea830fb687accf5577bfdb
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
    pydantic==2.10.6 \
    pydantic-settings==2.8.1 \
    pynwb==3.0.0 \
    -e git+https://github.com/AllenNeuralDynamics/aind-nwb-utils.git@fcce1d4d6d9d4736c58532d88c31ec1989b05e83#egg=aind-nwb-utils

ADD "https://github.com/coder/code-server/releases/download/v4.95.3/code-server-4.95.3-linux-amd64.tar.gz" /.code-server/code-server.tar.gz
	
RUN cd /.code-server \
    && tar -xvf code-server.tar.gz \
    && rm code-server.tar.gz \
    && ln -s /.code-server/code-server-4.95.3-linux-amd64/bin/code-server  /usr/bin/code-server

RUN mkdir -p /.vscode/extensions \
    && code-server --extensions-dir="/.vscode/extensions" --install-extension REditorSupport.R \
    && code-server --extensions-dir="/.vscode/extensions" --install-extension continue.continue \
    && code-server --extensions-dir="/.vscode/extensions" --install-extension ms-python.python \
    && code-server --extensions-dir="/.vscode/extensions" --install-extension ms-toolsai.jupyter \
    && code-server --extensions-dir="/.vscode/extensions" --install-extension reageyao.bioSyntax \
    && code-server --extensions-dir="/.vscode/extensions" --install-extension saoudrizwan.claude-dev

COPY postInstall /
RUN /postInstall
