"""
LightX2V RunPod Serverless Handler
Wan2.1 Image-to-Video Generation with 4-step Distillation
~20x faster than standard inference
"""

import runpod
import os
import base64
import requests
import uuid

# Global - model loads once on cold start
pipe = None


def download_image(url):
    """Download image from URL to temp file"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    ext = url.split('.')[-1].split('?')[0].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
        ext = 'jpg'

    temp_path = f"/tmp/input_{uuid.uuid4().hex}.{ext}"
    with open(temp_path, 'wb') as f:
        f.write(response.content)

    return temp_path


def load_model():
    """Load model (only on first call)"""
    global pipe

    if pipe is not None:
        return pipe

    print("Loading LightX2V Wan2.1 model...")

    from lightx2v import LightX2VPipeline

    model_path = os.environ.get("MODEL_PATH", "/models/wan2.1-i2v-480p-distill")

    pipe = LightX2VPipeline(
        model_path=model_path,
        model_cls="wan2.1_distill",
        task="i2v",
    )

    pipe.create_generator(
        attn_mode="sage_attn2",
        infer_steps=4,  # Distilled: only 4 steps needed!
        height=480,
        width=832,
        num_frames=81,  # ~5 sec video @ 16fps
        guidance_scale=5.0,
        sample_shift=5.0,
    )

    print("Model loaded successfully!")
    return pipe


def handler(job):
    """
    RunPod Handler for Wan2.1 I2V

    Input:
        - prompt: str - Video description
        - image_url: str - Input image URL
        - negative_prompt: str (optional)
        - seed: int (optional, default: 42)

    Output:
        - video_base64: str - Base64 encoded MP4 video
        - seed: int
        - status: str
    """
    try:
        job_input = job["input"]

        # Get parameters
        prompt = job_input.get("prompt", "")
        negative_prompt = job_input.get("negative_prompt", "")
        image_url = job_input.get("image_url")
        seed = job_input.get("seed", 42)

        # Validate required params
        if not image_url:
            return {"error": "image_url is required", "status": "failed"}

        if not prompt:
            return {"error": "prompt is required", "status": "failed"}

        # Load model
        model = load_model()

        # Download input image
        print(f"Downloading image: {image_url}")
        input_image_path = download_image(image_url)

        # Generate video
        output_path = f"/tmp/output_{uuid.uuid4().hex}.mp4"

        print(f"Generating video - prompt: {prompt[:50]}...")
        model.generate(
            seed=seed,
            prompt=prompt,
            negative_prompt=negative_prompt,
            input_image=input_image_path,
            save_result_path=output_path,
        )

        # Read and encode video
        with open(output_path, "rb") as f:
            video_base64 = base64.b64encode(f.read()).decode("utf-8")

        # Cleanup temp files
        os.remove(input_image_path)
        os.remove(output_path)

        print("Video generated successfully!")

        return {
            "video_base64": video_base64,
            "seed": seed,
            "status": "success"
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "status": "failed"}


# Start RunPod Serverless
runpod.serverless.start({"handler": handler})
