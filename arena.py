#!/usr/bin/env python3
"""The arena: run downstream test suites on Biopython and BioPAIthon, report the delta."""

import argparse
import concurrent.futures
import datetime
import json
import os
import shlex
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
RESULTS = ROOT / "results"
SIDES = ("bio", "pai")
BAD = {"fail", "error"}


def sh(cmd, cwd=None, log=None, timeout=None, env=None):
    """Run a command, append its output to log, return (returncode, output)."""
    if log:
        with open(log, "a") as fh:
            fh.write(f"\n$ {cmd if isinstance(cmd, str) else shlex.join(cmd)}\n")
    try:
        p = subprocess.run(
            cmd, cwd=cwd, shell=isinstance(cmd, str), timeout=timeout, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace",
        )
        rc, out = p.returncode, p.stdout
    except subprocess.TimeoutExpired as e:
        rc, out = 124, (e.stdout or b"").decode(errors="replace") + "\n[timeout]\n"
    if log:
        with open(log, "a") as fh:
            fh.write(out)
    return rc, out


def clone(t, src, log):
    if src.exists():
        return 0
    cmd = ["git", "clone", "--quiet", "--filter=blob:none"]
    if t.get("submodules"):
        cmd.append("--recurse-submodules")
    if "ref" in t and not t.get("ref_is_commit"):
        cmd += ["--branch", t["ref"]]
    cmd += [t["repo"], str(src)]
    rc, _ = sh(cmd, log=log)
    if rc == 0 and t.get("ref_is_commit"):
        rc, _ = sh(["git", "checkout", "--quiet", t["ref"]], cwd=src, log=log)
    return rc


def build_venv(t, side, spec, d, src, args, log):
    venv = d / f"venv-{side}"
    py = venv / "bin" / "python"
    pyver = t.get("python", args.python)
    rc, _ = sh(["uv", "venv", "--quiet", "--clear", "--python", pyver, str(venv)], log=log)
    if rc:
        return None, "venv failed"
    pip = ["uv", "pip", "install", "--quiet", "--python", str(py)]
    pkgdir = src / t["subdir"] if "subdir" in t else src
    specs = [str(pkgdir) + s[1:] if s == "." or s.startswith(".[") else s for s in t.get("install", ["."])]
    # Builds from a checkout that the other side already built in are "dirty" to setuptools_scm.
    env = dict(os.environ, SETUPTOOLS_SCM_PRETEND_VERSION="0.0.0")
    if t.get("pre"):  # legacy setup.py projects need old setuptools and no build isolation
        rc, _ = sh(pip + t["pre"], log=log, timeout=600)
        if rc:
            return None, "pre-install failed"
    rc, out = sh(pip + t.get("flags", []) + specs + ["pytest", "pytest-cov"] + t.get("extra", []), log=log, timeout=1800, env=env)
    if rc:
        return None, "project install failed"
    # Whatever the project's resolver pulled in, the side under test wins.
    sh(["uv", "pip", "uninstall", "--quiet", "--python", str(py), "biopython", "biopaithon"], log=log)
    rc, _ = sh(pip + [spec], log=log, timeout=600)
    if rc:
        return None, f"{spec} install failed"
    rc, out = sh([str(py), "-c",
                  "import Bio, importlib.metadata as m; "
                  "print(Bio.__version__, sorted(m.packages_distributions().get('Bio', [])))"],
                 log=log)
    return py, out.strip()


def run_tests(t, side, py, d, src, args, log):
    junit = d / f"junit-{side}.xml"
    junit.unlink(missing_ok=True)
    cwd = src / t["subdir"] if "subdir" in t else src
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1",
               PATH=f"{py.parent}:{os.environ['PATH']}", VIRTUAL_ENV=str(py.parent.parent))
    cmd = f"{t.get('tests', 'pytest')} -q -p no:cacheprovider --continue-on-collection-errors --junitxml={junit}"
    rc, _ = sh(cmd, cwd=cwd, log=log, timeout=t.get("timeout", args.timeout), env=env)
    return rc, parse_junit(junit)


def parse_junit(path):
    if not path.exists():
        return {}
    out = {}
    for tc in ET.parse(path).iter("testcase"):
        tid = f"{tc.get('classname', '')}::{tc.get('name', '')}"
        tags = {c.tag for c in tc}
        if "failure" in tags:
            out[tid] = "fail"
        elif "error" in tags:
            out[tid] = "error"
        elif "skipped" in tags:
            out[tid] = "skip"
        else:
            out[tid] = "pass"
    return out


