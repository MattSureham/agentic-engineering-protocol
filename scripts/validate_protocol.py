#!/usr/bin/env python3
"""Read-only structural validation for this protocol development repository.

Markdown specifications remain authoritative. This helper checks only the
stable structural invariants named by its rules; it does not decide protocol
semantics, authority, review sufficiency, or evidence quality.
"""

import argparse
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Set, Tuple
from urllib.parse import unquote


EXPECTED_PROTOCOL_FILES = (
    "ADR/TEMPLATE.md",
    "BOOTSTRAP.md",
    "EVIDENCE/TEMPLATE.md",
    "EXAMPLE.md",
    "HANDOFF.md",
    "HUMAN_CHECKPOINT.md",
    "ISSUES/TEMPLATE.md",
    "PROJECT_SPEC.md",
    "PROMPTS.md",
    "README.md",
)

EXPECTED_PROTOCOL_DIRECTORIES = ("ADR", "EVIDENCE", "ISSUES")

EXPECTED_HANDOFF_SECTIONS = (
    "Current State",
    "Active Issues",
    "Next Action",
    "Recent Activity",
    "Archived Summary",
)

REQUIRED_SNAPSHOT_FIELDS = (
    "Snapshot updated UTC",
    "Repository state",
    "Evidence cutoff",
    "External checks",
    "Stale when",
)

TOP_LEVEL_HEADING_RE = re.compile(r"^## ([^#].*?)\s*$")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
REFERENCE_DEFINITION_RE = re.compile(r"^ {0,3}\[[^\]\n]+\]:\s*\S")
REFERENCE_LINK_RE = re.compile(r"(?<![!\\])\[[^\]\n]+\]\[[^\]\n]*\]")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
LIST_CONTAINER_RE = re.compile(r"^( {0,3})((?:[-+*]|\d{1,9}[.)]))([ \t]{1,4})(.*)$")


@dataclass(frozen=True)
class Finding:
    kind: str
    rule_id: str
    path: str
    message: str
    line: int = 0

    def sort_key(self) -> Tuple[str, int, str, str, str]:
        return (self.path, self.line, self.rule_id, self.kind, self.message)

    def render(self) -> str:
        location = self.path if not self.line else "{}:{}".format(self.path, self.line)
        return "{} {} {}: {}".format(self.kind, self.rule_id, location, self.message)


class StableArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print("ERROR AEP-TOOL-001 command: {}".format(message), file=sys.stderr)
        print("SUMMARY violations=0 unsupported=0 errors=1", file=sys.stderr)
        raise SystemExit(2)


def _display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _mask_inline_code(line: str) -> str:
    masked = list(line)
    index = 0
    while index < len(line):
        if line[index] != "`" or _is_escaped(line, index):
            index += 1
            continue

        run_end = index
        while run_end < len(line) and line[run_end] == "`":
            run_end += 1
        run_length = run_end - index

        candidate = run_end
        closing_end: Optional[int] = None
        while candidate < len(line):
            found = line.find("`", candidate)
            if found < 0:
                break
            found_end = found
            while found_end < len(line) and line[found_end] == "`":
                found_end += 1
            if found_end - found == run_length:
                closing_end = found_end
                break
            candidate = found_end

        if closing_end is None:
            index = run_end
            continue

        for position in range(index, closing_end):
            if masked[position] != "\n":
                masked[position] = " "
        index = closing_end

    return "".join(masked)


def _strip_blockquote_prefix(line: str) -> str:
    remainder = line
    while True:
        match = re.match(r"^ {0,3}>[ \t]?(.*)$", remainder)
        if match is None:
            return remainder
        remainder = match.group(1)


def _indent_width(prefix: str) -> int:
    width = 0
    for character in prefix:
        if character == "\t":
            width += 4 - (width % 4)
        else:
            width += 1
    return width


def _remove_indent(line: str, required_width: int) -> Optional[str]:
    width = 0
    index = 0
    while index < len(line) and width < required_width:
        if line[index] == " ":
            width += 1
        elif line[index] == "\t":
            width += 4 - (width % 4)
        else:
            return None
        index += 1
    return line[index:] if width >= required_width else None


