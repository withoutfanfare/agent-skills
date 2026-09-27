# Common notarisation failures

## The notary log's usual entries

- **"The signature does not include a secure timestamp."** The binary was
  signed with `--timestamp=none`, or an old signature from before you
  added `--timestamp` is still in place on a nested file. Re-sign that
  specific file with `--timestamp` and resubmit.
- **"The executable does not have the hardened runtime enabled."** A
  nested binary or framework was signed without `--options runtime`, often
  because it was signed once by hand before the outer app's build step
  re-signed everything else. Sign the missing file explicitly, innermost
  first, then re-sign the outer bundle.
- **"The signature of the binary is invalid."** or a nested binary is
  unsigned: a bundled helper tool, a `.dylib` pulled in by a dependency, or
  a downloaded binary embedded in `Resources/` was never signed at all.
  List every executable inside the bundle (`find App.app -type f -perm
  +111`) and confirm each one has a signature before signing the outer
  app.
- **Wrong certificate type.** A build signed with "Apple Development" or
  "3rd Party Mac Developer Application" (the App Store certificate) is
  rejected outright; only "Developer ID Application" is valid for
  notarisation. `codesign -dvvv App.app` shows which identity actually
  signed it.
- **Notarised the zip, shipped the DMG unstapled.** A zip made only to
  satisfy notarytool's upload format cannot itself carry a staple. If a
  DMG or `.app` is what ships, staple that file specifically, after
  notarisation, not the zip that was uploaded.

## Tauri-specific

- Tauri's bundler looks for `APPLE_SIGNING_IDENTITY` (or
  `bundle.macOS.signingIdentity`) and will silently produce an
  **unsigned** build if neither is set; there is no build failure, only a
  Gatekeeper warning later. Confirm the identity is picked up by checking
  `codesign -dvvv` on the produced `.app` before assuming signing ran.
- `APPLE_TEAM_ID` is required alongside `APPLE_ID` and `APPLE_PASSWORD` for
  notarisation to run at all; missing it produces an authentication error
  from `notarytool` that reads like a wrong password.
- An app-specific password (generated at appleid.apple.com, not the
  account password itself) is required for `APPLE_PASSWORD`; the account
  password itself is always rejected.

## Out of scope

App Store distribution uses a different certificate ("Apple Distribution")
and a different pipeline (Xcode Cloud, Transporter, or `altool`/App Store
Connect submission), with no notarisation or stapling step at all. None of
the above applies there.
