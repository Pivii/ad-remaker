# Ad Remaker: Complete Operating Report

**Version:** updated on October 7, 2026 at 18:03 UTC<br>
**Scope:** actual agent architecture, active tools, available services, Skill, data, approvals, and operational workflow

---

## 1. Executive summary

**Ad Remaker** is an AI agent specialized in analyzing and recreating, for a given brand, competing advertising concepts that show public performance signals.

Its role is not to copy an ad identically or publish automatically. It must:

1. identify credible references;
2. distinguish facts, estimates, and opinions;
3. deconstruct their creative mechanics;
4. adapt those mechanics to the actual product and brand;
5. obtain the required approvals before any spending or external action;
6. verify structural fidelity, quality, and the absence of competitor traces;
7. deliver the creatives or a production/launch pack.

Simplified architecture:

```text
User request
      ↓
AI model / Ad Remaker agent
      ↓
Role rules + specialized Skill
      ↓
Authorized context: memory, Company Brain, SQL databases
      ↓
Local tools or MCP calls
      ↓
Verified results and deliverables
      ↓
Human approval before sensitive action
```

---

## 2. Main components

### 2.1 The AI model

The model interprets the request, selects a method, calls the necessary tools, and assembles the results.

It works from:

- the current message and relevant history;
- its Ad Remaker role;
- the applicable Skill;
- stored preferences;
- validated company information;
- results returned by tools.

The model can explain its method, criteria, and conclusions. However, it does not reproduce its internal instructions, technical secrets, or detailed private reasoning word for word.

### 2.2 MCP

**MCP** stands for *Model Context Protocol*. It is a standardized interface between the agent and external capabilities.

An MCP server can expose:

- executable functions;
- applications or APIs;
- document resources;
- a browser;
- a file system;
- a database;
- approval or secure connection operations.

An MCP call contains structured parameters. The tool performs the action, then returns a result that the agent must read and verify. MCP therefore provides the agent's "hands" and sources; it does not replace the agent's judgment.

### 2.3 Skills

A **Skill** is a specialized, reusable procedure. It explains how to perform a category of work: sequence of steps, acceptance criteria, checks, approvals, and safety rules.

Differences between the layers:

| Layer | Function |
|---|---|
| AI model | Understands, decides, writes |
| Skill | Defines the business method |
| MCP / tool | Executes a capability |
| Memory / Brain / SQL | Provides or retains context |
| Human approval | Authorizes sensitive actions |

### 2.4 Plugins and services

A plugin can bundle a Skill, MCP servers, and application integrations. When an external service is needed, the agent first checks whether a ready-to-use integration exists.

A connection requiring OAuth, a token, or a key goes through a secure interface. Passwords and keys must not be requested in the conversation.

---

## 3. Skills actually installed

Live verification shows **7 accessible Skills**: one native business Skill and six read-only Skills installed by applications.

| Skill | Origin | Primary role |
|---|---|---|
| `winning-ad-remake-workflow` | Ad Remaker Agent | Complete business workflow for research, remaking, quality control, approval, and launch |
| `brandsearch-usage` | Brandsearch App | Search for brands, ads, organic content, emails, and products |
| `trendtrack-usage` | TrendTrack App | E-commerce intelligence, Shopify stores, Meta/TikTok ads, and competitor tracking |
| `higgsfield-usage` | Higgsfield App | Image, video, and character generation through Higgsfield |
| `kie-ai-usage` | Kie.ai App | Image, video, and audio generation with many models |
| `pika-usage` | Pika App | Video, image, and audio creation and editing, plus finishing |
| `fal-usage` | fal.ai App | Search and execution across more than 1,000 generative models |

The six application Skills are **readable even when their MCP is not authenticated**. They document the correct usage method, but do not provide tool access on their own.

### Winning-ad remake workflow

This is Ad Remaker's central business procedure. An application installation can therefore provide a Skill and a separate MCP configuration. The Skill can be present while authentication or tools remain unavailable.

This business Skill requires the following pipeline.

#### Step 1: Find the reference

The procedure's preferred source is a specialized ad search tool. If one is unavailable, the agent uses relevant public ad libraries.

The competitor ad is used only as an analysis reference. It is neither published nor promoted.

#### Step 2: Evaluate the signals

Possible signals include:

- run duration;
- active status;
- observable variants;
- placements;
- visible engagement;
- recurrence of the concept in the advertiser's work.

