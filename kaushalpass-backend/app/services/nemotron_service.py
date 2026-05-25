"""Nemotron 3 Nano Omni — craft video/image analysis."""

from __future__ import annotations

import base64
import json
import re
from typing import Any

import httpx

from app.config import Settings, get_settings
from app.core.exceptions import ServiceError
from app.utils.media_preprocessor import apply_clahe, frame_to_base64_jpeg

CRAFT_ANALYSIS_PROMPT = """
Analyze these frames from a 30-second craft skill video.
Return JSON only: {
  skill_detected: string,
  technique_quality: 1-5,
  hands_visible: boolean,
  active_work: boolean,
  fraud_signals: [],
  confidence: 0.0-1.0
}
"""


def _parse_nemotron_json(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ServiceError("Nemotron did not return JSON", 502)
    parsed: dict[str, Any] = json.loads(text[start : end + 1])
    parsed.setdefault("fraud_signals", [])
    parsed.setdefault("hands_visible", False)
    parsed.setdefault("active_work", False)
    parsed.setdefault("confidence", 0.5)
    return parsed


def _build_vision_messages(frames_b64: list[str], prompt: str) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    for b64 in frames_b64:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
            }
        )
    return [{"role": "user", "content": content}]


async def _call_nemotron(
    frames_b64: list[str],
    *,
    settings: Settings | None = None,
) -> dict[str, Any]:
    s = settings or get_settings()
    if not frames_b64:
        raise ServiceError("No frames to analyze", 400)

    url = f"{s.NVIDIA_API_BASE.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {s.NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": s.NEMOTRON_MODEL,
        "messages": _build_vision_messages(frames_b64, CRAFT_ANALYSIS_PROMPT),
        "temperature": 0.1,
        "max_tokens": 512,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, headers=headers, json=body)
        if response.status_code != 200:
            raise ServiceError(
                f"Nemotron API error {response.status_code}: {response.text[:500]}",
                502,
            )
        data = response.json()

    choices = data.get("choices") or []
    if not choices:
        raise ServiceError("Empty Nemotron response", 502)
    content = choices[0].get("message", {}).get("content", "")
    return _parse_nemotron_json(str(content))


async def analyze_craft_video(
    video_bytes: bytes,
    *,
    max_frames: int = 8,
    settings: Settings | None = None,
) -> dict[str, Any]:
    from app.utils.media_preprocessor import extract_video_frames

    frames = extract_video_frames(video_bytes, max_frames=max_frames)
    if not frames:
        raise ServiceError("Could not extract video frames", 422)

    frames_b64 = [frame_to_base64_jpeg(f) for f in frames]
    return await _call_nemotron(frames_b64, settings=settings)


async def analyze_single_image(
    image_bytes: bytes,
    *,
    settings: Settings | None = None,
) -> dict[str, Any]:
    import cv2
    import numpy as np

    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise ServiceError("Invalid image file", 422)
    b64 = frame_to_base64_jpeg(frame)
    return await _call_nemotron([b64], settings=settings)
