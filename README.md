# LightX2V RunPod Serverless Worker

Wan2.1 Image-to-Video generation with **4-step distillation** - up to **20x faster** than standard inference.

## Features

- 🚀 **4-step inference** (vs 50 steps standard) via LightX2V distillation
- 📹 **480P video output** (~5 seconds @ 16fps)
- ⚡ **~1 minute** per video on RTX 4090
- 💰 **~$0.01-0.02** per video (vs $0.20-0.30 on WaveSpeed)

## API Usage

### Input

```json
{
    "input": {
        "prompt": "a beautiful woman smiling and waving",
        "image_url": "https://example.com/image.jpg",
        "negative_prompt": "blurry, low quality",
        "seed": 42
    }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | ✅ | Video description |
| `image_url` | string | ✅ | Input image URL |
| `negative_prompt` | string | ❌ | Negative prompt |
| `seed` | int | ❌ | Random seed (default: 42) |

### Output

```json
{
    "video_base64": "AAAAIGZ0eXBpc29...",
    "seed": 42,
    "status": "success"
}
```

## Deployment

### GPU Selection

| GPU | VRAM | Price/hr | Recommended |
|-----|------|----------|-------------|
| **RTX 4090** | 24GB | $0.77 | ✅ Best value |
| **A40** | 48GB | $0.85 | More stable |
| **L40S** | 48GB | $0.99 | Faster |

### Deploy via GitHub

1. Push this repo to your GitHub
2. Go to [RunPod Serverless Console](https://www.runpod.io/console/serverless)
3. Click **New Endpoint** → **Deploy from GitHub**
4. Select this repo
5. Choose **RTX 4090** GPU
6. Set:
   - Active Workers: 0
   - Max Workers: 3-5
   - Idle Timeout: 5s
   - Execution Timeout: 300s

### Test

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "a woman dancing gracefully",
      "image_url": "https://example.com/image.jpg"
    }
  }'
```

## Tech Stack

- [LightX2V](https://github.com/ModelTC/LightX2V) - Lightweight video generation framework
- [Wan2.1-I2V-14B-480P-StepDistill](https://huggingface.co/lightx2v/Wan2.1-I2V-14B-480P-StepDistill-CfgDistill-Lightx2v) - Distilled model
- [RunPod Serverless](https://www.runpod.io/serverless) - GPU serverless platform

## Cost Comparison

| Platform | Cost per video |
|----------|---------------|
| WaveSpeed | $0.20-0.30 |
| Alibaba Cloud API | $0.07 |
| **This worker** | **$0.01-0.02** |

Save **90%+** on video generation costs!
