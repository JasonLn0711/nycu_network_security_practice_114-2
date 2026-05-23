#!/usr/bin/env python3
from pathlib import Path
import subprocess
import json
import re
import time


SHARED = Path("/shared")

TARGET_CANDIDATES = [
    SHARED / "blogic.copy",
    SHARED / "blogic",
]

OUT_JSON = SHARED / "target_info.json"
OUT_LOG = SHARED / "target_analysis.log"


def run_cmd(args, timeout=5):
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }


def find_target_binary():
    for path in TARGET_CANDIDATES:
        if path.exists():
            return path
    return None


def parse_file_output(text):
    info = {
        "bits": "unknown",
        "architecture": "unknown",
        "endianness": "unknown",
        "stripped": "unknown",
        "raw": text.strip(),
    }

    if "ELF 64-bit" in text:
        info["bits"] = 64
    elif "ELF 32-bit" in text:
        info["bits"] = 32

    if "x86-64" in text or "x86_64" in text:
        info["architecture"] = "x86_64"
    elif "Intel 80386" in text:
        info["architecture"] = "x86"

    if "LSB" in text:
        info["endianness"] = "little"
    elif "MSB" in text:
        info["endianness"] = "big"

    if "not stripped" in text:
        info["stripped"] = False
    elif "stripped" in text:
        info["stripped"] = True

    return info


def parse_elf_type(readelf_h):
    match = re.search(r"Type:\s+(\S+)", readelf_h)
    elf_type = match.group(1) if match else "unknown"

    if elf_type == "EXEC":
        return {
            "elf_type": elf_type,
            "pie": False,
            "explanation": "ELF type is EXEC, so this is usually a non-PIE executable with fixed code addresses.",
        }

    if elf_type == "DYN":
        return {
            "elf_type": elf_type,
            "pie": True,
            "explanation": "ELF type is DYN, so this is likely PIE or a shared object.",
        }

    return {
        "elf_type": elf_type,
        "pie": "unknown",
        "explanation": "Could not determine PIE status from ELF type.",
    }


def parse_nx_status(readelf_l):
    result = {
        "nx_enabled": "unknown",
        "gnu_stack": "not_found",
        "explanation": "Could not find GNU_STACK program header.",
    }

    for line in readelf_l.splitlines():
        if "GNU_STACK" not in line:
            continue

        result["gnu_stack"] = line.strip()
        parts = line.split()
        flags = ""

        for part in parts:
            if set(part).issubset(set("RWE")) and "R" in part:
                flags = part

        if "E" in flags:
            result["nx_enabled"] = False
            result["explanation"] = "GNU_STACK contains E permission, so stack appears executable."
        elif "R" in flags and "E" not in flags:
            result["nx_enabled"] = True
            result["explanation"] = "GNU_STACK does not contain E permission, so NX stack protection appears enabled."
        else:
            result["nx_enabled"] = "unknown"
            result["explanation"] = "GNU_STACK found, but permission flags could not be parsed."

    return result


def parse_symbol_table(readelf_s):
    symbols = []

    for line in readelf_s.splitlines():
        parts = line.split()

        if len(parts) < 8:
            continue

        try:
            index = parts[0].rstrip(":")
            value = int(parts[1], 16)
            size = int(parts[2])
            sym_type = parts[3]
            bind = parts[4]
            visibility = parts[5]
            ndx = parts[6]
            name = " ".join(parts[7:])
        except Exception:
            continue

        symbols.append({
            "index": index,
            "address": value,
            "address_hex": hex(value),
            "size": size,
            "type": sym_type,
            "bind": bind,
            "visibility": visibility,
            "ndx": ndx,
            "name": name,
        })

    return symbols


def extract_interesting_symbols(parsed_symbols):
    keywords = [
        "main",
        "task",
        "maintenance",
        "exec",
        "execute",
        "system",
        "backdoor",
        "config",
        "input",
        "read",
        "strcpy",
        "strncpy",
        "gets",
        "sprintf",
        "scanf",
        "memcpy",
    ]

    interesting = []

    for sym in parsed_symbols:
        lower = sym["name"].lower()
        if any(keyword in lower for keyword in keywords):
            interesting.append(
                f'{sym["index"]}: {sym["address_hex"]} {sym["size"]} '
                f'{sym["type"]} {sym["bind"]} {sym["visibility"]} '
                f'{sym["ndx"]} {sym["name"]}'
            )

    return interesting[:100]


