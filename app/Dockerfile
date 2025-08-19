# The image contains 2 high vulnerabilities:
# https://hub.docker.com/layers/library/python/3.10-slim/images/sha256-e3c437eb1623e9086f42038c1273a7eff09cfff44d7c2ece721fa61560af7e1f

FROM python:3.10-slim

WORKDIR /app

COPY signal_generator.py .

RUN pip install numpy

CMD ["python", "signal_generator.py"]