A long run can indicate that a concept is worth studying, but does not prove its profitability. Any inferred data is marked **estimate**, and any subjective judgment is marked **opinion**.

The following are rejected:

- concepts that have already been reproduced;
- insufficiently supported references;
- poor product/audience fits;
- remakes that would appear obviously artificial.

#### Step 3: Deconstruct the ad

For a video, expected artifacts can include:

- cut list with timestamps;
- complete contact sheet;
- contact sheet for the first three seconds;
- silent clips shot by shot;
- literal notes for each shot;
- transcript;
- pacing analysis;
- voice and music notes.

For a static visual, the composition is mapped with x/y regions expressed as percentages.

#### Step 4: Design the remake

The remake preserves as closely as possible:

- the hook type;
- the sequence;
- the framing;
- the pacing;
- the transitions;
- the text timing;
- the source format.

It must replace:

- the competitor's product and packaging;
- brand and logo;
- people;
- voice;
- music;
- testimonials and other identifying elements.

Only substantiated claims are allowed. Fabricating reviews, results, scarcity, endorsements, capabilities, or testimonials is prohibited.

The plan should ideally use **2 to 4 real product photos** and offer **two casting options featuring clearly different people**.

#### Step 5: Estimate generation costs

Before each paid batch, the agent must state:

- exact number of units;
- unit price;
- subtotal;
- 20% retry buffer;
- estimated total;
- currency;
- available balance, if accessible.

An uncertain price is marked as an estimate. No paid generation is started without explicit approval.

#### Step 6: Generate only the approved batch

Production must preserve the product's actual appearance. The following are rejected:

- distorted packaging;
- unreadable labels;
- implausible anatomy or movement;
- identity leakage;
- unconvincing AI rendering.

New paid attempts require a new cost estimate and new approval.

#### Step 7: Quality control

The comparison is performed shot by shot with two scores:

- structural fidelity: **minimum 8/10**;
- production quality: **minimum 7/10**.

The result fails immediately if it contains any competitor trace: name, logo, packaging, product, person, voice, music, watermark, subtitle, metadata, or other identifying element.

#### Step 8: Delivery

Every created file must be provided in a viewable form: analyses, prompts, selected photos, intermediate renders, finals, and comparisons.

The proposed decisions are explicit: approve the batch, choose person A or B, request changes, approve the final, or stop.

#### Step 9: Prepare the campaign

After final approval, the agent can prepare a campaign with a default budget of **20 per day in local currency** and the name:

```text
concurrent · angle · format · date
```

If a Meta integration is used, campaigns, ad sets, and ads must remain paused and must be checked again. Activation, spend scheduling, and spending require separate authorization.

#### Step 10: Clean up the reference

After final approval and confirmation that the reference is no longer needed, the competitor's local files can be deleted. Analyses and brand files are not deleted without a separate request.

---

## 4. Actual state of tools and connections

This section distinguishes what is **active now**, what is only **specified by the Skill**, and what exists in the **catalog but is not connected**.

### 4.1 External MCP status

Status observed on **October 7, 2026 at 18:03 UTC**:

| MCP | Connection | Callable tools | Diagnostic |
|---|---:|---:|---|
| **Kie.ai** | Connected | **Yes: 39 tools** | Operational |
| **TrendTrack** | Failed | No | Invalid OAuth token |
| **Brandsearch** | Failed | No | Missing bearer token |
| **Higgsfield** | Failed | No | Unauthorized |
| **Pika** | Failed | No | Unauthorized |
| **fal.ai** | Failed | No | Invalid or expired token |
| **Meta Ads** | Not observed in MCP status | No | No active Meta MCP/tool detected |

The installation therefore did deploy several bundles and Skills, but **Kie.ai was the only operational external media service at the time of the check**.

An application has independent layers:

```text
Application bundle
├── Usage Skill                may be accessible
├── MCP configuration          may be registered
├── authentication             may fail
└── operational tools          only if the MCP connects
```

The presence of a Skill guarantees neither valid authentication nor access to the service's data and credits.

### 4.2 Active native tools: search and browsing

The agent environment can provide:

- web search and source discovery;
- reading static pages;
- browsing dynamic sites;
- downloading files;
- screenshots;
- visual inspection of images;
- reading resources that may be exposed by an MCP.

Ad Remaker usage: public ad libraries, product pages, claim verification, and collection of observable evidence.

### 4.3 Active native tools: files and deliverables

