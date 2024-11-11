FROM python:3.13-bookworm

WORKDIR /3d_tag_creator

RUN apt-get update
RUN apt-get install -y wget libgl1-mesa-glx fontconfig

# install fonts
RUN apt-get install fonts-liberation
# add additional fonts here
RUN fc-cache -vr

# install miniconda
ENV CONDA_DIR /opt/conda
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"; \
    elif [ "$arch" = "aarch64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"; \
    else \
    echo "Unsupported architecture: $arch"; \
    exit 1; \
    fi && \
    wget $MINICONDA_URL -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm -f miniconda.sh

ENV PATH=$CONDA_DIR/bin:$PATH

# install cadquery via conda
RUN conda install -y -c cadquery -c conda-forge cadquery=master

# copy and install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy folders
COPY static/ static/
COPY templates templates/
COPY *.py .

# create tmp dir
RUN mkdir tmp

# install gunicorn
RUN pip3 install gunicorn

CMD ["gunicorn", "--config", "gunicorn.config.py", "wsgi:app"]
