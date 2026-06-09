---
name: cmake-modern-cpp
description: Use this skill when the user is working on or asking about modern CMake for C++ audio plugins, FetchContent for CLAP/ARA/VST3 SDKs, target-based build configuration, generator expressions, presets, toolchain files, or cross-platform CMake for audio software.
version: 1.0.0
---

# Skill: Modern CMake for C++ Audio Plugins

## 1. Overview
Covers modern (3.20+) CMake patterns for C++ audio plugin development — target-centric builds, dependency fetching, export generation, sanitizer presets, and cross-compilation. Emphasizes the patterns needed for CLAP, VST3, and ARA projects.

## 2. Core Functionality
- **Target-Based Builds:** `add_library`, `target_include_directories`, `target_link_libraries`, `target_compile_features`, `target_compile_options`, `target_sources` with `PRIVATE`/`PUBLIC`/`INTERFACE`
- **SDK Management:** `FetchContent` for CLAP (`clap-helpers`), VST3 SDK, ARA SDK, JUCE — with version pins and shallow clones
- **Generator Expressions:** `$<CONFIG:Debug>`, `$<CXX_COMPILER_ID:Clang>`, `$<PLATFORM_ID:Windows>`, `$<TARGET_PROPERTY>` for conditional logic
- **CMake Presets:** `CMakePresets.json` / `CMakeUserPresets.json` — build, test, and configure presets with toolchain and cache variable overlays
- **Toolchains:** `cmake-toolchains` for cross-compilation (x86 → ARM, Windows → Linux audio plugin targets)
- **Export & Install:** `install(TARGETS)`, `export(EXPORT)`, `generate_export_header` for shared plugin builds
- **Sanitizers:** ASan, UBSan, MSan presets for debug builds: `-fsanitize=address,undefined -fno-omit-frame-pointer`

## 3. Input/Output Schema
| Inputs | `CMakeLists.txt`, `CMakePresets.json`, toolchain file, SDK versions |
| Outputs | Build targets, compile_commands.json (for clangd), install tree, SDK fetch cache |
| Config | `-DCMAKE_BUILD_TYPE=Release`, `-DCMAKE_CXX_COMPILER=clang-cl`, `-DENABLE_ARA=ON` |

## 4. Architecture
Modern CMake is graph-based: each library (plugin, DSP core, GUI) is a `CMake` target with interface dependencies. `FetchContent` populates SDKs at configure time. Presets define the build matrix. The `compile_commands.json` exports flags for clangd and clang-tidy.

## 5. Dependencies
`cmake 3.20+` (3.28+ recommended for presets), python3 (for `run-clang-tidy`), `ninja` (preferred generator) or Visual Studio, `clang-cl`/`clang++` for Windows

## 6. Edge Cases
| FetchContent Cache Stale | SDK version changed | `rm -rf _deps/*` and reconfigure |
| Generator Mismatch | Ninja vs MSBuild flags | Use `-G Ninja` for speed, MSBuild for `/analyze` |
| Export Header Missing | `generate_export_header` not called | `include(GenerateExportHeader)` before usage |
| ABI Incompatibility | VST3 built with different CRT | Set `/MD` for MSVC, match host's CRT linkage |
| clangd Fails | No `compile_commands.json` | `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` in presets |

## 7. Constraints
- JUCE projects need `juce_add_plugin()` macro — requires `JUCE_ROOT` or FetchContent JUCE
- CLAP projects: `add_subdirectory(clap-helpers)` provides `clap-helpers` target
- VST3 SDK: `find_package(VST3SDK CONFIG)` or FetchContent from Steinberg's GitLab
- ARA SDK is proprietary — `FetchContent` may not work; use `find_package` with `ARA_SDK_ROOT`
- Windows: prefer `clang-cl` over MSVC for better clangd integration

## 8. Usage
- *Prompt:* "Write a CMakeLists.txt for a CLAP+VST3+ARA plugin using FetchContent."
- *Prompt:* "Create a CMakePresets.json with Debug (ASan), Release, and MinSizeRel profiles."
- *Prompt:* "Add a cross-compilation toolchain for building a Windows VST3 on Linux."
- *Prompt:* "Generate an export header for the plugin's public API."

## 9. Testing
- `cmake --build build --target check` (CTest integration)
- `cmake --build build --target clang-tidy` (lint target)
- Verify `compile_commands.json` exists in build dir
- Test presets: `cmake --preset <name>`

## 10. Best Practices
- Pin all `FetchContent` versions with `GIT_TAG` and `GIT_SHALLOW TRUE`
- Use `CMAKE_CXX_STANDARD 20` with `CMAKE_CXX_STANDARD_REQUIRED YES`
- Separate `src/` (private) from `include/` (public headers) per target
- Set `CMAKE_EXPORT_COMPILE_COMMANDS ON` in all presets for clangd
- For ARA builds: `add_compile_definitions(JUCE_ARA=1)` before JUCE target creation
- Run `cmake -B build --graphviz=deps.dot && dot -Tpng deps.dot -o deps.png` to visualize dependency graph
*Skill Version: 1.0.0 | Standards: CMake 3.28+, Ninja, FetchContent | Domain: Build Systems*
