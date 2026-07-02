# Responsive State Review

Use this scenario to test whether `$ui-change-review` checks user-facing states
instead of only reviewing implementation style.

## Prompt

```text
Use $ui-change-review to review this interaction change across states, accessibility, responsive layout, and tests.
```

## Simulated Change

A pull request adds a mobile filter drawer to a results page. The desktop layout
works, but the mobile drawer:

- opens without moving focus into the drawer
- leaves the background scrollable
- hides the apply button below the viewport on small screens
- has no test for closing with Escape

## Expected Review

The skill should report user-visible risks:

- Focus management is incomplete for keyboard and screen reader users.
- Background scroll can create confusing page position after closing the drawer.
- The apply action must stay reachable at narrow widths.
- Interaction tests should cover open, apply, Escape close, and focus return.
