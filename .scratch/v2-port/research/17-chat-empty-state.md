# Ticket 17 — chat introduction and speaker distinction

Research date: 2026-10-16. Primary sources only. Scope: the author's requested chat styling and placement of the scope note and starter questions. The approved left history column and right chat column stay in place.

## Source guidance

- Carbon says empty states belong in the space where the missing content would appear. It recommends concise contextual guidance and allows a centered block of left-aligned content in larger spaces. [Carbon: Empty states](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states)
- Carbon AI Chat provides a pre-conversation home screen for an assistant introduction and conversation-starter buttons. It transitions to the conversation when the first message is sent. Returning to that introduction is configurable. [Carbon AI Chat: Home screen](https://chat.carbondesignsystem.com/tag/latest/docs/documents/UI_customization.Home_screen.html)
- WCAG requires a visible cue beyond color when color conveys meaning, and at least 4.5:1 text contrast for normal text. [WCAG 2.2: Use of Color](https://www.w3.org/TR/WCAG22/#use-of-color), [Contrast Minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum)

## Project application

Put a short heading, the existing read-only role description and the three existing starter buttons inside the empty message viewport. Group them as one left-aligned block. Let starter text wrap on narrow screens. Keep the composer and AI caution directly below the scrolling viewport so the input remains discoverable. These exact layout choices are our application of the guidance, rather than a universal design-system requirement.

Hide the introduction and starters after the first send, as the existing spec requires. Preserve starter behavior: selecting one fills the input for review before Send. Carbon's direct-send behavior is not required here.

Give user messages a dedicated soft rose surface. The existing primary token is neutral, so tinting it cannot create the requested pink. Use a separate message-role tint rather than an error colour variant. Keep assistant messages neutral. Retain right alignment for the user and left alignment for the assistant as a visible cue beyond color. Keep accessible speaker names and check text contrast in both themes.

No change to report behavior, tool evidence, API behavior or the answer renderer is needed.


## Applied choice and verification

The scope note and starter cards share one welcome region inside the message viewport. The viewport
keeps its height before and after the first question. Initial empty-state scrolling starts at the
top; conversation scrolling follows the existing end behaviour. A starter fills the input without
sending. The input and AI caution remain below the viewport.

User messages use rose-100 with rose-950 text in light mode. Dark mode uses rose-300 at 20% opacity
with rose-50 text. Both speakers have visible labels in addition to left/right alignment. A
calculation from the installed Tailwind OKLCH palette and default page/card colours gives text
contrast of approximately 13.02:1 in light mode and 11.97:1 in dark mode, after alpha compositing.
These are palette calculations rather than measurements from browser screenshots. Final visual
appearance remains the author's check.
