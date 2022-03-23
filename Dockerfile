FROM python:latest
COPY main.py /
COPY algorithm_tests.py /
COPY data_cases /data_cases
# Switch comments on the following lines to run tests.
ENTRYPOINT ["python", "./main.py"]
# ENTRYPOINT ["python", "./algorithm_tests.py"]