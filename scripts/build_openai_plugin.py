"""Validate and bundle the Attention OpenAI plugin for submission."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "plugin.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    mcp = json.loads((ROOT / "mcp.json").read_text())
    claude_mcp = json.loads((ROOT / ".mcp.json").read_text())
    assert manifest["name"] == "attention"
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert mcp["mcpServers"]["attention"]["url"] == claude_mcp["mcpServers"]["attention"]["url"]
    assert mcp["mcpServers"]["attention"]["type"] == "streamable-http"
    review = manifest["extensions"]["com.openai"]["review"]["test_cases"]
    assert len(review["positive"]) == 5 and len(review["negative"]) == 3
    package_files = [
        "plugin.json",
        "mcp.json",
        "skills/conversations/SKILL.md",
        "assets/attention-icon.png",
        "LICENSE",
    ]
    interface = manifest["extensions"]["com.openai"]["interface"]
    for field in ("logo", "composerIcon"):
        assert (ROOT / interface[field]).is_file()
    assert len(interface["displayName"]) <= 30
    assert len(interface["shortDescription"]) <= 30
    assert len(interface["longDescription"]) <= 4000
    output = ROOT / "dist" / f"attention-openai-{manifest['version']}.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for relative in package_files:
            archive.write(ROOT / relative, relative)
    print(output)


if __name__ == "__main__":
    main()
