# higgsfield-usage

_This skill was installed by the higgsfield app and is read-only._

# Higgsfield

This agent reaches Higgsfield in one of two ways. Check which applies before generating:
- **Higgsfield MCP tools are available** (signed in, uses the user's plan credits): use them. List the tools first, the model catalog evolves and the tool schemas tell you which model ids and aspect ratios are accepted. Let Higgsfield pick the model by default; only pin one (Soul, Seedream, Kling, Veo, Sora, Cinema Studio...) when the user asks for a named look or a capability the default cannot cover.
- **`HF_KEY` is in the environment** (API key in the `KEY_ID:KEY_SECRET` form, billed to the API dollar balance, separate from the higgsfield.ai plan): use the REST API below. An older install may carry `HF_API_KEY_ID` and `HF_API_KEY_SECRET` instead: join them as `${HF_API_KEY_ID}:${HF_API_KEY_SECRET}`.

## REST API (API key)

Base URL `https://api.higgsfield.ai`, header `Authorization: Key ${HF_KEY}`.

1. Pick a model from https://docs.higgsfield.ai/docs/models/image-generation.md or https://docs.higgsfield.ai/docs/models/video-generation.md. Each model page (`https://docs.higgsfield.ai/docs/models/<model>/<workflow>.md`) gives the Endpoint ID and the exact request schema. Never guess fields.
2. Submit:
```
curl -sS -X POST "https://api.higgsfield.ai/<endpoint-id>" \
  -H "Authorization: Key ${HF_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"..."}'
```
It returns `request_id`, `status_url` and `cancel_url`. Use those URLs, do not build them by hand.
3. Poll `status_url` with the same header (start at 2 s, back off to 10 s) until the status is `completed`, `failed`, `nsfw` or `canceled`. A completed request carries `images[].url`, `video.url` or `audio.url`; outputs stay available for at least 7 days, download them if they must last longer.
4. Local input file: `POST https://api.higgsfield.ai/files/generate-upload-url` with `{"content_type":"image/png"}`, PUT the file to `upload_url` with every header in `upload_headers` (never send the Higgsfield credentials there), then pass `public_url` as `image_url` / `video_url` / `audio_url`.
5. Never repeat a generation POST after an ambiguous timeout: submissions have no idempotency key and it would bill twice. Cancel with `POST cancel_url` while the request is still queued.

Errors: 401 bad credentials, 403 insufficient API balance (tell the user to top up in open.higgsfield.ai), 422 body does not match the schema (re-read the model page), 423 / 503 model temporarily unavailable. Failed and nsfw requests are not charged.

## Generating well

- Write prompts as a shot description: subject, action, setting, lighting, lens and mood. Vague prompts produce generic results.
- Video generation is asynchronous and slow. Start the job, then poll for its status instead of assuming the first response contains the final asset.
- Return the resulting asset URL to the user, and reuse the same character or seed across calls when a series must stay visually consistent.