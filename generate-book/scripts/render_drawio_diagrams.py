#!/usr/bin/env python3
"""将 generate-book（代码库模式）的图表 JSON 规格渲染为 draw.io XML 文件。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


NODE_WIDTH = 180
NODE_HEIGHT = 72
COL_GAP = 260
ROW_GAP = 160

STYLE_BY_TYPE = {
    "source": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#64748b;",
    "component": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#64748b;",
    "service": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#64748b;",
    "state": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#64748b;",
    "decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff7ed;strokeColor=#ea580c;",
    "data": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#64748b;",
    "default": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#64748b;",
}

GROUP_STYLE = (
    "swimlane;html=1;startSize=28;horizontal=1;rounded=1;"
    "fillColor=#f8fafc;strokeColor=#94a3b8;fontColor=#334155;"
    "collapsible=0;recursiveResize=0;"
)

EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
    "jettySize=auto;html=1;endArrow=block;endFill=1;"
    "strokeColor=#64748b;fontColor=#475569;"
)


def fail(message: str) -> None:
    raise ValueError(message)


def load_spec(path: Path) -> dict[str, Any]:
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: 无效的 JSON: {exc}")
    if not isinstance(spec, dict):
        fail(f"{path}: 顶层值必须是对象")
    return spec


def validate_spec(spec: dict[str, Any], path: Path) -> None:
    for key in ("id", "title", "nodes", "edges"):
        if key not in spec:
            fail(f"{path}: 缺少必需的键: {key}")
    if not isinstance(spec["nodes"], list) or len(spec["nodes"]) < 2:
        fail(f"{path}: nodes 必须包含至少两个条目")
    if not isinstance(spec["edges"], list) or len(spec["edges"]) < 1:
        fail(f"{path}: edges 必须包含至少一个条目")

    node_ids: set[str] = set()
    for node in spec["nodes"]:
        if not isinstance(node, dict):
            fail(f"{path}: 每个节点必须是对象")
        for key in ("id", "label"):
            if not node.get(key):
                fail(f"{path}: 节点缺少 {key}")
        node_id = str(node["id"])
        if not node_id.replace("-", "").replace("_", "").isalnum():
            fail(f"{path}: 节点 id 必须为稳定的 ASCII 字符: {node_id}")
        if node_id in node_ids:
            fail(f"{path}: 重复的节点 id: {node_id}")
        node_ids.add(node_id)

    for group in spec.get("groups", []):
        if not isinstance(group, dict):
            fail(f"{path}: 每个分组必须是对象")
        for node_id in group.get("nodes", []):
            if node_id not in node_ids:
                fail(f"{path}: 分组引用了不存在的节点: {node_id}")

    for edge in spec["edges"]:
        if not isinstance(edge, dict):
            fail(f"{path}: 每条边必须是对象")
        if edge.get("from") not in node_ids:
            fail(f"{path}: 边引用了不存在的源节点: {edge.get('from')}")
        if edge.get("to") not in node_ids:
            fail(f"{path}: 边引用了不存在的目标节点: {edge.get('to')}")
        if not edge.get("evidence") and not edge.get("inferred_reason"):
            fail(f"{path}: 边 {edge.get('from')}->{edge.get('to')} 需要 evidence 或 inferred_reason")


def positions(spec: dict[str, Any]) -> dict[str, tuple[int, int]]:
    layout = spec.get("layout", "left-right")
    node_count = len(spec["nodes"])
    columns = 3 if layout == "top-down" else min(5, max(1, node_count))
    if layout == "left-right" and node_count <= 6:
        columns = node_count

    coords: dict[str, tuple[int, int]] = {}
    for index, node in enumerate(spec["nodes"]):
        if "position" in node:
            pos = node["position"]
            coords[node["id"]] = (int(pos["x"]), int(pos["y"]))
            continue
        col = index % columns
        row = index // columns
        coords[node["id"]] = (100 + col * COL_GAP, 120 + row * ROW_GAP)
    return coords


def diagram_size(coords: dict[str, tuple[int, int]]) -> tuple[int, int]:
    max_x = max((x for x, _ in coords.values()), default=100) + NODE_WIDTH + 140
    max_y = max((y for _, y in coords.values()), default=100) + NODE_HEIGHT + 140
    return max(1169, max_x), max(827, max_y)


def group_geometry(group: dict[str, Any], coords: dict[str, tuple[int, int]]) -> tuple[int, int, int, int]:
    if "bounds" in group:
        bounds = group["bounds"]
        return int(bounds["x"]), int(bounds["y"]), int(bounds["width"]), int(bounds["height"])

    node_ids = [node_id for node_id in group.get("nodes", []) if node_id in coords]
    if not node_ids:
        return 40, 40, 240, 120

    min_x = min(coords[node_id][0] for node_id in node_ids)
    min_y = min(coords[node_id][1] for node_id in node_ids)
    max_x = max(coords[node_id][0] for node_id in node_ids) + NODE_WIDTH
    max_y = max(coords[node_id][1] for node_id in node_ids) + NODE_HEIGHT
    return min_x - 40, min_y - 54, (max_x - min_x) + 80, (max_y - min_y) + 94


def cell(parent: ET.Element, tag: str, attrs: dict[str, str]) -> ET.Element:
    return ET.SubElement(parent, tag, attrs)


def render_spec(spec: dict[str, Any]) -> ET.ElementTree:
    coords = positions(spec)
    page_width, page_height = diagram_size(coords)

    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "type": "device"})
    diagram = ET.SubElement(mxfile, "diagram", {"name": str(spec["title"])})
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": str(page_width),
            "dy": str(page_height),
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(page_width),
            "pageHeight": str(page_height),
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(model, "root")
    cell(root, "mxCell", {"id": "0"})
    cell(root, "mxCell", {"id": "1", "parent": "0"})

    for index, group in enumerate(spec.get("groups", []), start=1):
        group_id = str(group.get("id", f"group-{index}"))
        x, y, width, height = group_geometry(group, coords)
        group_cell = cell(
            root,
            "mxCell",
            {
                "id": group_id,
                "value": str(group.get("label", group_id)),
                "style": str(group.get("style", GROUP_STYLE)),
                "vertex": "1",
                "parent": "1",
            },
        )
        ET.SubElement(
            group_cell,
            "mxGeometry",
            {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
        )

    for node in spec["nodes"]:
        node_id = str(node["id"])
        x, y = coords[node_id]
        style = STYLE_BY_TYPE.get(str(node.get("type", "default")), STYLE_BY_TYPE["default"])
        if node.get("style"):
            style = str(node["style"])
        node_cell = cell(
            root,
            "mxCell",
            {
                "id": node_id,
                "value": str(node["label"]),
                "style": style,
                "vertex": "1",
                "parent": "1",
            },
        )
        ET.SubElement(
            node_cell,
            "mxGeometry",
            {
                "x": str(x),
                "y": str(y),
                "width": str(int(node.get("width", NODE_WIDTH))),
                "height": str(int(node.get("height", NODE_HEIGHT))),
                "as": "geometry",
            },
        )

    for index, edge in enumerate(spec["edges"], start=1):
        edge_id = f"edge-{index}"
        edge_cell = cell(
            root,
            "mxCell",
            {
                "id": edge_id,
                "value": str(edge.get("label", "")),
                "style": str(edge.get("style", EDGE_STYLE)),
                "edge": "1",
                "parent": "1",
                "source": str(edge["from"]),
                "target": str(edge["to"]),
            },
        )
        ET.SubElement(edge_cell, "mxGeometry", {"relative": "1", "as": "geometry"})

    return ET.ElementTree(mxfile)


def render_directory(spec_dir: Path, output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(spec_dir.glob("*.json")):
        spec = load_spec(path)
        validate_spec(spec, path)
        tree = render_spec(spec)
        target = output_dir / f"{path.stem}.drawio"
        tree.write(target, encoding="utf-8", xml_declaration=True)
        count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="将图表 JSON 规格文件渲染为 draw.io XML 文件"
    )
    parser.add_argument("spec_dir", type=Path, help="包含 JSON 规格文件的目录")
    parser.add_argument("output_dir", type=Path, help="输出 draw.io 文件的目录")
    args = parser.parse_args(argv)
    try:
        count = render_directory(args.spec_dir, args.output_dir)
    except ValueError as exc:
        print(f"失败: {exc}", file=sys.stderr)
        return 1
    print(f"成功: 已渲染 {count} 个 draw.io 图表")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
