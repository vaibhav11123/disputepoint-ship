# Earth Studio shot — Mode C (Tier S cinematic)

**Not an app dependency.** Pre-render in [Google Earth Studio](https://www.google.com/earth/studio/), edit into the YouTube open.

## Camera path (3–5s)

```text
EARTH → INDIA → DELHI → CENTRAL DELHI → PURANA QUILA → HARD CUT → DisputePoint queue
```

| Time | Action |
|------|--------|
| 0:00–0:02 | World / India / Delhi aerial |
| 0:02–0:04 | Descend; camera-target on Purana Quila corridor |
| 0:04–0:05 | Hold incident point |
| 0:05 | Hard cut to live app (`make run` UI) |

## Rules

- VO after cut = DM cell / HC buck-passing / honest null ([DEMO_SCRIPT.md](DEMO_SCRIPT.md)).
- Do **not** narrate “Monsoon hits Delhi…” over Earth.
- Do not export Earth buildings into `frontend/`.
- Store MP4/WebM under local demo assets (gitignored) or editor project — not runtime.

## Checklist

- [ ] Keyframes + camera target locked on Purana Quila
- [ ] Export ≤5s
- [ ] Hard cut into calm queue
- [ ] LICENSE_AUDIT row: video tool only
