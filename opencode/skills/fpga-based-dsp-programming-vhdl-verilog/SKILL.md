---
name: fpga-based-dsp-programming-vhdl-verilog
description: >-
  Use this skill when the user is working on or asking about FPGA DSP, VHDL, Verilog, hardware audio processing, zero-latency FPGA effects, or implementing DSP algorithms in FPGA fabric.
version: 1.0.0
---

# SKILL: FPGA-Based DSP Programming (VHDL/Verilog)

## CAPABILITIES
- Design custom digital signal processing pipelines on FPGAs
- Implement zero-latency audio effects and synthesizers
- Optimize resource utilization for specific FPGA targets
- Create hardware-accelerated audio interfaces
- Develop testbenches for functional verification

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| DSP algorithm specifications (mathematical equations) | VHDL/Verilog RTL code |
| Target FPGA device specifications | Resource utilization report (LUTs, FFs, DSP slices) |
| Audio interface requirements (sample rate, bit depth) | Pin constraints file (.xdc/.sdc) |
| Test signals and expected outputs | Simulation waveforms and verification reports |
| Clock frequency and latency requirements | Timing analysis report (setup/hold slack) |

## IMPLEMENTATION PATTERN

```vhdl
-- FIR Filter Implementation for Audio Processing
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity audio_fir_filter is
    Generic (
        DATA_WIDTH      : integer := 24;  -- Audio bit depth
        COEFF_WIDTH     : integer := 18;  -- Coefficient bit depth
        TAP_COUNT       : integer := 64   -- Number of filter taps
    );
    Port (
        clk             : in  std_logic;
        reset_n         : in  std_logic;
        audio_in        : in  signed(DATA_WIDTH-1 downto 0);
        audio_out       : out signed(DATA_WIDTH-1 downto 0);
        coeff_update    : in  std_logic;
        new_coeff       : in  signed_array(0 to TAP_COUNT-1)(COEFF_WIDTH-1 downto 0);
        valid_in        : in  std_logic;
        valid_out       : out std_logic
    );
end audio_fir_filter;

architecture rtl of audio_fir_filter is
    type coeff_array is array (0 to TAP_COUNT-1) of signed(COEFF_WIDTH-1 downto 0);
    type delay_line is array (0 to TAP_COUNT-1) of signed(DATA_WIDTH-1 downto 0);
    
    signal coeff_reg    : coeff_array := (others => (others => '0'));
    signal delay_line_reg: delay_line := (others => (others => '0'));
    signal acc_reg      : signed(DATA_WIDTH+COEFF_WIDTH+5 downto 0) := (others => '0');
    signal valid_pipe   : std_logic_vector(0 to TAP_COUNT) := (others => '0');
    
begin
    -- Coefficient update register
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            coeff_reg <= (others => (others => '0'));
        elsif rising_edge(clk) then
            if coeff_update = '1' then
                coeff_reg <= new_coeff;
            end if;
        end if;
    end process;
    
    -- Delay line and MAC operation
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            delay_line_reg <= (others => (others => '0'));
            acc_reg <= (others => '0');
            valid_pipe <= (others => '0');
        elsif rising_edge(clk) then
            if valid_in = '1' then
                -- Shift delay line
                delay_line_reg(TAP_COUNT-1 downto 1) <= delay_line_reg(TAP_COUNT-2 downto 0);
                delay_line_reg(0) <= audio_in;
                
                -- Multiply-Accumulate
                acc_reg <= resize(audio_in * coeff_reg(0), acc_reg'length);
                for i in 1 to TAP_COUNT-1 loop
                    acc_reg <= acc_reg + resize(delay_line_reg(i) * coeff_reg(i), acc_reg'length);
                end loop;
                
                -- Shift validity pipeline
                valid_pipe(TAP_COUNT downto 1) <= valid_pipe(TAP_COUNT-1 downto 0);
                valid_pipe(0) <= valid_in;
            end if;
        end if;
    end process;
    
    -- Output assignment
    audio_out <= acc_reg(DATA_WIDTH+COEFF_WIDTH+4 downto COEFF_WIDTH+3);  -- Truncate and round
    valid_out <= valid_pipe(TAP_COUNT);
    
end rtl;
```

## EDGE CASES & FALLBACKS
- **Resource Overutilization**: Reduce tap count, use symmetric coefficients for half the multipliers, or implement time-multiplexed architecture
- **Timing Violations**: Add pipeline registers, reduce clock frequency, or use FPGA-specific DSP blocks
- **Coefficient Update Glitches**: Double-buffer coefficient registers with synchronous update
- **Numerical Overflow**: Implement saturation arithmetic or use wider accumulators with scaling
- **Audio Sample Rate Mismatch**: Add sample rate conversion FIFO between FPGA and host system
- **Jitter in Clock Domains**: Use asynchronous FIFOs for crossing between audio and control clock domains

## INTEGRATION POINTS
- FPGA Development Tools: Xilinx Vivado, Intel Quartus, Lattice Diamond
- Audio Interfaces: I2S, TDM, SPDIF, USB Audio Class 2.0
- Host Communication: SPI, I2C, UART, USB, PCIe
- Software Drivers: Linux kernel modules, Windows WDM/KSFT, macOS CoreAudio
- Simulation & Verification: ModelSim, QuestaSim, Verilator, VUnit
- Board Support: ZedBoard, DE10-Net, STM32MP1, BeagleBone Black PRU
- DSP Libraries: Xilinx DSP IP, Intel FPGA DSP Builder, OpenCores FIR filters

## EXECUTION EXAMPLES