def compare(bio, pai):
    ids = set(bio) | set(pai)
    delta = {"regress": [], "improve": [], "only_bio": [], "only_pai": [], "changed": []}
    for tid in sorted(ids):
        a, b = bio.get(tid), pai.get(tid)
        if a is None:
            delta["only_pai"].append(tid)
        elif b is None:
            delta["only_bio"].append(tid)
        elif a == b:
            continue
        elif a == "pass" and b in BAD:
            delta["regress"].append(tid)
        elif a in BAD and b == "pass":
            delta["improve"].append(tid)
        else:
            delta["changed"].append(f"{tid} {a}->{b}")
    return delta


def run_target(t, args):
    name = t["name"]
    d = WORK / name
    d.mkdir(parents=True, exist_ok=True)
    log = d / "arena.log"
    res = {"name": name, "sides": {}, "status": "ok"}
    if clone(t, d / "src", log):
        res["status"] = "clone failed"
        return finish(res)
    src = d / "src"
    if "patch" in t and not (d / ".patched").exists():
        sh(t["patch"], cwd=src / t["subdir"] if "subdir" in t else src, log=log)
        (d / ".patched").touch()
    outcomes = {}
    for side in SIDES:
        py, info = build_venv(t, side, getattr(args, side), d, src, args, log)
        if py is None:
            res["sides"][side] = {"status": info}
            continue
        rc, outcomes[side] = run_tests(t, side, py, d, src, args, log)
        counts = {k: sum(1 for v in outcomes[side].values() if v == k) for k in ("pass", "fail", "error", "skip")}
        res["sides"][side] = {"status": "ran", "bio": info, "rc": rc, **counts}
    if len(outcomes) < 2:
        res["status"] = "dropped" if not outcomes else "one side failed to install"
    else:
        res["delta"] = compare(*(outcomes[s] for s in SIDES))
        if not outcomes["bio"] and not outcomes["pai"]:
            res["status"] = "no tests collected"
    return finish(res)


def finish(res):
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{res['name']}.json").write_text(json.dumps(res, indent=1))
    d = res.get("delta", {})
    print(f"{res['name']:<22} {res['status']:<28} regress={len(d.get('regress', []))} "
          f"improve={len(d.get('improve', []))} only_bio={len(d.get('only_bio', []))} "
          f"only_pai={len(d.get('only_pai', []))}", flush=True)
    return res


def report(results, args):
    lines = ["# Arena report", "",
             f"`{args.bio}` (bio) vs `{args.pai}` (pai), run {datetime.date.today()}.", "",
             "| target | status | tests | pass bio | pass pai | regress | improve | only bio | only pai | other |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    details = []
    for r in sorted(results, key=lambda r: r["name"]):
        s = r["sides"]
        d = r.get("delta", {})
        b, p = s.get("bio", {}), s.get("pai", {})
        n = sum(b.get(k, 0) for k in ("pass", "fail", "error", "skip"))
        lines.append(f"| {r['name']} | {r['status']} | {n} | {b.get('pass', '-')} | {p.get('pass', '-')} | "
                     f"{len(d.get('regress', []))} | {len(d.get('improve', []))} | "
                     f"{len(d.get('only_bio', []))} | {len(d.get('only_pai', []))} | {len(d.get('changed', []))} |")
        for key in ("regress", "only_bio", "changed", "improve", "only_pai"):
            if d.get(key):
                details.append(f"\n## {r['name']}: {key}\n")
                details += [f"- `{x}`" for x in d[key][:200]]
                if len(d[key]) > 200:
                    details.append(f"- ... {len(d[key]) - 200} more")
        for side in SIDES:
            if s.get(side, {}).get("status") != "ran":
                details.append(f"\n## {r['name']}: {side} {s.get(side, {}).get('status', 'not run')}\n")
    lines += ["", "Side info (Bio.__version__ and the distribution that provides `Bio`):", ""]
    for r in sorted(results, key=lambda r: r["name"]):
        for side in SIDES:
            if "bio" in r["sides"].get(side, {}):
                lines.append(f"- {r['name']} {side}: `{r['sides'][side]['bio']}`")
    text = "\n".join(lines + details) + "\n"
    (ROOT / "REPORT.md").write_text(text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "report"])
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--bio", default="biopython==1.88")
    ap.add_argument("--pai", default="biopaithon==1.88")
    ap.add_argument("--python", default="3.12")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=2400, help="seconds per test run")
    args = ap.parse_intermixed_args()

    if args.cmd == "report":
        results = [json.loads(p.read_text()) for p in sorted(RESULTS.glob("*.json"))]
        print(report(results, args))
        return

    targets = tomllib.loads((ROOT / "targets.toml").read_text())["target"]
    if args.targets:
        targets = [t for t in targets if t["name"] in args.targets]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(lambda t: run_target(t, args), targets))
    report([json.loads(p.read_text()) for p in sorted(RESULTS.glob("*.json"))], args)
    print(f"\nwrote {ROOT / 'REPORT.md'}")


if __name__ == "__main__":
    sys.exit(main())
