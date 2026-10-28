"""Build the portable OpenAI package from shared sources (Python 3.9+)."""

import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

OPENAI = Path(__file__).resolve().parent
ROOT = OPENAI.parent
SCHEMA_BASE = "https://agent-plugins.org/schemas/1.0.0"
SHARED_FIELDS = (
    "name", "version", "description", "author", "homepage", "repository",
    "license", "keywords",
)


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def encode_json(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def build(output_dir: Path) -> Path:
    shared = read_object(ROOT / ".claude-plugin/plugin.json")
    overlay = read_object(OPENAI / "manifest-overlay.json")
    if set(overlay) - {"description", "homepage", "extensions"}:
        raise ValueError("The OpenAI overlay may only override presentation metadata")
    manifest = {key: shared[key] for key in SHARED_FIELDS if key in shared}
    manifest.update(overlay)
    manifest["$schema"] = f"{SCHEMA_BASE}/plugin.schema.json"
    if manifest.get("name") != "attention":
        raise ValueError("Expected the shared Attention plugin identity")
    # The shared version also becomes part of the output filename.
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
                        manifest.get("version", "")):
        raise ValueError("The shared plugin version must be a semantic version")

    mcp = read_object(ROOT / ".mcp.json")
    mcp["$schema"] = f"{SCHEMA_BASE}/mcp.schema.json"
    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise ValueError("The shared MCP configuration must contain servers")
    for server in servers.values():
        if not isinstance(server, dict):
            raise ValueError("Each shared MCP server must be a JSON object")
        # Claude's HTTP transport is named streamable-http in Agent Plugins.
        if server.get("type") == "http":
            server["type"] = "streamable-http"

    interface = manifest["extensions"]["com.openai"]["interface"]
    for key, maximum in (("displayName", 30), ("shortDescription", 30),
                         ("longDescription", 4000)):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > maximum:
            raise ValueError(f"{key} must be nonblank and at most {maximum} characters")

    files = {"plugin.json": encode_json(manifest), "mcp.json": encode_json(mcp)}
    for directory, base in ((ROOT / "skills", ROOT), (OPENAI / "assets", OPENAI)):
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f"Expected a regular component directory: {directory}")
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlinks cannot be packaged: {path}")
            if path.is_file():
                files[path.relative_to(base).as_posix()] = path.read_bytes()
    if not any(Path(name).match("skills/*/SKILL.md") for name in files):
        raise ValueError("The package must contain a shared skill")
    for key in ("logo", "composerIcon"):
        value = interface[key]
        if not value.startswith("./") or ".." in value.split("/") or value[2:] not in files:
            raise ValueError(f"{key} must reference a contained packaged asset")
    license_path = ROOT / "LICENSE"
    if license_path.is_symlink():
        raise ValueError("The license cannot be a symlink")
    files["LICENSE"] = license_path.read_bytes()

    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"attention-openai-{manifest['version']}.zip"
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            # Stable timestamps and permissions make identical inputs reproducible.
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = ZIP_DEFLATED
            archive.writestr(entry, content)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OPENAI / "dist")
    args = parser.parse_args()
    try:
        print(build(args.output_dir).resolve())
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    main()