def extract_interesting_strings(strings_output):
    keywords = [
        "backdoor",
        "user_input",
        "config",
        "task",
        "maintenance",
        "exec",
        "system",
        "shared",
        "exploit_done",
        ".data",
        "/",
    ]

    found = []

    for line in strings_output.splitlines():
        lower = line.lower()
        if any(keyword in lower for keyword in keywords):
            found.append(line)

    return found[:100]


def extract_imported_functions(parsed_symbols):
    risky_keywords = [
        "gets",
        "strcpy",
        "strcat",
        "sprintf",
        "scanf",
        "memcpy",
        "system",
        "exec",
        "popen",
    ]

    imports = []

    for sym in parsed_symbols:
        lower = sym["name"].lower()

        if sym["ndx"] == "UND" and any(keyword in lower for keyword in risky_keywords):
            imports.append(
                f'{sym["index"]}: {sym["address_hex"]} {sym["size"]} '
                f'{sym["type"]} {sym["bind"]} {sym["visibility"]} '
                f'{sym["ndx"]} {sym["name"]}'
            )

    return imports[:100]


def discover_targets(parsed_symbols):
    discovered = {}

    for sym in parsed_symbols:
        name = sym["name"]
        lower = name.lower()

        if "execute_task" in lower:
            discovered["execute_task"] = {
                "address": sym["address_hex"],
                "address_int": sym["address"],
                "symbol": name,
                "type": sym["type"],
                "size": sym["size"],
                "reason": "symbol name contains execute_task",
            }

        elif "parse_config" in lower:
            discovered["parse_config"] = {
                "address": sym["address_hex"],
                "address_int": sym["address"],
                "symbol": name,
                "type": sym["type"],
                "size": sym["size"],
                "reason": "symbol name contains parse_config",
            }

        elif "maintenance" in lower:
            discovered["maintenance_task"] = {
                "address": sym["address_hex"],
                "address_int": sym["address"],
                "symbol": name,
                "type": sym["type"],
                "size": sym["size"],
                "reason": "symbol name contains maintenance",
            }

        elif name == "user_input":
            discovered["user_input"] = {
                "address": sym["address_hex"],
                "address_int": sym["address"],
                "symbol": name,
                "type": sym["type"],
                "size": sym["size"],
                "reason": "global object named user_input",
            }

        elif name == "user_input_len":
            discovered["user_input_len"] = {
                "address": sym["address_hex"],
                "address_int": sym["address"],
                "symbol": name,
                "type": sym["type"],
                "size": sym["size"],
                "reason": "global object named user_input_len",
            }

        elif name == "main":
            discovered["main"] = {
                "address": sym["address_hex"],
                "address_int": sym["address"],
                "symbol": name,
                "type": sym["type"],
                "size": sym["size"],
                "reason": "program entry logic symbol",
            }

    return discovered


def parse_objdump_ret_gadgets(objdump_d):
    gadgets = []

    for line in objdump_d.splitlines():
        line = line.strip()

        if not line:
            continue

        if not re.match(r"^[0-9a-fA-F]+:", line):
            continue

        if not re.search(r"\bret[q]?\b", line):
            continue

        try:
            addr_text = line.split(":", 1)[0]
            addr = int(addr_text, 16)
        except Exception:
            continue

        gadgets.append({
            "address": hex(addr),
            "address_int": addr,
            "instruction": line,
            "type": "ret",
        })

    return gadgets


def choose_preferred_ret_gadget(ret_gadgets, discovered_targets):
    execute_task = discovered_targets.get("execute_task", {})
    execute_task_addr = execute_task.get("address_int")

    if not ret_gadgets:
        return None

    if execute_task_addr is None:
        return ret_gadgets[0]

    before_execute_task = [
        g for g in ret_gadgets
        if g["address_int"] < execute_task_addr
    ]

    if before_execute_task:
        return max(before_execute_task, key=lambda g: g["address_int"])

    return ret_gadgets[0]


def parse_objdump_lines(objdump_d):
    parsed = []

    for raw in objdump_d.splitlines():
        line = raw.strip()
        match = re.match(r"^([0-9a-fA-F]+):\s*(.*)$", line)
        if not match:
            continue

        try:
            addr = int(match.group(1), 16)
        except Exception:
            continue

        parsed.append({
            "address": addr,
            "address_hex": hex(addr),
            "line": line,
        })

    return parsed