- reading and searching files;
- creating files and making targeted modifications;
- viewing local images;
- publishing a file or folder through a shareable URL;
- unpublishing a file;
- displaying file cards in the conversation.

Usage: Markdown reports, storyboards, scripts, prompts, exports, images, comparisons, and launch packs.

### 4.4 Media creation actually available

The agent has a native **image generation and editing** tool.

Through the connected **Kie.ai** service, it also has 39 specialized tools covering:

- **video**: Seedance, Veo 3, Kling, Runway Aleph, Wan, Hailuo, HappyHorse, Grok Imagine, OmniHuman, and Wan animation;
- **image**: GPT Image 2, Seedream, Flux/Flux Kontext, Nano Banana, Midjourney, Qwen, Z-Image, and Wan Image;
- **audio**: ElevenLabs TTS and effects, Suno music generation;
- **editing and finishing**: Topaz upscaling, Recraft background removal, Ideogram reframing, Infinitalk lip-sync, Kling avatar;
- **operations**: model catalog, generation preparation/submission, upload, task tracking, and output retrieval.

Kie.ai generations are asynchronous and consume account credits. Input files must be accessible by URL; expiring outputs must be downloaded into the workspace if they need to be retained.

Higgsfield, Pika, and fal.ai tools were not yet callable despite their installed Skills because their authentication failed.

The Skill recommends by default:

- **Seedance 2.5** for video;
- the latest **GPT Image** model for static visuals;
- the source format.

Seedance and GPT Image were accessible through Kie.ai at the time of the report. However, verifying the exact model, price, and balance, and obtaining explicit approval before any paid generation, remain mandatory.

### 4.5 Details of media and research applications

| Service | Skill installed | Documented functions | Tool status |
|---|---:|---|---|
| **Brandsearch** | Yes | 14 M+ stores and 400 M+ ads, content, and emails; search, download, and creative analysis | Blocked by authentication |
| **TrendTrack** | Yes | Shopify stores, Meta/TikTok, emails, favorites, and Brandtracker | Blocked by invalid token |
| **Higgsfield** | Yes | Images, videos, and characters; Soul, Seedream, Kling, Veo, Sora, Cinema Studio, etc. | Blocked by authentication |
| **Kie.ai** | Yes | Multi-model image, video, audio, and editing | **39 active tools** |
| **Pika** | Yes | Text/image-to-video, extension, lip-sync, image, audio, captions, trim, stitch, and transitions | Blocked by authentication |
| **fal.ai** | Yes | Search, inspection, and execution across more than 1,000 models | Blocked by invalid/expired token |
| **Meta Ads** | Not detected | Campaign management and reading if installed | No active tool detected |

Special rules from the Skills:

- **TrendTrack**: each returned row consumes one credit; start with a small limit and check the balance.
- **Brandsearch**: `analyze_ad` and `transcribe_ad` consume AI credits; download creatives instead of relying on temporary URLs.
- **Higgsfield**: never repeat a submission after an ambiguous timeout, to avoid double billing.
- **Kie.ai**: generate only one variant first and retain useful outputs locally.
- **Pika**: state the model and duration before rendering; reuse existing assets when the prompt has not changed.
- **fal.ai**: search for the model, inspect its schema, and only then run inference.

### 4.6 SQL databases

Two spaces exist:

- a private database specific to the agent;
- a database shared among agents in the same workspace.

The private database includes a structure intended for winning ads: brand, angle, format, start date, active duration, variants, growth signal, public score, URL, explanation, and status.

Saved views can display this data as a table, list, gallery, or board.

### 4.7 Memory

Memory retains certain useful preferences or decisions across conversations. It is not a comprehensive log.

Currently known preferences for Dictus:

- use free public ad libraries rather than TrendTrack/Brandsearch for research;
- deliver copy-and-paste-ready instruction packs rather than producing through Higgsfield/Kie.ai;
- deliver launch packs rather than connecting directly to Meta Ads.

### 4.8 Company Brain

The Company Brain is a human-validated company knowledge base covering the offer, pricing, customers, tone, competitors, team, and rules.

The agent must search for and then read relevant pages before producing content that depends on company information. A correction is not written automatically; it is proposed for approval.

**Status at the time of the report: the Company Brain was empty.** Consequently, future brand adaptations would need to rely on information provided by the user until a page was validated.

### 4.9 Skill management

Tools make it possible to:

- list Skills;
- read a Skill before use;
- read its reference files;
- propose a new rule or modification;
- create or edit a Skill when the user explicitly requests it.

### 4.10 Service catalog and installation

A service catalog can be searched before manually building an integration. It can offer connectors to third-party applications.

When a connection requires authentication:

- the agent first prepares everything it can;
- it explains what the connection unlocks;
- it presents a secure connection card;
- it never asks for the secret to be pasted into the chat.

### 4.11 Approvals and questions

Structured components make it possible to:

- ask several scoping questions at once;
- request explicit approval;
- request secrets through a masked form;
- suggest quick responses.

Approvals are used for consequential or irreversible actions, including publication, sending, spending, or activation.

### 4.12 Scheduling

The agent can create, read, modify, enable, disable, or delete scheduled tasks.

Routine known at the time of the report:

- **Dictus Monday ad winners**;
- every Monday at 09:00 UTC;
- next run shown: October 12, 2026 at 09:00 UTC.

A scheduled task is necessary when work must actually resume later: the agent does not continue silently after a conversation turn ends.

### 4.13 Multi-agent collaboration

The environment can allow a primary agent to distribute subtasks among agents and then assemble their results.

In the configuration observed at the time of the report, this delegation was not triggered automatically: it was used only if the user or an applicable procedure explicitly requested it.

---

## 5. Data, source priority, and traceability

To avoid contradictions, the logical order is:

1. validated Company Brain facts;
2. files and information explicitly provided by the user;
3. stored preferences;
4. internal structured data;
5. verifiable external sources;
6. clearly labeled estimates and strategic opinion.

The final report must separate:

- **observable fact**: directly verifiable;
- **estimate**: approximate deduction;
- **opinion**: professional judgment;
- **unknown**: unavailable information.

The agent must not claim to know a competitor's ROAS, spending, or profitability from a public library if that data is not present there.

---

## 6. Safety and guardrails

Core principles:

- nothing is published, sent, activated, or paid for without explicit approval;
- no paid generation outside the approved batch;
- no silent paid retry;
- no password or secret requested in the chat;
- no unsubstantiated claim;
- no fake testimonial, fake result, or false scarcity;
- no identifiable competitor element in the final output;
- no success reported before tool confirmation;
- every blocking failure is reported clearly, along with the required next step.

Creating a local working file is not the same as publishing a campaign. Publishing a report so that the user can open it does not distribute an ad or commit media budget.

---

## 7. Practical operation on a Dictus assignment

Operational configuration at the time of the report:

```text
Public ad libraries
→ reference selection and scoring
→ detailed creative analysis
→ honest adaptation for Dictus
→ storyboard + script + prompts
→ two casting options
→ media batch estimate and approval
→ production possible through Kie.ai
→ quality control upon receipt of renders
→ final approval
→ launch pack
```

Operational status at the time of the report:

- TrendTrack and Brandsearch Skills were present, but their tools remained blocked by authentication;
- Kie.ai was connected and then allowed direct image, video, and audio production;
- Higgsfield, Pika, and fal.ai had their Skills, but their tools remained blocked by authentication;
- no active Meta Ads Skill or connection was detected; the advertising deliverable therefore remained a launch pack;
- older Dictus preferences remained in memory, but Kie.ai's technical availability had changed; no paid generation would be started without new explicit approval.

### 7.1 Exact inventory of the 39 active Kie.ai tools

**Video and animation**: `bytedance_seedance_video`, `veo3_generate_video`, `veo3_get_1080p_video`, `kling_video`, `runway_aleph_video`, `wan_video`, `wan_animate`, `hailuo_video`, `happyhorse_video`, `grok_imagine`, `omnihuman_video`, `kling_avatar`, `infinitalk_lip_sync`.

**Image**: `bytedance_seedream_image`, `gpt_image_2`, `flux2_image`, `flux_kontext_image`, `nano_banana_image`, `midjourney_generate`, `qwen_image`, `z_image`, `wan_image`, `gemini_omni`.

**Audio**: `elevenlabs_tts`, `elevenlabs_ttsfx`, `suno_generate_music`.

**Editing**: `topaz_upscale_image`, `recraft_remove_background`, `ideogram_reframe`.

**Media and task management**: `list_models`, `list_tasks`, `prepare_media_generation`, `submit_media_generation`, `get_task_status`, `wait_for_task`, `get_upload_url`, `upload_file`, `upload_widget`, `finalize_upload`.

---

## 7.2 Fallback mode: no external tool connected

