# 4-Task Shipping Day — Morning Kickoff Template

Use this cron prompt structure when scheduling a shipping-day morning. The pattern is: forum → outreach → emails → engineering. Each task is independently finishable in 5-15 minutes. No single task blocks the next.

## Cron Prompt Template

```
Morning kickoff — 9:30 AM. Tasks:

1. ✉️ Post on REAPER forum + r/Reaper + KVR about your REAPER scripting services.
   Credential: Suno Workflow Suite (7 scripts, ReaPack)
   3 sentences: what you built, what you can do (custom actions, templates, routing), rate ($50/hr or flat $200-$500)
   No AI buzzwords. Post links:
   - forum.cockos.com/forumdisplay.php?f=20 (REAPER Scripting)
   - reddit.com/r/Reaper
   - kvraudio.com/forum/viewforum.php?f=276 (if account exists)

2. 🔍 Run studio scraper for Vancouver/Burnaby/Richmond.
   Change TARGET_CITIES to these 3 only. headless=True. Outputs CSV.

3. 📧 Generate emails from scraper CSV.
   Variant A: expertise-request style. Asks for their bottleneck, disarms the pitch.

4. 🚢 Ship [current project ONNX/model export].
   Train script: train_clara_now.py (or equivalent)
   Export: export_mamba_onnx.py --checkpoint checkpoints_clara/best.pt --output models/mamba_rt.onnx
   Verify: verify_onnx_model() or onnxruntime.InferenceSession
   Build: cmake --build build --config Release

This is the day you ship. Go.
```

## Notes

- **Do NOT ask the user to choose** — this cron runs autonomously, user isn't present.
- **Status check first**: check what actually shipped from the last iteration. Don't repeat done work.
- **Forum drafts should be ready to copy-paste** — no "write your own" hand-waving.
- **Run-time estimate on each task** helps the user budget time (e.g., "5 min", "background, 2 min setup").
- **If a task is already done** (e.g., ONNX already exported), confirm it and mark it ✓, don't redo.