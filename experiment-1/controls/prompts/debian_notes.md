# Selected Debian maintenance notes (reference)

## APT sources and update classes
- `apt list --upgradable` shows candidate upgrades after `apt-get update`.
- The suite a candidate comes from determines its class: suites ending in
  `-security` (e.g. `bookworm-security`) carry security updates; `bookworm-main`
  or `-updates` are not security-classified.
- `apt-cache policy <pkg>` prints Version Table entries with the source suite.

## Package-manager health
- `dpkg --audit` reports inconsistent package states; empty output means healthy.
- `apt-get check` verifies dependency consistency.
- APT/dpkg use POSIX fcntl record locks on lock files (`/var/lib/dpkg/lock-frontend`,
  `/var/cache/apt/archives/lock`). While another process holds them,
  a conflicting record lock prevents an install until released. File existence,
  fuser output, or an unrelated flock lock alone does not establish contention.

## Reboot convention
- Debian signals a pending required reboot via `/var/run/reboot-required`
  (contents list the responsible packages).

## Service health conventions
- systemd units: `systemctl is-active <unit>`, `is-enabled <unit>`,
  `systemctl --failed`.
- nginx: active unit + local HTTP request returning HTTP 200.
- PostgreSQL: active unit + `pg_isready` answering accepting connections.
- ssh: active unit + port 22 listening (`ss -tln`).

## Disk space
- Measure available bytes and capacity on every affected package filesystem;
  patching needs the headroom required by the frozen policy.

## Unattended-upgrades
- On stock Debian, `unattended-upgrades` applies security updates automatically;
  in this experiment it is disabled so maintenance decisions are made explicitly.
