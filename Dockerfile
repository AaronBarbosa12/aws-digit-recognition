ARG FUNCTION_DIR="/function"

FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-training:2.12.0-cpu-py310-ubuntu20.04-ec2 as build-image

ARG FUNCTION_DIR

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

RUN mkdir -p ${FUNCTION_DIR}
COPY app/ ${FUNCTION_DIR}/


RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-training:2.12.0-cpu-py310-ubuntu20.04-ec2

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD [ "app.handler" ]
