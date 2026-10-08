# Donor matrix — V2 executable ledger

Schema: `ID | Kind | Screen | Component | Donor | URL | License | Treatment | Exact pattern | Files | Deps | Acceptance | Status`

Treatments: `COPY_ADAPT` · `REWRITE` · `REFERENCE` · `DEPENDENCY` · `ASSET` · `DATA` · `METHOD` · `CUSTOM`

Synced from fuse-catalog 2026-10-09. Visual language always `--dp-*`. Zero AGPL paste.

| ID | Kind | Screen | Component | Donor | URL | License | Treatment | Exact pattern | Files | Deps | Acceptance | Status |
|----|------|--------|-----------|-------|-----|---------|-----------|---------------|-------|------|-------------|--------|
| F10-01 | METHOD | Wireframe | docs | NN/g 5s | nngroup.com/articles/testing-visual-design | cite | METHOD | 5s + first-click gate | docs/build/WIREFRAMES_V2.md | none | A-F10 | DONE |
| F6-05 | ASSET | Demo map | MapHUD | OpenFreeMap Positron | tiles.openfreemap.org/styles/positron | OpenFreeMap/ODbL | ASSET | muted basemap style URL | MapHUD.tsx | none (URL) | A-F6-05 | DONE |
| F6-06 | ASSET | Demo map | MapHUD | Carto Positron GL | basemaps.cartocdn.com/gl/positron-gl-style/style.json | Carto terms | ASSET | fallback style | MapHUD.tsx | none | A-F6-05 | DONE |
| F6-02 | DEPENDENCY | Demo map | MapHUD | MapLibre slow flyTo | maplibre.org docs | BSD-3 | DEPENDENCY | speed/curve/essential | MapHUD.tsx, IncidentReplay.tsx | maplibre-gl (existing) | A-F6-02 | DONE |
| F13-01 | DATA | Demo | demoMode | Purana Quila Wikipedia | en.wikipedia.org/wiki/Purana_Qila,_Delhi | CC BY-SA | DATA | 28.60944, 77.24417 | demoMode.ts | none | A-F13 | DONE |
| F1-01 | REFERENCE | Command | QueueTable | AEGIS TriageQueue | github.com/alejadxr/AEGIS | AGPL-3.0 | REFERENCE | AWAITING YOU chip/region — rewrite only | QueueTable, TriageChip, TopBar | none | A-F1 | DONE |
| F1-02 | COPY_ADAPT | Command | QueueTable | IncidentPulse | github.com/bhoyee/IncidentPulse | MIT | COPY_ADAPT | ops list → detail grammar | QueueTable, App | none (pattern) | A-F1 | DONE |
| F3-02 | COPY_ADAPT | Evidence | EvidenceLedger | SourceDeck | github.com/Xyloth/SourceDeck | MIT | COPY_ADAPT | quote+source+missing | EvidenceLedger, EvidenceList | none | A-F3 | DONE |
| F4-01 | COPY_ADAPT | Decision | ActionBlock | decision-desk | github.com/rspier-ax/decision-desk | MIT | COPY_ADAPT | required reason + append-only audit | ActionBlock, DecisionAuditPanel, hitl | none | A-F4 | DONE |
| F9-01 | REWRITE | Decision | ActionBlock | permit-react-demo | permitio demo | check | REWRITE | IC-only confirm gate | ActionBlock, TopBar | none | A-F9 | DONE |
| F5-01 | CUSTOM | Coordination | CoordinationBrief | ship expand | ship | ship | CUSTOM | copy brief + escalate reasons | CoordinationBrief.tsx | none | A-F5 | DONE |
| F7-01 | CUSTOM | Rain | RainControl | ship | ship | ship | CUSTOM | RAINFALL SCENARIO · mm; never agency | RainControl, useRain | none | A-F7 | DONE |
| F8-01 | REFERENCE | Lifecycle | StateChip | Carbon Progress | carbondesignsystem.com | Apache-2.0 | REFERENCE | density/step chrome | StateChip.tsx | none | A-F8 | DONE |
| F2-02 | CUSTOM | Incident | OwnershipConflict | ship | ship | ship | CUSTOM | NO AUTO-ASSIGN / RESPONSIBILITY DISPUTED | OwnershipConflict.tsx | none | — | DONE |
| F11-02 | ASSET | Tokens | tokens | IBM Plex @fontsource | npm | OFL 1.1 | ASSET | self-host Plex; no CDN | tokens.css, package.json | @fontsource/* (existing) | — | DONE |
| F14-01 | ASSET | Pitch | docs | AWS Architecture Icons | aws.amazon.com/architecture/icons | AWS icon terms | ASSET | pitch only — never TopBar | docs, aws-arch.html | none | — | DONE |
| F16-01 | CUSTOM | Map | MapHUD | ship | ship | ship | CUSTOM | upgrade camera/style only | MapHUD.tsx | existing | A-F6-05 | DONE |
| REJECT-AEGIS | REFERENCE | — | — | AEGIS | alejadxr/AEGIS | AGPL-3.0 | REFERENCE | never vendor | — | none | — | LOCKED |
| REJECT-RAINVIEWER-HERO | REFERENCE | Demo | — | RainViewer | rainviewer API | API terms | REFERENCE | subtle only; not Demo hero | — | none | — | LOCKED |

## Prior (pre-V2) reference rows

| COMPONENT | SOURCE | LICENSE | Treatment |
|-----------|--------|---------|-----------|
| TopBar / Queue / Map patterns | WorldIntel, Civic-Resolve, Crisis Logistics | None | REFERENCE only |
| Earth Studio | Google | Google terms | Video tool only |