**Input:** "Design a 128-tap FIR filter for 48kHz audio with programmable coefficients"
**Output:**
```vhdl
-- Resource-optimized symmetric FIR filter
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity symmetric_fir is
    Generic (
        DATA_WIDTH  : integer := 24;
        COEFF_WIDTH : integer := 18;
        TAP_COUNT   : integer := 128  -- Must be even for symmetry
    );
    Port (
        clk         : in  std_logic;
        reset_n     : in  std_logic;
        audio_in    : in  signed(DATA_WIDTH-1 downto 0);
        audio_out   : out signed(DATA_WIDTH-1 downto 0);
        coeff_addr  : in  integer range 0 to TAP_COUNT/2-1;
        coeff_data  : in  signed(COEFF_WIDTH-1 downto 0);
        coeff_we    : in  std_logic;
        valid_in    : in  std_logic;
        valid_out   : out std_logic
    );
end symmetric_fir;

architecture rtl of symmetric_fir is
    type coeff_array is array (0 to TAP_COUNT/2-1) of signed(COEFF_WIDTH-1 downto 0);
    type delay_line is array (0 to TAP_COUNT-1) of signed(DATA_WIDTH-1 downto 0);
    
    signal coeff_mem    : coeff_array := (others => (others => '0'));
    signal delay_line_reg: delay_line := (others => (others => '0'));
    signal acc_reg      : signed(DATA_WIDTH+COEFF_WIDTH+6 downto 0) := (others => '0');
    signal valid_pipe   : std_logic_vector(0 to TAP_COUNT) := (others => '0');
    
begin
    -- Single-port RAM for coefficients (symmetric implementation)
    process(clk)
    begin
        if rising_edge(clk) then
            if coeff_we = '1' then
                coeff_mem(coeff_addr) <= coeff_data;
            end if;
        end if;
    end process;
    
    -- Symmetric MAC: uses half the multipliers
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            delay_line_reg <= (others => (others => '0'));
            acc_reg <= (others => '0');
            valid_pipe <= (others => '0');
        elsif rising_edge(clk) then
            if valid_in = '1' then
                -- Update delay line
                delay_line_reg(TAP_COUNT-1 downto 1) <= delay_line_reg(TAP_COUNT-2 downto 0);
                delay_line_reg(0) <= audio_in;
                
                -- Symmetric accumulation: h[n]*x[k] + h[N-1-n]*x[k+N-1-2n]
                acc_reg <= resize(delay_line_reg(0) * coeff_mem(0), acc_reg'length);
                for i in 1 to TAP_COUNT/2-1 loop
                    acc_reg <= acc_reg + 
                               resize(delay_line_reg(i) * coeff_mem(i), acc_reg'length) +
                               resize(delay_line_reg(TAP_COUNT-1-i) * coeff_mem(i), acc_reg'length);
                end loop;
                
                valid_pipe(TAP_COUNT downto 1) <= valid_pipe(TAP_COUNT-1 downto 0);
                valid_pipe(0) <= valid_in;
            end if;
        end if;
    end process;
    
    audio_out <= acc_reg(DATA_WIDTH+COEFF_WIDTH+5 downto COEFF_WIDTH+2);  -- Proper truncation
    valid_out <= valid_pipe(TAP_COUNT);
    
end rtl;
```

**Input:** "Implement a biquad filter with programmable coefficients on FPGA"
**Output:**
```vhdl
-- Direct Form II Transposed Biquad Filter
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity biquad_filter is
    Generic (
        DATA_WIDTH  : integer := 24;
        COEFF_WIDTH : integer := 20
    );
    Port (
        clk         : in  std_logic;
        reset_n     : in  std_logic;
        audio_in    : in  signed(DATA_WIDTH-1 downto 0);
        audio_out   : out signed(DATA_WIDTH-1 downto 0);
        b0,b1,b2    : in  signed(COEFF_WIDTH-1 downto 0);
        a1,a2       : in  signed(COEFF_WIDTH-1 downto 0);
        valid_in    : in  std_logic;
        valid_out   : out std_logic
    );
end biquad_filter;

architecture rtl of biquad_filter is
    signal w_reg      : signed(DATA_WIDTH+COEFF_WIDTH downto 0) := (others => '0');
    signal w1_reg,w2_reg: signed(DATA_WIDTH+COEFF_WIDTH downto 0) := (others => '0');
    signal valid_pipe : std_logic_vector(0 to 2) := (others => '0');
    
begin
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            w_reg <= (others => '0');
            w1_reg <= (others => '0');
            w2_reg <= (others => '0');
            valid_pipe <= (others => '0');
        elsif rising_edge(clk) then
            if valid_in = '1' then
                -- Direct Form II Transposed: w[n] = x[n] - a1*w[n-1] - a2*w[n-2]
                w_reg <= resize(audio_in, w_reg'length) - 
                         resize(w1_reg * a1, w_reg'length) - 
                         resize(w2_reg * a2, w_reg'length);
                         
                -- y[n] = b0*w[n] + b1*w[n-1] + b2*w[n-2]
                audio_out <= resize(w_reg * b0, audio_out'length) +
                             resize(w1_reg * b1, audio_out'length) +
                             resize(w2_reg * b2, audio_out'length);
                             
                -- Shift registers
                w2_reg <= w1_reg;
                w1_reg <= w_reg;
                
                -- Shift validity
                valid_pipe(2 downto 1) <= valid_pipe(1 downto 0);
                valid_pipe(0) <= valid_in;
            end if;
        end if;
    end process;
    
    valid_out <= valid_pipe(2);
    
end rtl;
```