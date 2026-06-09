#!/usr/bin/env python3
"""LangGraph DAG for CMake audio plugin build pipeline.

Runs: cmake configure → compile matrix → validate → test → sign → package
Exposed as both a CLI and an MCP tool.
"""

import os
import sys
import json
import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Annotated, TypedDict, Literal
from datetime import datetime

try:
    from langgraph.graph import StateGraph, END as LG_END
    from langgraph.checkpoint.memory import MemorySaver
except ImportError:
    print("Run: pip install langgraph")
    sys.exit(1)


BUILD_DIR = "build"
CONFIG = os.environ.get("CMAKE_BUILD_TYPE", "Release")
GENERATOR = os.environ.get("CMAKE_GENERATOR", "Visual Studio 17 2022")
COMPILER = os.environ.get("CMAKE_CXX_COMPILER", "clang-cl")
ARCH = os.environ.get("CMAKE_ARCH", "x64")
PROJECT_DIR = os.environ.get("PROJECT_DIR", os.getcwd())
SIGN_TOOL = os.environ.get("SIGN_TOOL", "")


class PipelineState(TypedDict):
    project_dir: str
    config: str
    arch: str
    cmake_ok: bool
    compile_results: dict
    validate_results: dict
    test_results: dict
    sign_results: dict
    package_path: str
    errors: list
    log: list


def _log(state: PipelineState, msg: str) -> None:
    state["log"].append(f"[{datetime.now().isoformat()}] {msg}")
    print(msg)


def step_cmake_configure(state: PipelineState) -> dict:
    _log(state, "=== CMake Configure ===")
    build_path = Path(state["project_dir"]) / BUILD_DIR
    build_path.mkdir(exist_ok=True)
    cmd = [
        "cmake", "-B", str(build_path),
        "-G", GENERATOR,
        f"-DCMAKE_CXX_COMPILER={COMPILER}",
        f"-DCMAKE_BUILD_TYPE={state['config']}",
    ]
    try:
        r = subprocess.run(cmd, cwd=state["project_dir"], capture_output=True, text=True, timeout=120)
        ok = r.returncode == 0
        if not ok:
            state["errors"].append(r.stderr[-2000:])
        return {"cmake_ok": ok, **({} if ok else {})}
    except subprocess.TimeoutExpired:
        state["errors"].append("cmake configure timed out")
        return {"cmake_ok": False}


def step_compile(state: PipelineState) -> dict:
    if not state["cmake_ok"]:
        return {"compile_results": {"status": "skipped"}}
    _log(state, f"=== Compile ({state['config']}) ===")
    build_path = Path(state["project_dir"]) / BUILD_DIR
    cmd = ["cmake", "--build", str(build_path), "--config", state["config"]]
    results = {}
    for target in ["all"]:
        r = subprocess.run(cmd + ["--target", target], capture_output=True, text=True, timeout=600)
        results[target] = {"ok": r.returncode == 0, "stderr": r.stderr[-1000:]}
        if r.returncode != 0:
            state["errors"].append(f"compile {target} failed: {r.stderr[-500:]}")
    return {"compile_results": results}


def step_validate(state: PipelineState) -> dict:
    if not state["cmake_ok"]:
        return {"validate_results": {"status": "skipped"}}
    _log(state, "=== Plugin Validation ===")
    build_path = Path(state["project_dir"]) / BUILD_DIR
    results = {}
    pattern = os.environ.get("PLUGIN_PATTERN", "*.clap")
    for f in build_path.rglob(pattern):
        validator = shutil.which("clap-validator") or "clap-validator"
        r = subprocess.run([validator, str(f)], capture_output=True, text=True, timeout=60)
        results[f.name] = {"ok": r.returncode == 0, "output": r.stdout[-500:]}
        if r.returncode != 0:
            state["errors"].append(f"validation failed: {f.name}")
    return {"validate_results": results}


def step_test(state: PipelineState) -> dict:
    if not state["cmake_ok"]:
        return {"test_results": {"status": "skipped"}}
    _log(state, "=== Tests ===")
    build_path = Path(state["project_dir"]) / BUILD_DIR
    r = subprocess.run(["ctest", "--test-dir", str(build_path), "--output-on-failure"],
                       capture_output=True, text=True, timeout=300)
    ok = r.returncode == 0
    if not ok:
        state["errors"].append(r.stderr[-1000:])
    return {"test_results": {"ok": ok, "output": r.stdout[-1000:]}}


