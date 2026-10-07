# kie-ai-usage

_This skill was installed by the kie-ai app and is read-only._

# Kie.ai

Kie.ai exposes one tool per media model: images (nano_banana_image, gpt_image_2, flux2_image, bytedance_seedream_image, midjourney_generate, qwen_image, z_image), video (veo3_generate_video, kling_video, bytedance_seedance_video, runway_aleph_video, wan_video, hailuo_video), audio (suno_generate_music, elevenlabs_tts, elevenlabs_ttsfx) and editing (topaz_upscale_image, recraft_remove_background, ideogram_reframe).

## Workflow
1. Not sure which model fits? Call list_models to search by capability.
2. Input images or audio must be public URLs. For a local file, call upload_file (base64) first and pass the returned URL.
3. Generation is asynchronous: the tool returns a task_id. Call wait_for_task (or poll get_task_status) until it succeeds, then read the output URLs.
4. Output URLs expire: download the files you want to keep into the workspace.

## Cost
Every generation spends the user's Kie.ai credits, and video is the most expensive. Generate one variant first, and only batch or retry when the user asked for it.