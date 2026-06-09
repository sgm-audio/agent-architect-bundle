---
name: cmake-modern-cpp
description: "Modern CMake for C++ audio plugins: target-based config, FetchContent for CLAP/ARA/VST3 SDKs, presets, toolchain files, clang-cl on Windows."
version: 1.0.0
author: SGM Studios
license: MIT
tags: [cmake, cpp, build, audio-plugin, clap]
---

# Modern CMake for C++ Audio Plugins

## Build Commands

```bash
# Configure
cmake -B build -G "Visual Studio 17 2022" -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl

# Build
cmake --build build --config Release

# Test
cmake --build build --target check
ctest --test-dir build --output-on-failure
```

## Key Patterns

- **Target-based** config (not variable soup)
- **FetchContent** for CLAP/ARA/VST3 SDK dependencies
- **Generator expressions** for platform/compiler conditionals
- **Presets** for reusable config profiles
- **clang-cl** as the Windows compiler (MSVC ABI compatible, better diagnostics)
- **Strict compile flags**: `/W4 /WX` on MSVC, `-Wall -Wextra -Werror` on GCC/Clang

## Pitfalls

- `FetchContent` downloads every configure — use `FECTHCONTENT_QUIET` or cache with `FETCHCONTENT_SOURCE_DIR_<NAME>`
- clang-cl needs `-DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl` explicitly
- Generator expressions are evaluated at build time, not configure time — use variables for configure-time logic