def step_sign(state: PipelineState) -> dict:
    if not SIGN_TOOL or not state["cmake_ok"]:
        return {"sign_results": {"status": "skipped"}}
    _log(state, "=== Code Signing ===")
    build_path = Path(state["project_dir"]) / BUILD_DIR
    results = {}
    for ext in [".dll", ".clap", ".vst3"]:
        for f in build_path.rglob(f"*{ext}"):
            r = subprocess.run([SIGN_TOOL, "sign", str(f)], capture_output=True, text=True, timeout=60)
            results[f.name] = {"ok": r.returncode == 0}
    return {"sign_results": results}


def step_package(state: PipelineState) -> dict:
    if not state["cmake_ok"]:
        return {"package_path": ""}
    _log(state, "=== Package ===")
    pkg_dir = Path(state["project_dir"]) / "dist"
    pkg_dir.mkdir(exist_ok=True)
    pkg_name = f"plugin-{state['config']}-{state['arch']}.zip"
    pkg_path = str(pkg_dir / pkg_name)
    build_path = Path(state["project_dir"]) / BUILD_DIR
    subprocess.run(
        ["powershell", "-Command",
         f"Compress-Archive -Path '{build_path}\\*.clap','{build_path}\\*.vst3' -DestinationPath '{pkg_path}' -Force"],
        capture_output=True, text=True, timeout=60)
    _log(state, f"Packaged: {pkg_path}")
    return {"package_path": pkg_path}


def route_after_compile(state: PipelineState) -> str:
    cr = state.get("compile_results", {})
    if cr.get("all", {}).get("ok"):
        return "validate"
    return LG_END


def build_pipeline() -> StateGraph:
    workflow = StateGraph(PipelineState)

    workflow.add_node("cmake_configure", step_cmake_configure)
    workflow.add_node("compile", step_compile)
    workflow.add_node("validate", step_validate)
    workflow.add_node("test", step_test)
    workflow.add_node("sign", step_sign)
    workflow.add_node("package", step_package)

    workflow.set_entry_point("cmake_configure")
    workflow.add_edge("cmake_configure", "compile")
    workflow.add_conditional_edges("compile", route_after_compile)
    workflow.add_edge("validate", "test")
    workflow.add_edge("test", "sign")
    workflow.add_edge("sign", "package")
    workflow.add_edge("package", LG_END)

    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)


async def run_pipeline(project_dir: str, config: str = "Release", arch: str = "x64") -> dict:
    graph = build_pipeline()
    initial = PipelineState(
        project_dir=project_dir,
        config=config,
        arch=arch,
        cmake_ok=False,
        compile_results={},
        validate_results={},
        test_results={},
        sign_results={},
        package_path="",
        errors=[],
        log=[],
    )
    result = await graph.ainvoke(initial)
    return result


# ── CLI ──
def cli():
    import argparse
    p = argparse.ArgumentParser(description="CMake build pipeline DAG")
    p.add_argument("--project-dir", default=os.getcwd())
    p.add_argument("--config", default="Release")
    p.add_argument("--arch", default="x64")
    args = p.parse_args()

    result = asyncio.run(run_pipeline(args.project_dir, args.config, args.arch))
    print(json.dumps({
        "ok": result["cmake_ok"] and result.get("test_results", {}).get("ok", True),
        "package": result["package_path"],
        "errors": result["errors"],
        "log": result["log"],
    }, indent=2))


# ── MCP Server ──
def run_mcp():
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio

    server = Server("cmake-pipeline")

    @server.list_tools()
    async def list_tools():
        return [{
            "name": "run_cmake_pipeline",
            "description": "Run the full CMake build DAG: configure → compile → validate → test → sign → package",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_dir": {"type": "string", "description": "Project root with CMakeLists.txt"},
                    "config": {"type": "string", "enum": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]},
                    "arch": {"type": "string", "default": "x64"},
                },
                "required": ["project_dir"],
            },
        }]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list:
        if name != "run_cmake_pipeline":
            raise ValueError(f"Unknown tool: {name}")
        result = await run_pipeline(
            project_dir=arguments["project_dir"],
            config=arguments.get("config", "Release"),
            arch=arguments.get("arch", "x64"),
        )
        ok = result["cmake_ok"] and result.get("test_results", {}).get("ok", True)
        status = "ok" if ok else "failed"
        summary = f"Pipeline {status} | package: {result['package_path'] or 'none'}"
        if result["errors"]:
            summary += f"\nErrors: {len(result['errors'])}"
        return [{"type": "text", "text": json.dumps({"status": status, "summary": summary, "log": result["log"], "errors": result["errors"]}, indent=2)}]

    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, InitializationOptions(
                server_name="cmake-pipeline",
                server_version="0.1.0",
            ))

    asyncio.run(main())


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "cli"
    if mode == "mcp":
        run_mcp()
    else:
        cli()