def extract_function_disassembly(objdump_d, start_addr, size):
    lines = parse_objdump_lines(objdump_d)

    if start_addr is None:
        return []

    if size and size > 0:
        end_addr = start_addr + size
        selected = [
            item for item in lines
            if start_addr <= item["address"] < end_addr
        ]
    else:
        selected = [
            item for item in lines
            if item["address"] >= start_addr
        ]

    return selected[:300]


def extract_rbp_displacements(function_lines):
    candidates = []

    for item in function_lines:
        line = item["line"]

        for match in re.finditer(r"-0x([0-9a-fA-F]+)\(%rbp\)", line):
            displacement = int(match.group(1), 16)

            candidates.append({
                "address": item["address_hex"],
                "line": line,
                "displacement": displacement,
                "displacement_hex": hex(displacement),
            })

    return candidates


def function_contains_call(function_lines, keyword):
    keyword = keyword.lower()

    for item in function_lines:
        line = item["line"].lower()
        if "call" in line and keyword in line:
            return True

    return False


def find_memcpy_destination_buffer(function_lines):
    """
    Infer memcpy destination buffer.

    System V x86_64:
      arg1 -> rdi

    Common pattern:
      lea -0x60(%rbp), %rax
      mov %rax, %rdi
      call memcpy@plt

    This function searches backward from memcpy call.
    """

    memcpy_indices = [
        i for i, item in enumerate(function_lines)
        if "call" in item["line"].lower() and "memcpy" in item["line"].lower()
    ]

    for idx in memcpy_indices:
        start = max(0, idx - 16)
        window = function_lines[start:idx + 1]

        reg_defs = {}

        for item in window:
            line = item["line"]

            # lea -0x60(%rbp),%rax
            m = re.search(r"lea\s+-0x([0-9a-fA-F]+)\(%rbp\),%([a-z0-9]+)", line)
            if m:
                displacement = int(m.group(1), 16)
                reg = "%" + m.group(2)
                reg_defs[reg] = {
                    "address": item["address_hex"],
                    "line": line,
                    "displacement": displacement,
                    "displacement_hex": hex(displacement),
                    "register": reg,
                    "reason": "rbp-relative lea near memcpy",
                    "memcpy_call": function_lines[idx]["line"],
                }

            # mov %rax,%rdi
            m = re.search(r"mov\s+(%[a-z0-9]+),%rdi", line)
            if m:
                src = m.group(1)
                if src in reg_defs:
                    ev = dict(reg_defs[src])
                    ev["reason"] = "rbp-relative address moved into rdi before memcpy"
                    ev["rdi_assignment"] = line
                    return ev

            # lea -0x60(%rbp),%rdi
            m = re.search(r"lea\s+-0x([0-9a-fA-F]+)\(%rbp\),%rdi", line)
            if m:
                displacement = int(m.group(1), 16)
                return {
                    "address": item["address_hex"],
                    "line": line,
                    "displacement": displacement,
                    "displacement_hex": hex(displacement),
                    "register": "%rdi",
                    "reason": "direct rbp-relative lea into rdi before memcpy",
                    "memcpy_call": function_lines[idx]["line"],
                }

        # fallback within this memcpy window:
        rbp_lea_candidates = []
        for item in reversed(window):
            line = item["line"]
            m = re.search(r"lea\s+-0x([0-9a-fA-F]+)\(%rbp\),%([a-z0-9]+)", line)
            if m:
                rbp_lea_candidates.append({
                    "address": item["address_hex"],
                    "line": line,
                    "displacement": int(m.group(1), 16),
                    "displacement_hex": hex(int(m.group(1), 16)),
                    "register": "%" + m.group(2),
                    "reason": "fallback rbp-relative lea near memcpy",
                    "memcpy_call": function_lines[idx]["line"],
                })

        # In maintenance_task, choose the most plausible local destination.
        # This should usually be rbp-0x60, producing 0x68.
        if rbp_lea_candidates:
            plausible = [
                c for c in rbp_lea_candidates
                if 0x20 <= c["displacement"] <= 0x200
            ]
            if plausible:
                return max(plausible, key=lambda c: c["displacement"])
            return max(rbp_lea_candidates, key=lambda c: c["displacement"])

    return None


