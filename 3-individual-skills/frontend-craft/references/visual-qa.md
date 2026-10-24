# Visual QA matrix

Choose the rows that matter to the requested surface. Record actual viewport/device, action and observation. A screenshot documents appearance at one moment; it cannot by itself prove a click, motion continuity or accessibility.

| Concern | Inspect or exercise |
| --- | --- |
| Product identity | Does the first screen/viewport show the product's real job, content and distinct visual idea? Could the same layout be relabelled for an unrelated product? |
| Hierarchy and composition | Identify first, second and third visual priorities. Check alignment, reading order, line lengths, density, whitespace and whether each container carries meaning. |
| Truthful content | Use real or labelled sample data. Verify every statistic, status, privacy claim, download and CTA against what exists. |
| Responsive layout | Render narrow phone, ordinary phone, tablet/desktop and any user-specified breakpoint. Check clipping, horizontal overflow, artwork/copy separation, safe areas, long labels and large text. |
| Actions and states | Activate each primary control, then loading, empty, denied, offline, failure, cancelled and completed states. Check that button wording matches the result. |
| Input and accessibility | Tab/keyboard order, visible focus, control names, touch targets, contrast, screen-reader semantics, reduced motion and alternate access to drag/hover-only actions. |
| Motion and 3D | Verify interaction feedback, repeated switching, reverse scroll, pause/resume, renderer/context lifecycle, cleanup and simple/failure view. Observe actual frames when claiming smoothness. |
| Native integration | Check platform-owned permission/keyguard/share interfaces, notification takeover, physical insets and navigation. Browser preview does not close these gates. |
| Regression | Preserve accepted desktop/mobile surfaces and user choices. Compare changed views with the last accepted baseline, then test the new behavior. |

End with a short critique: the strongest choice, the largest mismatch fixed, and anything that still needs a real device, browser engine or user judgment.
