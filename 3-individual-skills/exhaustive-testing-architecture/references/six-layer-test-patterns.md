# Six-Layer Test Patterns (Phoney `code01`–`code110` Reference)

These patterns distill how the Phoney codebase grew to **649 Vitest tests across 112 files**, **203 native Android JVM tests across 44 suites**, **18 website runtime/asset tests**, and **18 Python compliance/artifact negative-control tests** without relying on fragile UI snapshots or fake SQL mocks.

---

## Layer 1: Pure State-Machine & Policy Suite

**When to use**: Before wiring any UI screen, onboarding flow, audio controller, or native Accessibility/InCall service.

**Pattern**:
1. Define a pure state type and explicit event union.
2. Return both the next state and declarative side-effect intents (for example, `speakPrompt`, `openSettings`, `persistStep`, `abortSession`) instead of executing side effects inline.
3. Test every transition, guard condition, timeout, and cancellation race:

```ts
// Example: testing rapid switching and cancellation during async decoding
it('cancels the in-flight request when a newer selection or Stop arrives', async () => {
  const controller = createPlaybackController(fakeLoader);
  const first = controller.select('cheer');
  const second = controller.select('wow');
  await Promise.all([first, second]);
  expect(controller.activeSoundId()).toBe('wow');
  expect(fakeLoader.abortedIds).toEqual(['cheer']);
});
```

---

## Layer 2: In-Memory Real Postgres (`PGlite`) Migration & Privilege Suite

**When to use**: Any project using PostgreSQL, Supabase, RLS policies, SQL triggers, or RPC functions.

**Pattern**:
1. Boot `new PGlite()` in memory.
2. Bootstrap minimal `auth.users`, `auth.uid()`, `auth.jwt()`, and roles (`anon`, `authenticated`, `service_role`).
3. Apply every file in `supabase/migrations/*.sql` in lexical order.
4. Execute queries under `SET LOCAL ROLE anon` and `SET LOCAL ROLE authenticated` with `request.jwt.claim.sub` set to specific test UUIDs:

```ts
it('blocks anonymous and signed-in clients from administrative RPCs while permitting public catalog reads', async () => {
  await expect(runAsAnon(db, `SELECT public.admin_upsert_sound_pack(...)`)).rejects.toThrow(/permission denied/i);
  await expect(runAsUser(db, userA, `SELECT public.admin_upsert_sound_pack(...)`)).rejects.toThrow(/permission denied/i);
  const catalog = await runAsAnon(db, `SELECT * FROM public.list_published_sound_packs()`);
  expect(catalog.rows.length).toBeGreaterThan(0);
});
```

---

## Layer 3: Cryptographic & External-Input Boundary Suite

**When to use**: Webhook verification (AdMob SSV, Stripe, GitHub), OAuth PKCE callbacks, signed access proofs, CLI/API file ingestion.

**Pattern**:
- Generate ephemeral key pairs (`crypto.generateKeyPairSync('ed25519')` or `'ec'`) in the test.
- Verify valid signatures pass, then systematically mutate the query string, user ID, reward amount, key ID, and signature bytes to prove each mutation fails closed.
- Test key rotation rate bounds so an attacker sending random `key_id` values cannot trigger unbounded upstream key fetches.

---

## Layer 4: Negative-Control Build & Release Guard Suite

**When to use**: Gradle/Xcode release configs, bundler plugins, CSP headers, environment variable gates, and preflight scripts.

**Pattern**:
- Write a script or test that copies or parameterizes the release input and intentionally introduces one violation at a time:
  - `minifyEnabled = false` in release
  - Debug signing key or mismatched upload certificate SHA-256
  - Unverified third-party sound or screenshot hash
  - Prohibited package/permission string in `AndroidManifest.xml` or DEX
  - Path escape (`../package.json`) or missing rights evidence in operator pack drafts
- Assert that the guard exits non-zero and names the specific violated invariant.

---

## Layer 5: Byte-Level Artifact & Provenance Verifier

**When to use**: Release APKs/AABs, static website outputs, downloadable source/compliance archives, and media catalogs.

**Pattern**:
- Open the compiled `.apk` / `.aab` / `.zip` as a zip archive and parse:
  - `classes*.dex` string tables for prohibited symbols or leaked test keys
  - `lib/**/*.so` ELF program headers (`p_align >= 16384` for Android 15+ 16 KB page compatibility)
  - `assets/**` and `res/raw/**` SHA-256 digests against the committed rights manifest
  - WAV RIFF headers (`sampleRate * channels * bitsPerSample / 8`) to verify `durationMs` matches actual PCM sample bytes rather than an invented number.

---

## Layer 6: Cross-Layer Reconciliation Ledger

Before claiming completion on a multi-part task, reconcile all six layers in `.unlazy/<task>/GATES.md` or `docs/TEST_RESULTS.md`:

| Layer | Command / Oracle | Positive & Negative Control | Status |
| --- | --- | --- | --- |
| L1 Pure State/Policy | `npx vitest run src/**` | Valid transitions + cancellation/stale-event rejection | observed |
| L2 Real DB/RLS | `npx vitest run tests/backend/**` | Authorized RPC + cross-user/anon `permission denied` | observed |
| L3 Crypto/Input | `npx vitest run tests/security/**` | Valid signature + tampered/replayed/path-escape rejection | observed |
| L4 Build Guards | `node scripts/security/verify-release-guards.cjs` | Clean release pass + broken-flag rejection | observed |
| L5 Byte Verifiers | `python scripts/security/test-play-artifacts.py` | Clean artifact pass + seeded prohibited-string failure | observed |
| L6 Runtime/Device | Browser DevTools / ADB / physical call | Rendered frame / receiver audio ground truth | observed / scoped |
