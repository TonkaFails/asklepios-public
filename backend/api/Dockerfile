FROM python:3.9-slim

WORKDIR /app


# e.g.
# docker buildx build --build-arg CHROMA_HOST=xyz --build-arg CHROMA_COLLECTION_NAME=xyz --build-arg INFERENCE_TOKEN=xyz --platform linux/amd64,linux/arm64 --push -t tonkafails/asklepios-backend .
ARG CHROMA_HOST
ARG CHROMA_COLLECTION_NAME
ARG INFERENCE_TOKEN
ENV CHROMA_HOST=${CHROMA_HOST}
ENV CHROMA_COLLECTION_NAME=${CHROMA_COLLECTION_NAME}
ENV INFERENCE_TOKEN=${INFERENCE_TOKEN}
ARG USERNAME
ENV USERNAME=${USERNAME}
ARG PASSWORD
ENV PASSWORD=${PASSWORD}

ENV CUDA_VISIBLE_DEVICES=""

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY service.py .
COPY controller.py .
COPY embedding_function.py .


EXPOSE 5001

CMD ["python3", "controller.py"]
#CMD ["tail", "-f", "/dev/null"]