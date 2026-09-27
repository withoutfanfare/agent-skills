---
name: notarise
description: >-
  Takes a built macOS app, from Tauri or Xcode and Swift, to something a
  client can open without a Gatekeeper warning: Developer ID signing with
  hardened runtime and entitlements, notarisation with `xcrun notarytool`,
  stapling, and packaging as a DMG or zip. Use when the user wants to ship
  a Mac app to someone else, sees "app is damaged and can't be opened", or
  asks about notarisation, codesigning for distribution, or Gatekeeper.
  Not for building the app (use `tauri` or `swift`), and not for the App
  Store.
license: MIT
allowed-tools: Read Grep Glob Bash
---

# Notarise

Gatekeeper does not check that an app is safe; it checks that Apple has
seen it. Getting a build past that check is a fixed sequence, sign, submit,
staple, and most failures come from doing one of those steps to the wrong
file, in the wrong order, or with the wrong certificate type, not from the
app itself.

## 1. Identify the artefact and the certificate

Work out what you are shipping: a Tauri bundle
(`src-tauri/target/release/bundle/macos/<App>.app`) or an Xcode archive
exported to a `.app`. Both need the same treatment from here on.

Check the signing certificate in the keychain:

```bash
security find-identity -v -p codesigning
```

You need a **Developer ID Application** certificate, not "Apple
Development" or "Mac App Store"; those are for local runs and App Store
submission respectively, and notarisation rejects a build signed with
either.

Done when: the certificate's name (`Developer ID Application: <Name>
(<TEAMID>)`) is confirmed and copied for the next step.

## 2. Sign with hardened runtime, innermost first

Sign nested binaries and frameworks before the outer app bundle; the notary
service rejects an app whose inner components are unsigned or signed
after the outer bundle in a way that invalidates its seal:

```bash
codesign --force --options runtime --timestamp \
  --sign "Developer ID Application: <Name> (<TEAMID>)" \
  path/to/Inner.framework

codesign --force --options runtime --timestamp \
  --entitlements entitlements.plist \
  --sign "Developer ID Application: <Name> (<TEAMID>)" \
  path/to/App.app
```

`--options runtime` turns on the hardened runtime, required for
notarisation. `--timestamp` requests a secure timestamp; a build signed
with `--timestamp=none` is refused. Entitlements belong on executables, not
frameworks. Add only the entitlements the app actually needs (`com.apple.security.cs.allow-jit`,
`disable-library-validation`, and similar); an unused one widens the
app's attack surface for no benefit. Tauri's bundler and `xcodebuild
-exportArchive` both sign for you when a Developer ID identity and
entitlements are already configured; do this by hand only when packaging
outside those tools.

Done when: `codesign --verify --deep --strict --verbose=2 App.app` reports
no errors.

## 3. Store credentials once, use the profile everywhere

Create a keychain profile a single time, and never put a password or API
key in a command line or file after that:

```bash
xcrun notarytool store-credentials "notary-profile" \
  --apple-id "sam@example.com" --team-id "ABCDE12345"
```

Leave out `--password`: the tool then asks for the app-specific password
at a prompt, so it never reaches shell history.

For CI, use an App Store Connect API key instead (`--key`, `--key-id`,
`--issuer`) stored as a CI secret; a keychain profile lives only on the
machine that created it. `pipeline` (if installed) covers CI secrets more
generally.

Done when: `xcrun notarytool history --keychain-profile "notary-profile"`
returns without asking for credentials again.

## 4. Package the thing you will actually ship, then notarise that

Notarise the exact artefact a client will download and open, a DMG or a
zip of the signed `.app`, not the bare `.app` and not an intermediate
build product. A zip made for upload (`ditto -c -k --keepParent App.app
App.zip`) is fine to notarise but cannot itself be stapled; only a `.app`,
a DMG or a `.pkg` can carry a staple. If you package a DMG, sign it too
(`codesign --timestamp --sign "Developer ID Application: ..." App.dmg`) after the
`.app` inside it is already signed.

Done when: you can point at one file and say "this is what ships", and it
is signed.

## 5. Submit and wait

```bash
xcrun notarytool submit App.dmg \
  --keychain-profile "notary-profile" --wait
```

`--wait` blocks until Apple returns Accepted, Invalid or Rejected instead
of leaving you to poll. On anything but Accepted, pull the log before
guessing:

```bash
xcrun notarytool log <submission-id> --keychain-profile "notary-profile"
```

The log names the exact binary and problem (unsigned nested binary,
missing hardened runtime, missing secure timestamp); fix that file rather
than re-signing the whole bundle and resubmitting blind.

Done when: the submission status is Accepted, or the log names the file
and reason for a rejection.

## 6. Staple and verify

```bash
xcrun stapler staple App.dmg
xcrun stapler validate App.dmg
spctl -a -vvv -t open --context context:primary-signature App.dmg
```

For a bare `.app` use `spctl -a -vvv -t exec App.app`; `-t install` is for
`.pkg` installers.

Stapling attaches the notarisation ticket to the file, so Gatekeeper can
check it offline on first launch; an accepted-but-unstapled build still
works, but only while the opening machine can reach Apple's servers.
`spctl` runs the same check Gatekeeper does, and should report `accepted`
and `source=Notarized Developer ID`.

Done when: all three commands above pass on the file you are about to
hand over.

## Tauri's own signing and notarisation

Tauri reads `APPLE_CERTIFICATE` (base64 `.p12`), `APPLE_CERTIFICATE_PASSWORD`,
`APPLE_SIGNING_IDENTITY`, `APPLE_ID`, `APPLE_PASSWORD` (an app-specific
password) and `APPLE_TEAM_ID` from the environment during `tauri build`,
alongside `bundle.macOS.signingIdentity` and `bundle.macOS.entitlements` in
`tauri.conf.json`. Set these as CI secrets, never committed to the config
file or typed into a shell history. Given these, `tauri build` signs and
notarises the app bundle as part of the bundle step. Check the DMG it
produces with step 6 rather than assuming it is notarised and stapled too;
if it is not, notarise and staple the DMG with steps 5 and 6. The manual
steps are also for diagnosing a failure the bundler reports.

Common failure shapes, and Tauri's own env var names, are catalogued in
[references/failures.md](references/failures.md).

Done when: `tauri build` (or your manual sequence) completes with no
Gatekeeper warning on the artefact that ships.

## It's working if

- `codesign --verify --deep --strict`, `spctl` and `stapler validate` all
  pass on the exact file that ships.
- Opening the file on another Mac, one that has never seen this build, is
  clean of any Gatekeeper warning, including offline.
- No password, API key or certificate secret appears in a command line,
  shell history, or file tracked by the repository.
