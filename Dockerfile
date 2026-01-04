# LightX2V RunPod Serverless Worker
# Wan2.1 Image-to-Video Generation with 4-step Distillation

FROM lightx2v/lightx2v:25111101-cu128

WORKDIR /

# Install RunPod SDK and dependencies
RUN pip install runpod requests

# Create model directory
RUN mkdir -p /models

# Download Wan2.1 I2V 480P Distilled Model (4-step fast version)
# This is ~30GB, will take some time on first build
RUN huggingface-cli download lightx2v/Wan2.1-I2V-14B-480P-StepDistill-CfgDistill-Lightx2v \
    --local-dir /models/wan2.1-i2v-480p-distill

# Copy handler
COPY handler.py /handler.py

# Environment variables
ENV MODEL_PATH=/models/wan2.1-i2v-480p-distill
ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "/handler.py"]
