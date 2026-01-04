# LightX2V RunPod Serverless Worker
# Model loaded from Network Volume (not baked into image)

FROM lightx2v/lightx2v:25111101-cu128

WORKDIR /

# Install RunPod SDK
RUN pip install runpod requests

# Copy handler only (no model download - use Network Volume)
COPY handler.py /handler.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "/handler.py"]
