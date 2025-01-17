FROM python:3

RUN pip3 install --no-cache-dir --upgrade canvaslms && \
  activate-global-python-argcomplete && \
  register-python-argcomplete canvaslms > /etc/bash_completion.d/canvaslms.bash