def infer_offset_to_ret(discovered_targets, objdump_d):
    """
    Corrected offset inference:
    - Prefer maintenance_task.
    - Find memcpy destination local buffer.
    - Estimate saved RIP offset = buffer displacement + 8.
    - Avoid parse_config largest-stack-object false positives.
    """

    analysis_order = []

    if "maintenance_task" in discovered_targets:
        analysis_order.append(("maintenance_task", discovered_targets["maintenance_task"]))

    if "parse_config" in discovered_targets:
        analysis_order.append(("parse_config", discovered_targets["parse_config"]))

    if not analysis_order:
        return {
            "ok": False,
            "offset_to_ret": None,
            "source": "static_disassembly_inference",
            "confidence": "none",
            "reason": "neither maintenance_task nor parse_config symbol was discovered",
        }

    attempts = []

    for function_name, target in analysis_order:
        start_addr = target.get("address_int")
        size = target.get("size", 0)

        function_lines = extract_function_disassembly(
            objdump_d=objdump_d,
            start_addr=start_addr,
            size=size,
        )

        rbp_candidates = extract_rbp_displacements(function_lines)
        contains_memcpy = function_contains_call(function_lines, "memcpy")
        memcpy_dest = find_memcpy_destination_buffer(function_lines)

        attempt = {
            "function": function_name,
            "symbol": target.get("symbol"),
            "address": target.get("address"),
            "size": size,
            "contains_memcpy": contains_memcpy,
            "memcpy_destination_candidate": memcpy_dest,
            "rbp_candidates_sample": rbp_candidates[:40],
            "function_disassembly_sample": [x["line"] for x in function_lines[:120]],
        }

        attempts.append(attempt)

        if function_name == "maintenance_task" and memcpy_dest:
            local_buffer_displacement = memcpy_dest["displacement"]
            offset_to_ret = local_buffer_displacement + 8

            return {
                "ok": True,
                "offset_to_ret": offset_to_ret,
                "offset_hex": hex(offset_to_ret),
                "local_buffer_displacement": local_buffer_displacement,
                "local_buffer_displacement_hex": hex(local_buffer_displacement),
                "saved_rbp_size": 8,
                "source": "static_disassembly_inference",
                "confidence": "high",
                "reason": (
                    "selected memcpy destination buffer in maintenance_task; "
                    f"saved return address offset estimated as "
                    f"{hex(local_buffer_displacement)} + 8 = {hex(offset_to_ret)}"
                ),
                "selected_function": function_name,
                "selected_evidence": memcpy_dest,
                "attempts": attempts,
            }

    return {
        "ok": False,
        "offset_to_ret": None,
        "source": "static_disassembly_inference",
        "confidence": "none",
        "reason": (
            "could not identify memcpy destination buffer in maintenance_task; "
            "refusing to infer offset from parse_config largest stack object"
        ),
        "attempts": attempts,
    }


def calculate_risk_score(report):
    score = 0
    reasons = []

    pie = report.get("pie_info", {}).get("pie")
    nx = report.get("nx_info", {}).get("nx_enabled")
    symbols = "\n".join(report.get("interesting_symbols", [])).lower()
    strings = "\n".join(report.get("interesting_strings", [])).lower()
    imports = "\n".join(report.get("imported_risky_functions", [])).lower()
    discovered = report.get("discovered_targets", {})
    gadgets = report.get("discovered_gadgets", {})
    offset_inference = report.get("offset_inference", {})

    if pie is False:
        score += 2
        reasons.append("non-PIE executable: code addresses are likely fixed")

    if nx is False:
        score += 2
        reasons.append("executable stack: stack-based code execution may be easier")

    if "user_input" in strings:
        score += 2
        reasons.append("binary contains user_input string")

    if "config" in strings:
        score += 1
        reasons.append("binary contains config-related string")

    if "task" in symbols or "execute" in symbols or "exec" in symbols:
        score += 2
        reasons.append("binary contains task/execute-related symbol")

    if imports:
        score += 2
        reasons.append("binary imports potentially risky library functions")

    if "execute_task" in discovered:
        score += 1
        reasons.append("agent discovered a candidate task execution function")

    if "maintenance_task" in discovered:
        score += 1
        reasons.append("agent discovered a candidate vulnerable maintenance function")

    if gadgets.get("preferred_ret"):
        score += 1
        reasons.append("agent discovered a usable ret gadget")

    if offset_inference.get("ok"):
        score += 1
        reasons.append("agent inferred a candidate return-address offset")

    return {
        "score": min(score, 10),
        "reasons": reasons,
    }


