import os
import warnings
import cocotb_test.simulator
import pytest

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.mark.parametrize("toplevel_lang", ["verilog"])
def test_reference_rtl(toplevel_lang):

    sim_build = os.path.join("sim_build", "grade_rtl_build")

    cocotb_test.simulator.run(
        verilog_sources=[
            "./rtl/apb_gpio_with_secret_toggle.sv",  # <-- RTL implementation file
        ],
        toplevel="apb_gpio_with_secret_toggle",     # <-- from spec
        module="apb_gpio_toggle_test_hidden",       # <-- hidden test file
        toplevel_lang=toplevel_lang,
        sim="icarus",
        sim_build=sim_build,
    )
