import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock


async def apb_idle_cycles(dut, cycles: int):
    """Keep APB idle for N cycles."""
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0
    for _ in range(cycles):
        await RisingEdge(dut.pclk)


async def apb_write(dut, addr: int, data: int):
    """Perform a single APB write transaction."""
    
    # Setup phase
    dut.psel.value = 1
    dut.pwrite.value = 1
    dut.penable.value = 0
    dut.paddr.value = addr
    dut.pwdata.value = data
    await RisingEdge(dut.pclk)

    # Enable phase
    dut.penable.value = 1
    await RisingEdge(dut.pclk)

    # Idle phase
    dut.psel.value = 0
    dut.penable.value = 0
    await RisingEdge(dut.pclk)


@cocotb.test()
async def test_secret_toggle(dut):

    cocotb.start_soon(Clock(dut.pclk, 10, unit="ns").start())

    # Reset
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0
    dut.paddr.value = 0
    dut.pwdata.value = 0

    dut.presetn.value = 0
    await RisingEdge(dut.pclk)
    await RisingEdge(dut.pclk)
    dut.presetn.value = 1
    await RisingEdge(dut.pclk)

    try:
        initial_pin = int(dut.secret_pin.value)
    except:
        initial_pin = 0

    # --- Write 0x55 ---
    await apb_write(dut, 0x0, 0x55)
    await apb_idle_cycles(dut, 3)

    # --- Write 0xAA ---
    await apb_write(dut, 0x0, 0xAA)
    await apb_idle_cycles(dut, 3)

    # --- Write 0x5A ---
    await apb_write(dut, 0x0, 0x5A)
    await apb_idle_cycles(dut, 2)

    final_pin = int(dut.secret_pin.value)

    assert final_pin != initial_pin, \
        f"Secret pin must toggle! initial={initial_pin}, final={final_pin}"


# ✅ CRITICAL: Pytest wrapper function for HUD
def test_apb_gpio_toggle_hidden_runner():
    import os
    from pathlib import Path
    from cocotb_tools.runner import get_runner
    
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    
    sources = [proj_path / "sources/apb_gpio_with_secret_toggle.sv"]
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="apb_gpio_with_secret_toggle",
        always=True,
    )
    runner.test(
        hdl_toplevel="apb_gpio_with_secret_toggle",
        test_module="test_apb_gpio_toggle_hidden"
    )

