# Frontend Review Reference

Use this for Vue, React, Flutter, TypeScript, Dart, API client, routing, state, forms, and UI changes.

## Shared Frontend Checks

- Contract compatibility: request/response fields, enum values, pagination, empty states, error codes, and timestamp formats match backend behavior.
- Permission UX is not security: hidden buttons are fine, but backend must still authorize sensitive actions.
- Loading, empty, error, retry, offline/timeout, and permission-denied states exist for important flows.
- Avoid duplicate submission: disable submit, debounce search, add idempotency token when backend needs it.
- Do not expose secrets, internal endpoints, private bucket paths, debug switches, or excessive user PII in browser/app logs.
- Internationalization/local copy: Chinese text should match product tone; avoid hardcoded magic strings when the app already has i18n.
- Accessibility and mobile ergonomics: keyboard focus, touch targets, safe areas, viewport scrolling, and screen reader labels where relevant.

## Vue 3

- Prefer Composition API with typed `defineProps`/`defineEmits`; use `withDefaults` for optional props.
- Do not mutate props directly; emit updates or copy into local state intentionally.
- Avoid losing reactivity by destructuring `reactive` without `toRefs`; be consistent with `ref` usage.
- Keep `computed` pure. Put side effects in event handlers or `watch`.
- Watchers need correct sources, cleanup for async requests, and controlled `deep` usage.
- Check route guards, Pinia stores, composables, and API modules for stale state after logout/tenant switch.

## React

- Hooks must be called unconditionally at component top level.
- `useEffect` dependencies must be complete; async effects need cancellation/ignore flags.
- Do not use `useEffect` for derived state or event-only work.
- Use `useMemo`/`useCallback` only when referential stability matters; do not cargo-cult optimize.
- Keep server/client boundaries clear in Next.js or RSC code; never import server secrets into client bundles.
- Review TanStack Query/SWR keys, cache invalidation, stale time, optimistic updates, and error handling.

## Flutter

- Dispose controllers, focus nodes, animation controllers, streams, and subscriptions.
- Avoid calling `setState` after `dispose`; check `mounted` after awaits.
- Keep build methods side-effect free and reasonably cheap.
- Review state management lifecycle for Provider/Riverpod/BLoC/GetX according to project conventions.
- Handle platform permissions, app lifecycle, network retries, and safe-area/layout overflow.
- For lists/images, check pagination, cache behavior, placeholder/error UI, and memory pressure.

## UI Regression Risks

- Text overflow in Chinese labels, narrow mobile screens, admin table columns, and long product/user names.
- Time/date display consistency: timezone, format, relative dates, and settlement/report day boundaries.
- File/export flows: progress, large files, repeated clicks, filename encoding, and permission failures.
- Form validation mismatch between frontend and backend, especially phone, ID card, money, percentage, and address fields.
