FROM python

RUN pip install sysv_ipc
ADD *.py /