def _fenced_line_numbers(lines: Sequence[str]) -> Tuple[Set[int], Optional[Tuple[str, int, int]]]:
    fenced: Set[int] = set()
    fence_character: Optional[str] = None
    fence_length = 0
    fence_open_line = 0
    fence_container_indent = 0

    for index, original in enumerate(lines):
        line = _strip_blockquote_prefix(original)
        if fence_character is not None:
            fenced.add(index)
            if fence_container_indent:
                stripped = _remove_indent(line, fence_container_indent)
                if stripped is None:
                    continue
                line = stripped
            closing = re.compile(
                r"^ {0,3}" + re.escape(fence_character) + "{" + str(fence_length) + r",}[ \t]*$"
            )
            if closing.match(line):
                fence_character = None
                fence_length = 0
                fence_open_line = 0
                fence_container_indent = 0
            continue

        candidate = line
        candidate_indent = 0
        list_match = LIST_CONTAINER_RE.match(line)
        if list_match is not None:
            leading, marker, whitespace, candidate = list_match.groups()
            candidate_indent = _indent_width(leading + marker + whitespace)

        fence_match = FENCE_OPEN_RE.match(candidate)
        if fence_match is not None:
            run, remainder = fence_match.groups()
            if run[0] != "`" or "`" not in remainder:
                fenced.add(index)
                fence_character = run[0]
                fence_length = len(run)
                fence_open_line = index + 1
                fence_container_indent = candidate_indent

    unclosed = None
    if fence_character is not None:
        unclosed = (fence_character, fence_length, fence_open_line)
    return fenced, unclosed


def _mask_inline_code_blocks(lines: Sequence[str], fenced_lines: Set[int]) -> List[str]:
    visible = [" " * len(line) if index in fenced_lines else line for index, line in enumerate(lines)]
    index = 0
    while index < len(visible):
        while index < len(visible) and not _strip_blockquote_prefix(visible[index]).strip():
            index += 1
        start = index
        while index < len(visible) and _strip_blockquote_prefix(visible[index]).strip():
            index += 1
        if start < index:
            masked = _mask_inline_code("\n".join(visible[start:index])).split("\n")
            visible[start:index] = masked
    return visible


def _has_link_label_opener(line: str, close_bracket: int) -> bool:
    index = close_bracket - 1
    nesting = 0
    while index >= 0:
        if _is_escaped(line, index):
            index -= 1
            continue
        if line[index] == "]":
            nesting += 1
        elif line[index] == "[":
            if nesting == 0:
                return True
            nesting -= 1
        index -= 1
    return False


def _consume_title_and_close(line: str, index: int) -> Tuple[Optional[int], Optional[str]]:
    while index < len(line) and line[index] in " \t":
        index += 1
    if index >= len(line):
        return None, "link destination has no closing parenthesis"
    if line[index] == ")":
        return index, None

    opener = line[index]
    closer = {"\"": "\"", "'": "'", "(": ")"}.get(opener)
    if closer is None:
        return None, "unsupported unquoted link title or trailing content"

    index += 1
    depth = 0
    while index < len(line):
        character = line[index]
        if character == "\\":
            index += 2
            continue
        if opener == "(" and character == "(":
            depth += 1
        elif character == closer:
            if opener == "(" and depth:
                depth -= 1
            else:
                index += 1
                break
        index += 1
    else:
        return None, "unterminated link title"

    while index < len(line) and line[index] in " \t":
        index += 1
    if index >= len(line) or line[index] != ")":
        return None, "link title has no outer closing parenthesis"
    return index, None


def _parse_inline_destination(line: str, open_parenthesis: int) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    index = open_parenthesis + 1
    while index < len(line) and line[index] in " \t":
        index += 1
    if index >= len(line):
        return None, None, "link destination is incomplete"

    if line[index] == "<":
        index += 1
        start = index
        while index < len(line):
            if line[index] == "\\":
                index += 2
                continue
            if line[index] == ">":
                destination = line[start:index]
                close_index, error = _consume_title_and_close(line, index + 1)
                return destination, close_index, error
            index += 1
        return None, None, "unterminated angle-bracket link destination"

    start = index
    nested_parentheses = 0
    while index < len(line):
        character = line[index]
        if character == "\\":
            index += 2
            continue
        if character == "(":
            nested_parentheses += 1
        elif character == ")":
            if nested_parentheses:
                nested_parentheses -= 1
            else:
                return line[start:index], index, None
        elif character in " \t" and nested_parentheses == 0:
            destination = line[start:index]
            close_index, error = _consume_title_and_close(line, index)
            return destination, close_index, error
        index += 1

    return None, None, "link destination has no closing parenthesis"


