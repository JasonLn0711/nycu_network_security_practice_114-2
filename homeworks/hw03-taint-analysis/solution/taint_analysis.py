from triton import *
import lief

# ============================================================
# Configuration
# ============================================================
BASE_PLT   = 0x10000000
BASE_STACK = 0x9fffffff

def hook_libc_start_main(ctx):
    """Sets up the call to main()."""
    main = ctx.getConcreteRegisterValue(ctx.registers.rdi)
    ctx.setConcreteRegisterValue(
        ctx.registers.rsp,
        ctx.getConcreteRegisterValue(ctx.registers.rsp) - CPUSIZE.QWORD
    )
    ret2main = MemoryAccess(
        ctx.getConcreteRegisterValue(ctx.registers.rsp), CPUSIZE.QWORD
    )
    ctx.setConcreteMemoryValue(ret2main, main)
    ctx.concretizeRegister(ctx.registers.rdi)
    ctx.concretizeRegister(ctx.registers.rsi)
    return 0

def hook_memset(ctx):
    """Simulates memset: fills memory with a constant value and untaints it."""
    dest = ctx.getConcreteRegisterValue(ctx.registers.rdi)
    val  = ctx.getConcreteRegisterValue(ctx.registers.rsi)
    size = ctx.getConcreteRegisterValue(ctx.registers.rdx)
    for i in range(size):
        ctx.setConcreteMemoryValue(dest + i, val & 0xFF)
        ctx.untaintMemory(dest + i)
    return dest

def hook_strncpy(ctx):
    # ===== TODO 1: Implement strncpy with taint propagation (15 pts) =====
    #
    # Implement strncpy(dest, src, n) and propagate taint from src to dest.
    # Refer to: hook_memset above for how to read arguments and access memory.
    # Think about: when copying a byte, should its taint status also be copied?
    #
    # Triton APIs you may need:
    #   ctx.getConcreteRegisterValue, ctx.getConcreteMemoryValue,
    #   ctx.setConcreteMemoryValue, ctx.isMemoryTainted,
    #   ctx.taintMemory, ctx.untaintMemory
    #
    # =============================================================
    pass

def hook_printf(ctx):
    """Simulates printf (simplified)."""
    return 0

# ============================================================
# Hook Table & Binary Loading (infrastructure — no changes needed)
# ============================================================
customRelocation = [
    ['__libc_start_main', hook_libc_start_main, BASE_PLT + 0],
    ['memset',            hook_memset,           BASE_PLT + 1],
    ['strncpy',           hook_strncpy,          BASE_PLT + 2],
    ['printf',            hook_printf,           BASE_PLT + 3],
]

def loadBinary(ctx, binary):
    """Loads binary segments into Triton's virtual memory."""
    for phdr in binary.segments:
        ctx.setConcreteMemoryAreaValue(phdr.virtual_address, list(phdr.content))

def makeRelocation(ctx, binary):
    """Redirects PLT/GOT entries to our Python hooks."""
    try:
        for rel in binary.pltgot_relocations:
            for crel in customRelocation:
                if rel.symbol.name == crel[0]:
                    ctx.setConcreteMemoryValue(
                        MemoryAccess(rel.address, CPUSIZE.QWORD), crel[2]
                    )
    except Exception:
        pass
    try:
        for rel in binary.dynamic_relocations:
            for crel in customRelocation:
                if rel.symbol.name == crel[0]:
                    ctx.setConcreteMemoryValue(
                        MemoryAccess(rel.address, CPUSIZE.QWORD), crel[2]
                    )
    except Exception:
        pass

def hookingHandler(ctx):
    """Checks if the current instruction is a hooked function and calls it."""
    pc = ctx.getConcreteRegisterValue(ctx.registers.rip)
    for rel in customRelocation:
        if rel[2] == pc:
            ret_value = rel[1](ctx)
            if ret_value is not None:
                ctx.setConcreteRegisterValue(ctx.registers.rax, ret_value)
            ret_addr = ctx.getConcreteMemoryValue(
                MemoryAccess(
                    ctx.getConcreteRegisterValue(ctx.registers.rsp),
                    CPUSIZE.QWORD
                )
            )
            ctx.setConcreteRegisterValue(ctx.registers.rip, ret_addr)
            ctx.setConcreteRegisterValue(
                ctx.registers.rsp,
                ctx.getConcreteRegisterValue(ctx.registers.rsp) + CPUSIZE.QWORD
            )

# ============================================================
# Emulation & Taint Tracking
# ============================================================

def emulate(ctx, pc, source_addr, sink_addr, track_length):

    # ===== TODO 2: Mark taint source (10 pts) =====
    # Mark 'track_length' bytes starting from 'source_addr' as tainted.
    # ==============================================

    count = 0
    while pc:
        opcodes = ctx.getConcreteMemoryAreaValue(pc, 16)
        inst = Instruction(pc, opcodes)

        err = ctx.processing(inst)
        if err != 0:
            if list(opcodes[:4]) == [0xF3, 0x0F, 0x1E, 0xFA]:
                ctx.setConcreteRegisterValue(ctx.registers.rip, pc + 4)
                pc = pc + 4
                count += 1
                continue
            break

        hookingHandler(ctx)
        pc = ctx.getConcreteRegisterValue(ctx.registers.rip)
        count += 1
        if count > 50000:
            break

    # ===== TODO 3: Check taint sink (15 pts) =====
    # Check 'track_length' bytes starting from 'sink_addr'.
    # Print whether each byte is [TAINTED] or [CLEAN],
    # and print the total count of tainted bytes.

    # =============================================

# ============================================================
# Main
# ============================================================

def main():
    ctx = TritonContext(ARCH.X86_64)
    ctx.setMode(MODE.ALIGNED_MEMORY, True)
    ctx.setAstRepresentationMode(AST_REPRESENTATION.PYTHON)

    binary = lief.parse('./vuln')
    loadBinary(ctx, binary)
    makeRelocation(ctx, binary)

    ctx.setConcreteRegisterValue(ctx.registers.rbp, BASE_STACK)
    ctx.setConcreteRegisterValue(ctx.registers.rsp, BASE_STACK)

    SOURCE_ADDR = binary.get_symbol('user_input').value
    SINK_ADDR   = binary.get_symbol('output_buf').value
    TRACK_LEN   = 16

    print("=" * 50)
    print("  TAINT ANALYSIS WITH TRITON")
    print("=" * 50)
    print(f"  Source: user_input @ 0x{SOURCE_ADDR:x}")
    print(f"  Sink:   output_buf @ 0x{SINK_ADDR:x}")
    print(f"  Track length: {TRACK_LEN} bytes")
    print("=" * 50)
    print()

    emulate(ctx, binary.entrypoint, SOURCE_ADDR, SINK_ADDR, TRACK_LEN)

    print("\nDone.")

if __name__ == '__main__':
    main()
