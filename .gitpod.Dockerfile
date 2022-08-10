FROM gitpod/workspace-full

USER gitpod

# Install gcloud SDK
ARG GCS_DIR=/opt/google-cloud-sdk
ENV PATH=$GCS_DIR/bin:$PATH
RUN sudo chown gitpod: /opt \
    && mkdir $GCS_DIR \
    && curl -fsSL https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-361.0.0-linux-x86_64.tar.gz \
    | tar -xzvC /opt \
    && /opt/google-cloud-sdk/install.sh --quiet --usage-reporting=true --bash-completion=true --additional-components kubectl

# Install tools for gsutil
RUN sudo install-packages \
    gcc \
    python-dev \
    python-setuptools

RUN bash -c "pip uninstall crcmod; pip install --no-cache-dir -U crcmod"

# Copy gcloud default config
ARG GCLOUD_CONFIG_DIR=/home/gitpod/.config/gcloud
COPY --chown=gitpod gcloud-default-config $GCLOUD_CONFIG_DIR/configurations/config_default

# Set Application Default Credentials (ADC) based on user-provided env var
RUN echo ". /workspace/airbyte/scripts/setup-google-adc.sh" >> ~/.bashrc

# Install latest python 3.9
RUN git clone https://github.com/momo-lab/xxenv-latest.git "$(pyenv root)"/plugins/xxenv-latest \
    && pyenv update \
    && pyenv latest install 3.9 \
    && pyenv latest global 3.9