def _supported_inline_links(line: str) -> Tuple[List[Tuple[str, int]], List[Tuple[int, str]]]:
    masked = _mask_inline_code(line)
    links: List[Tuple[str, int]] = []
    unsupported: List[Tuple[int, str]] = []
    index = 0

    while index < len(masked):
        close_bracket = masked.find("](", index)
        if close_bracket < 0:
            break
        if _is_escaped(masked, close_bracket) or not _has_link_label_opener(masked, close_bracket):
            index = close_bracket + 2
            continue

        destination, close_index, error = _parse_inline_destination(line, close_bracket + 1)
        if error is not None or destination is None or close_index is None:
            unsupported.append((close_bracket + 1, error or "unsupported inline link"))
            index = close_bracket + 2
            continue
        links.append((destination, close_bracket + 1))
        index = close_index + 1

    return links, unsupported


def _within_directory(directory: Path, candidate: Path) -> bool:
    try:
        return os.path.commonpath((str(directory), str(candidate))) == str(directory)
    except ValueError:
        return False


def _has_symlink_component(bundle: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(bundle)
    except ValueError:
        return True
    current = bundle
    if current.is_symlink():
        return True
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            return True
    return False


def _validate_link_target(
    root: Path,
    bundle: Path,
    source: Path,
    line_number: int,
    destination: str,
) -> Optional[Finding]:
    raw_target = re.sub(r"\\(.)", r"\1", destination.strip())
    if not raw_target or raw_target.startswith("#"):
        return None
    if raw_target.startswith("//"):
        return None
    if re.match(r"^[A-Za-z]:[\\/]", raw_target):
        return Finding(
            "VIOLATION",
            "AEP-MD-005",
            _display_path(root, source),
            "drive-absolute link is not copy-portable: {!r}".format(destination),
            line_number,
        )
    scheme_match = URI_SCHEME_RE.match(raw_target)
    if scheme_match is not None:
        scheme = raw_target[: raw_target.index(":")]
        if scheme.lower() != "file":
            return None
        return Finding(
            "VIOLATION",
            "AEP-MD-005",
            _display_path(root, source),
            "local file URI is not copy-portable: {!r}".format(destination),
            line_number,
        )
    if raw_target.startswith("/"):
        return Finding(
            "VIOLATION",
            "AEP-MD-005",
            _display_path(root, source),
            "absolute local link is not copy-portable: {!r}".format(destination),
            line_number,
        )

    path_text = raw_target.split("#", 1)[0].split("?", 1)[0]
    try:
        path_text = unquote(path_text)
    except UnicodeError:
        return Finding(
            "UNSUPPORTED",
            "AEP-MD-006",
            _display_path(root, source),
            "link destination cannot be URL-decoded: {!r}".format(destination),
            line_number,
        )
    if not path_text:
        return None
    if "\x00" in path_text:
        return Finding(
            "UNSUPPORTED",
            "AEP-MD-006",
            _display_path(root, source),
            "link destination contains a NUL byte",
            line_number,
        )

    lexical_target = source.parent / path_text
    try:
        resolved_bundle = bundle.resolve(strict=True)
        resolved_target = lexical_target.resolve(strict=False)
    except OSError as error:
        return Finding(
            "ERROR",
            "AEP-TOOL-001",
            _display_path(root, source),
            "cannot resolve link {!r}: {}".format(destination, error),
            line_number,
        )

    if not _within_directory(resolved_bundle, resolved_target):
        return Finding(
            "VIOLATION",
            "AEP-MD-005",
            _display_path(root, source),
            "relative link escapes the reusable bundle: {!r}".format(destination),
            line_number,
        )
    if not resolved_target.exists():
        return Finding(
            "VIOLATION",
            "AEP-MD-005",
            _display_path(root, source),
            "relative link target does not exist: {!r}".format(destination),
            line_number,
        )
    if resolved_target.is_symlink() or not (resolved_target.is_file() or resolved_target.is_dir()):
        return Finding(
            "VIOLATION",
            "AEP-MD-005",
            _display_path(root, source),
            "relative link target is not a regular file or directory: {!r}".format(destination),
            line_number,
        )
    return None


def _scan_protocol_entries(root: Path, protocol: Path) -> Tuple[Set[str], Set[str], List[Finding]]:
    files: Set[str] = set()
    directories: Set[str] = set()
    findings: List[Finding] = []

    if protocol.is_symlink():
        findings.append(Finding("VIOLATION", "AEP-PKG-002", "protocol", "bundle root must not be a symlink"))
        return files, directories, findings
    if not protocol.exists() or not protocol.is_dir():
        findings.append(Finding("VIOLATION", "AEP-PKG-001", "protocol", "bundle directory is missing"))
        return files, directories, findings

    traversal_errors: List[OSError] = []

    def record_traversal_error(error: OSError) -> None:
        traversal_errors.append(error)

    try:
        walker = os.walk(str(protocol), topdown=True, onerror=record_traversal_error, followlinks=False)
        for current, directory_names, file_names in walker:
            current_path = Path(current)
            kept_directories = []
            for name in sorted(directory_names):
                path = current_path / name
                relative = path.relative_to(protocol).as_posix()
                if path.is_symlink():
                    findings.append(Finding("VIOLATION", "AEP-PKG-002", "protocol/" + relative, "symlinks are forbidden in the reusable bundle"))
                    continue
                directories.add(relative)
                kept_directories.append(name)
            directory_names[:] = kept_directories

            for name in sorted(file_names):
                path = current_path / name
                relative = path.relative_to(protocol).as_posix()
                try:
                    mode = path.lstat().st_mode
                except OSError as error:
                    findings.append(Finding("ERROR", "AEP-TOOL-001", "protocol/" + relative, "cannot inspect entry: {}".format(error)))
                    continue
                if stat.S_ISLNK(mode):
                    findings.append(Finding("VIOLATION", "AEP-PKG-002", "protocol/" + relative, "symlinks are forbidden in the reusable bundle"))
                elif stat.S_ISREG(mode):
                    files.add(relative)
                else:
                    findings.append(Finding("VIOLATION", "AEP-PKG-002", "protocol/" + relative, "expected a regular file"))
    except OSError as error:
        findings.append(Finding("ERROR", "AEP-TOOL-001", "protocol", "cannot traverse bundle: {}".format(error)))

    for error in traversal_errors:
        error_path = Path(error.filename) if error.filename else protocol
        findings.append(
            Finding(
                "ERROR",
                "AEP-TOOL-001",
                _display_path(root, error_path),
                "cannot traverse bundle entry: {}".format(error),
            )
        )

    return files, directories, findings


def _validate_manifest(root: Path, protocol: Path) -> List[Finding]:
    files, directories, findings = _scan_protocol_entries(root, protocol)
    expected_files = set(EXPECTED_PROTOCOL_FILES)
    expected_directories = set(EXPECTED_PROTOCOL_DIRECTORIES)

    for missing in sorted(expected_files - files):
        findings.append(Finding("VIOLATION", "AEP-PKG-001", "protocol/" + missing, "required package file is missing"))
    for unexpected in sorted(files - expected_files):
        findings.append(Finding("VIOLATION", "AEP-PKG-001", "protocol/" + unexpected, "unexpected package file"))
    for missing in sorted(expected_directories - directories):
        findings.append(Finding("VIOLATION", "AEP-PKG-001", "protocol/" + missing, "required package directory is missing"))
    for unexpected in sorted(directories - expected_directories):
        findings.append(Finding("VIOLATION", "AEP-PKG-001", "protocol/" + unexpected, "unexpected package directory"))

    return findings


def _validate_markdown_file(root: Path, protocol: Path, path: Path) -> List[Finding]:
    findings: List[Finding] = []
    display = _display_path(root, path)
    try:
        data = path.read_bytes()
    except OSError as error:
        return [Finding("ERROR", "AEP-TOOL-001", display, "cannot read file: {}".format(error))]

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        return [Finding("VIOLATION", "AEP-MD-001", display, "file is not valid UTF-8: {}".format(error))]

    if not data.endswith(b"\n"):
        findings.append(Finding("VIOLATION", "AEP-MD-002", display, "file must end with a newline"))

    lines = text.splitlines()
    fenced_lines, unclosed_fence = _fenced_line_numbers(lines)
    visible_lines = _mask_inline_code_blocks(lines, fenced_lines)

    for line_number, line in enumerate(lines, 1):
        if re.search(r"[ \t]+$", line):
            findings.append(Finding("VIOLATION", "AEP-MD-003", display, "trailing whitespace", line_number))

        index = line_number - 1
        if index in fenced_lines:
            continue

        visible = _strip_blockquote_prefix(visible_lines[index])
        if visible.startswith("    ") or visible.startswith("\t"):
            if "](" in visible or REFERENCE_DEFINITION_RE.match(visible) or REFERENCE_LINK_RE.search(visible):
                findings.append(
                    Finding(
                        "UNSUPPORTED",
                        "AEP-MD-006",
                        display,
                        "link-like syntax on an indented line requires full container parsing",
                        line_number,
                    )
                )
            continue

        if REFERENCE_DEFINITION_RE.match(visible) or REFERENCE_LINK_RE.search(visible):
            findings.append(
                Finding(
                    "UNSUPPORTED",
                    "AEP-MD-006",
                    display,
                    "reference-style links are outside this checker's supported syntax",
                    line_number,
                )
            )

        links, unsupported = _supported_inline_links(visible)
        for _column, message in unsupported:
            findings.append(Finding("UNSUPPORTED", "AEP-MD-006", display, message, line_number))
        for destination, _column in links:
            finding = _validate_link_target(root, protocol, path, line_number, destination)
            if finding is not None:
                findings.append(finding)

    if unclosed_fence is not None:
        fence_character, fence_length, fence_open_line = unclosed_fence
        findings.append(
            Finding(
                "VIOLATION",
                "AEP-MD-004",
                display,
                "unclosed {} fence of length {}".format(fence_character, fence_length),
                fence_open_line,
            )
        )

    return findings


def _section_positions(lines: Sequence[str], fenced_lines: Set[int]) -> List[Tuple[str, int]]:
    positions: List[Tuple[str, int]] = []
    for index, line in enumerate(lines):
        if index in fenced_lines or line.startswith("    ") or line.startswith("\t"):
            continue
        match = TOP_LEVEL_HEADING_RE.match(line)
        if match is not None:
            positions.append((match.group(1), index))
    return positions


def _validate_handoff(root: Path, path: Path) -> List[Finding]:
    display = _display_path(root, path)
    if path.is_symlink():
        return [Finding("VIOLATION", "AEP-HANDOFF-001", display, "HANDOFF must not be a symlink")]
    if not path.exists() or not path.is_file():
        return [Finding("VIOLATION", "AEP-HANDOFF-001", display, "HANDOFF file is missing or not a regular file")]
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return [Finding("VIOLATION", "AEP-MD-001", display, "file is not valid UTF-8: {}".format(error))]
    except OSError as error:
        return [Finding("ERROR", "AEP-TOOL-001", display, "cannot read HANDOFF: {}".format(error))]

    lines = text.splitlines()
    fenced_lines, unclosed_fence = _fenced_line_numbers(lines)
    positions = _section_positions(lines, fenced_lines)
    headings = tuple(name for name, _index in positions)
    findings: List[Finding] = []
    if headings != EXPECTED_HANDOFF_SECTIONS:
        findings.append(
            Finding(
                "VIOLATION",
                "AEP-HANDOFF-001",
                display,
                "top-level sections must be exactly {} in order; found {}".format(
                    ", ".join(EXPECTED_HANDOFF_SECTIONS),
                    ", ".join(headings) if headings else "NONE",
                ),
            )
        )
    if unclosed_fence is not None:
        findings.append(Finding("VIOLATION", "AEP-HANDOFF-001", display, "unclosed fenced block prevents reliable HANDOFF parsing"))

    current_start = next((index for name, index in positions if name == "Current State"), None)
    active_start = next((index for name, index in positions if name == "Active Issues"), None)
    if current_start is not None and active_start is not None and current_start < active_start:
        current_lines = [
            line
            for index, line in enumerate(lines[current_start + 1 : active_start], current_start + 1)
            if index not in fenced_lines and not line.startswith("    ") and not line.startswith("\t")
        ]
        for field in REQUIRED_SNAPSHOT_FIELDS:
            pattern = re.compile(r"^- \*\*" + re.escape(field) + r":\*\*\s*(\S.*)$")
            matches = [line for line in current_lines if pattern.match(line)]
            if len(matches) != 1:
                findings.append(
                    Finding(
                        "VIOLATION",
                        "AEP-HANDOFF-002",
                        display,
                        "snapshot field {!r} must appear exactly once with a nonempty value".format(field),
                    )
                )
    else:
        findings.append(Finding("VIOLATION", "AEP-HANDOFF-002", display, "snapshot fields cannot be located without ordered Current State and Active Issues sections"))

    next_positions = [index for name, index in positions if name == "Next Action"]
    if len(next_positions) == 1:
        start = next_positions[0] + 1
        end = next((index for _name, index in positions if index > next_positions[0]), len(lines))
        body = [
            line.strip()
            for index, line in enumerate(lines[start:end], start)
            if index not in fenced_lines and line.strip()
        ]
        if not body:
            findings.append(Finding("VIOLATION", "AEP-HANDOFF-003", display, "Next Action must be nonempty"))
    else:
        findings.append(Finding("VIOLATION", "AEP-HANDOFF-003", display, "Next Action heading must appear exactly once"))

    return findings


def validate_repository(root: Path) -> List[Finding]:
    findings: List[Finding] = []
    protocol = root / "protocol"
    findings.extend(_validate_manifest(root, protocol))

    protocol_is_safe_directory = protocol.exists() and protocol.is_dir() and not protocol.is_symlink()
    if protocol_is_safe_directory:
        for relative in EXPECTED_PROTOCOL_FILES:
            path = protocol / relative
            if (
                path.exists()
                and path.is_file()
                and not _has_symlink_component(protocol, path)
            ):
                findings.extend(_validate_markdown_file(root, protocol, path))

    findings.extend(_validate_handoff(root, root / "HANDOFF.md"))
    if protocol_is_safe_directory and not _has_symlink_component(protocol, protocol / "HANDOFF.md"):
        findings.extend(_validate_handoff(root, protocol / "HANDOFF.md"))
    return sorted(set(findings), key=Finding.sort_key)


def _build_parser() -> argparse.ArgumentParser:
    parser = StableArgumentParser(description="Validate stable structural invariants of the protocol source bundle.")
    parser.add_argument(
        "--root",
        default=None,
        help="repository root to inspect (default: parent of this script)",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)
    candidate = Path(arguments.root) if arguments.root is not None else Path(__file__).resolve().parent.parent
    try:
        root = candidate.resolve(strict=True)
    except OSError as error:
        print("ERROR AEP-TOOL-001 {}: repository root cannot be resolved: {}".format(candidate, error))
        print("SUMMARY violations=0 unsupported=0 errors=1")
        return 2
    if not root.is_dir():
        print("ERROR AEP-TOOL-001 {}: repository root is not a directory".format(root))
        print("SUMMARY violations=0 unsupported=0 errors=1")
        return 2

    try:
        findings = validate_repository(root)
    except Exception as error:  # Defensive boundary: never turn an evaluator failure into a pass.
        print("ERROR AEP-TOOL-001 .: unexpected checker failure: {}: {}".format(type(error).__name__, error))
        print("SUMMARY violations=0 unsupported=0 errors=1")
        return 2

    if not findings:
        print("PASS structural protocol validation (package_files=10 handoffs=2)")
        return 0

    for finding in findings:
        print(finding.render())
    violations = sum(finding.kind == "VIOLATION" for finding in findings)
    unsupported = sum(finding.kind == "UNSUPPORTED" for finding in findings)
    errors = sum(finding.kind == "ERROR" for finding in findings)
    print("SUMMARY violations={} unsupported={} errors={}".format(violations, unsupported, errors))
    return 2 if unsupported or errors else 1


if __name__ == "__main__":
    sys.exit(main())
