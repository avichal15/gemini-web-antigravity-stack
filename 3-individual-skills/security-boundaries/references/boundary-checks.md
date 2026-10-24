# Boundary check matrix

Use this as an abuse-case selector, not as a universal pass/fail checklist. The exact framework, provider and regulation must be verified for the target product.

| Boundary | Failure to try | Decisive evidence |
| --- | --- | --- |
| Input/API | Oversized, malformed, duplicated, out-of-order, encoded or unexpected fields | Handler rejects before side effects; valid control still succeeds |
| Authentication | Missing, expired, switched, revoked or replayed session | Protected action denied; state clears or refreshes without leaking another account |
| Authorization/database | User A reads/writes User B's row; anonymous user calls privileged RPC; client writes a server-owned field | Actual policy engine denies cross-principal operations; intended owner path succeeds |
| Upload/storage | Wrong MIME/content, path traversal, symlink, oversized or duplicate object, partial write | Admission rejects or quarantines; originals/previous valid objects remain intact |
| Webhook/reward | Forged signature, changed field order/amount/user, duplicate delivery, timeout before commit, unknown verifier key | No grant before verified durable transaction; legitimate retry is idempotent and reconciled |
| Offline/cache | Clock rollback, account switch, copied proof, expired entitlement, corrupt restored file | Local UI hides invalid access; server authority remains intact; core use still works |
| Migration/deletion | Existing records lost, tombstones revived, partial failure, backfill repeated | Old-to-new fixture and positive deletion control detect loss; rollback/recovery path documented |
| Release artifact | Debug signer, secret bundled, minification disabled, unexpected exported component/permission, private asset included | Inspect exact package/config; negative guard control fails for the intended reason |
| Privacy/rights | Log includes token or personal data; media/contacts uploaded unexpectedly; uncleared asset enters public build | Inspect data flow, logs and built bytes; match disclosures and rights evidence |

Classify each result by environment. A local database test does not prove hosted RLS; a release-config script does not prove store approval; a private repo does not prevent client extraction.
