---
name: gstack-upgrade
version: 1.1.0
description: >
  Use this skill to upgrade gstack to the latest version. Detects global vs vendored install, runs the upgrade, and shows what's new. Also supports inline upgrade flow triggered by update checks from other skills.
allowed-tools:
  - Bash
  - Read
  - Write
  - Question
---

# gstack-upgrade

Upgrade gstack to the latest version and show what's new.

## Inline upgrade flow

This section is referenced by other skills when they detect an upgrade is available.

### Step 1: Ask the user (or auto-upgrade)

First, check if auto-upgrade is enabled:
```bash
_AUTO=""
[ "${GSTACK_AUTO_UPGRADE:-}" = "1" ] && _AUTO="true"
[ -z "$_AUTO" ] && _AUTO=$("$GSTACK_DIR/bin/gstack-config" get auto_upgrade 2>/dev/null || true)
echo "AUTO_UPGRADE=$_AUTO"
```

The `GSTACK_DIR` should be set to the gstack installation directory (e.g., `~/.claude/skills/gstack` or `.claude/skills/gstack`).

**If `AUTO_UPGRADE=true`:** Skip Question. Log "Auto-upgrading gstack v{old} → v{new}..." and proceed directly to Step 2. If `./setup` fails during auto-upgrade, restore from backup (`.bak` directory) and warn the user.

**Otherwise**, use Question:
- Question: "gstack **v{new}** is available (you're on v{old}). Upgrade now?"
- Options: ["Yes, upgrade now", "Always keep me up to date", "Not now", "Never ask again"]

**If "Yes, upgrade now":** Proceed to Step 2.

**If "Always keep me up to date":**
```bash
$GSTACK_DIR/bin/gstack-config set auto_upgrade true
```
Then proceed to Step 2.

**If "Not now":** Write snooze state with escalating backoff (first snooze = 24h, second = 48h, third+ = 1 week), then continue with the current skill.
```bash
_SNOOZE_FILE=~/.gstack/update-snoozed
_REMOTE_VER="{new}"
_CUR_LEVEL=0
if [ -f "$_SNOOZE_FILE" ]; then
  _SNOOZED_VER=$(awk '{print $1}' "$_SNOOZE_FILE")
  if [ "$_SNOOZED_VER" = "$_REMOTE_VER" ]; then
    _CUR_LEVEL=$(awk '{print $2}' "$_SNOOZE_FILE")
    case "$_CUR_LEVEL" in *[!0-9]*) _CUR_LEVEL=0 ;; esac
  fi
fi
_NEW_LEVEL=$((_CUR_LEVEL + 1))
[ "$_NEW_LEVEL" -gt 3 ] && _NEW_LEVEL=3
echo "$_REMOTE_VER $_NEW_LEVEL $(date +%s)" > "$_SNOOZE_FILE"
```

**If "Never ask again":**
```bash
$GSTACK_DIR/bin/gstack-config set update_check false
```
Continue with the current skill.

### Step 2: Detect install type

```bash
_GSTACK_DIR=""
if [ -d "$HOME/.claude/skills/gstack/.git" ]; then
  _GSTACK_DIR="$HOME/.claude/skills/gstack"
  INSTALL_TYPE="global-git"
elif [ -d ".claude/skills/gstack/.git" ]; then
  _GSTACK_DIR=".claude/skills/gstack"
  INSTALL_TYPE="local-git"
elif [ -d ".claude/skills/gstack" ]; then
  _GSTACK_DIR=".claude/skills/gstack"
  INSTALL_TYPE="vendored"
elif [ -d "$HOME/.claude/skills/gstack" ]; then
  _GSTACK_DIR="$HOME/.claude/skills/gstack"
  INSTALL_TYPE="vendored-global"
else
  echo "ERROR: gstack not found"
  exit 1
fi
echo "Install type: $INSTALL_TYPE at $_GSTACK_DIR"
```

### Step 3: Save old version

```bash
OLD_VERSION=$(cat "$_GSTACK_DIR/VERSION" 2>/dev/null || echo "unknown")
```

### Step 4: Upgrade

**For git installs:**
```bash
cd "$_GSTACK_DIR"
STASH_OUTPUT=$(git stash 2>&1)
git fetch origin
git reset --hard origin/main
./setup
```

**For vendored installs:**
```bash
PARENT=$(dirname "$_GSTACK_DIR")
TMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/garrytan/gstack.git "$TMP_DIR/gstack"
mv "$_GSTACK_DIR" "$_GSTACK_DIR.bak"
mv "$TMP_DIR/gstack" "$_GSTACK_DIR"
cd "$_GSTACK_DIR" && ./setup
rm -rf "$_GSTACK_DIR.bak" "$TMP_DIR"
```

### Step 4.5: Sync local vendored copy

After upgrading the primary install, check if there's also a local copy in the current project:
```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
LOCAL_GSTACK=""
if [ -n "$_ROOT" ] && [ -d "$_ROOT/.claude/skills/gstack" ]; then
  _RESOLVED_LOCAL=$(cd "$_ROOT/.claude/skills/gstack" && pwd -P)
  _RESOLVED_PRIMARY=$(cd "$_GSTACK_DIR" && pwd -P)
  if [ "$_RESOLVED_LOCAL" != "$_RESOLVED_PRIMARY" ]; then
    LOCAL_GSTACK="$_ROOT/.claude/skills/gstack"
  fi
fi
```

If `LOCAL_GSTACK` is non-empty, update it from the freshly-upgraded primary install:
```bash
mv "$LOCAL_GSTACK" "$LOCAL_GSTACK.bak"
cp -Rf "$_GSTACK_DIR" "$LOCAL_GSTACK"
rm -rf "$LOCAL_GSTACK/.git"
cd "$LOCAL_GSTACK" && ./setup
rm -rf "$LOCAL_GSTACK.bak"
```

### Step 5: Write marker + clear cache

```bash
mkdir -p ~/.gstack
echo "$OLD_VERSION" > ~/.gstack/just-upgraded-from
rm -f ~/.gstack/last-update-check
rm -f ~/.gstack/update-snoozed
```

### Step 6: Show What's New

Read `$_GSTACK_DIR/CHANGELOG.md`. Find all version entries between the old version and the new version. Summarize as 5-7 bullets grouped by theme. Focus on user-facing changes.

### Step 7: Continue

After showing What's New, continue with whatever skill the user originally invoked.

## Standalone usage

When invoked directly (not from a preamble), follow Steps 2-6 above. If already on the latest version, tell the user: "You're already on the latest version (v{version})."