def main():
    log = []
    report = {
        "timestamp": int(time.time()),
        "stage": "level_5c_corrected_static_offset_inference",
        "target_path": None,
        "target_exists": False,
    }

    log.append("[*] Level 5C corrected static offset inference analysis started")

    target = find_target_binary()

    if target is None:
        log.append("[-] No target binary found.")
        log.append("[-] Checked /shared/blogic.copy and /shared/blogic.")

        OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
        OUT_LOG.write_text("\n".join(log) + "\n", encoding="utf-8")

        print("[-] target binary not found")
        return

    report["target_path"] = str(target)
    report["target_exists"] = True

    log.append(f"[*] Target binary found: {target}")

    file_result = run_cmd(["file", str(target)])
    readelf_h = run_cmd(["readelf", "-h", str(target)])
    readelf_l = run_cmd(["readelf", "-W", "-l", str(target)])
    readelf_s = run_cmd(["readelf", "-s", str(target)])
    strings_result = run_cmd(["strings", "-a", str(target)])
    objdump_d = run_cmd(["objdump", "-d", str(target)], timeout=10)

    parsed_symbols = parse_symbol_table(readelf_s["stdout"])

    report["file_info"] = parse_file_output(file_result["stdout"])
    report["pie_info"] = parse_elf_type(readelf_h["stdout"])
    report["nx_info"] = parse_nx_status(readelf_l["stdout"])
    report["parsed_symbol_count"] = len(parsed_symbols)
    report["interesting_symbols"] = extract_interesting_symbols(parsed_symbols)
    report["interesting_strings"] = extract_interesting_strings(strings_result["stdout"])
    report["imported_risky_functions"] = extract_imported_functions(parsed_symbols)
    report["discovered_targets"] = discover_targets(parsed_symbols)

    ret_gadgets = parse_objdump_ret_gadgets(objdump_d["stdout"])
    preferred_ret = choose_preferred_ret_gadget(
        ret_gadgets,
        report["discovered_targets"],
    )

    report["discovered_gadgets"] = {
        "ret_gadgets_count": len(ret_gadgets),
        "preferred_ret": preferred_ret,
        "ret_gadgets_sample": ret_gadgets[:30],
    }

    report["offset_inference"] = infer_offset_to_ret(
        discovered_targets=report["discovered_targets"],
        objdump_d=objdump_d["stdout"],
    )

    report["risk_assessment"] = calculate_risk_score(report)
    report["all_parsed_symbols_sample"] = parsed_symbols[:120]

    log.append("")
    log.append("[*] File info")
    log.append(json.dumps(report["file_info"], indent=2))

    log.append("")
    log.append("[*] PIE info")
    log.append(json.dumps(report["pie_info"], indent=2))

    log.append("")
    log.append("[*] NX info")
    log.append(json.dumps(report["nx_info"], indent=2))

    log.append("")
    log.append("[*] Interesting symbols")
    if report["interesting_symbols"]:
        log.extend(report["interesting_symbols"])
    else:
        log.append("(none found)")

    log.append("")
    log.append("[*] Interesting strings")
    if report["interesting_strings"]:
        log.extend(report["interesting_strings"])
    else:
        log.append("(none found)")

    log.append("")
    log.append("[*] Imported risky functions")
    if report["imported_risky_functions"]:
        log.extend(report["imported_risky_functions"])
    else:
        log.append("(none found)")

    log.append("")
    log.append("[*] Discovered targets")
    if report["discovered_targets"]:
        log.append(json.dumps(report["discovered_targets"], indent=2))
    else:
        log.append("(none found)")

    log.append("")
    log.append("[*] Discovered gadgets")
    log.append(json.dumps(report["discovered_gadgets"], indent=2))

    log.append("")
    log.append("[*] Offset inference")
    log.append(json.dumps(report["offset_inference"], indent=2))

    log.append("")
    log.append("[*] Risk assessment")
    log.append(json.dumps(report["risk_assessment"], indent=2))

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_LOG.write_text("\n".join(log) + "\n", encoding="utf-8")

    print("[*] Level 5C corrected target analysis complete")
    print(f"[*] Report written to {OUT_JSON}")
    print(f"[*] Log written to {OUT_LOG}")


if __name__ == "__main__":
    main()