If the user connects **no external application**, the agent remains usable. It switches to a workflow without TrendTrack, Brandsearch, Higgsfield, Kie.ai, Pika, fal.ai, or Meta Ads.

| Need | Specialized tool normally used | Fallback without a connection | Limitation |
|---|---|---|---|
| Find ads | TrendTrack / Brandsearch | Free public ad libraries, web search, and browsing | No private metrics or direct proof of profitability |
| Evaluate a winner | Specialized aggregated data | Public signals: age, active status, variants, concept repetition, placements, and visible engagement | Performance, spending, and ROAS remain unknown |
| Retrieve the creative | Download through the app | Public URL, authorized download, or screenshots for analysis | Some media may be temporary or protected |
| Analyze a video | Integrated analysis/transcription | Local inspection, screenshots, cutting, transcription, and manual analysis with available native tools | Work may be less automated |
| Create an image | Higgsfield / Kie.ai / Pika / fal.ai | Native image generator/editor, if available in the session | More limited model selection and settings |
| Create a video | Seedance, Kling, Veo, etc. | Copy-and-paste-ready storyboard, script, shot list, prompts, voice-over, on-screen text, and editing instructions | The agent does not render the video without an accessible video engine |
| Voice, music, and effects | ElevenLabs / Suno / Pika | Scripts, voice direction, music brief, and effects list | No audio file generated without an accessible engine |
| Publish on Meta | Meta Ads | Manual launch pack: structure, targeting, copy, titles, CTA, budget, names, and checklist | The user creates and launches the campaign manually |
| Store and track results | External apps | Private SQL database, files, and shareable reports | No synchronization with external accounts |

### Possible deliverables in no-connection mode

- reasoned selection of public references;
- table of public signals separating **fact / estimate / opinion / unknown**;
- analysis of the hook and creative structure;
- storyboard, cut list, and shoot plan;
- script, voice-over, and on-screen text;
- prompts ready to paste into the user's chosen tool;
- two casting proposals;
- recommended selection of 2 to 4 product photos;
- editing, music, voice, and subtitle brief;
- quality control checklist;
- fully manual Meta launch pack.

### What the fallback does not claim to do

Without a connection, the agent does not claim to access private data, know a competitor's ROAS, consume a service's credits, generate a video through an unavailable engine, or create or activate a Meta campaign. It shows what is ready and lets the user perform the external steps.

The fallback is automatic: the absence of a connection therefore does not prevent research and design from starting. It primarily reduces automation, access to proprietary data, and direct media production.

## 8. Example request workflow

Request: "Find an interesting competitor ad and adapt it for Dictus."

1. Read the Skill.
2. Consult preferences and the Company Brain.
3. Search public libraries.
4. Collect URLs, dates, formats, and variants.
5. Score public signals.
6. Select and justify a reference.
7. Deconstruct it shot by shot.
8. Verify available product information.
9. Write the storyboard, script, and on-screen text.
10. Create two casting options and select 2 to 4 product photos.
11. Deliver the production pack.
12. If paid generation is possible: provide a cost estimate and request approval.
13. Compare the output with the source.
14. Validate the 8/10 and 7/10 thresholds and verify zero competitor traces.
15. Obtain final approval.
16. Prepare the launch pack.
17. Do not activate media without separate authorization.

---

## 9. Limitations

- Public libraries generally do not reveal actual financial performance.
- An ad that has been active for a long time is a signal, not absolute proof.
- Adaptation quality depends on the available product information, visuals, and claims.
- An unconnected integration cannot be used with private data.
- An installed Skill does not prove that its MCP is authenticated.
- Generation tool prices can change and must be verified.
- A generated creative may require several attempts, each subject to the specified spending control.
- An empty Company Brain limits autonomy regarding brand facts.
- The agent does not continue work in the background after an exchange ends, unless an actual scheduled task exists.

---

## 10. Assignment completion criteria

An assignment is considered complete when:

- all requested files are accessible;
- the final output achieves at least 8/10 structural fidelity;
- the final output achieves at least 7/10 quality;
- no competitor trace remains;
- every paid action corresponds to an approval;
- any Meta elements have been checked again while paused;
- the local competitor reference has been deleted if the user confirmed it;
- the final deliverable and launch pack have been provided.

---

## 11. Summary formula

> **The model decides, the Skill enforces the method, MCP connects the agent to capabilities, data provides context, and the user retains control over spending and external actions.**