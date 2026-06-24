"""
章节树构建工具

处理 book_chapters 表的树形结构，支持两种顶级节点约定：
  - parent_id IS NULL       → 顶级章节
  - parent_id == chapter.id → 顶级章节（自引用）
"""

from typing import Any


def build_chapter_tree(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    将扁平章节列表转换为嵌套树结构。

    Args:
        rows: 扁平章节列表，每个元素需含 id, name, parent_id, sort_order

    Returns:
        树根节点列表（已按 sort_order 递归排序）
    """
    if not rows:
        return []

    # 构建 id → node 映射，预分配 children 容器
    node_map: dict[str, dict] = {}
    for r in rows:
        node_map[r["id"]] = {
            "id": r["id"],
            "name": r["name"],
            "sortOrder": r.get("sort_order", 0),
            "children": [],
        }

    roots: list[dict] = []

    for node in node_map.values():
        orig = next(r for r in rows if r["id"] == node["id"])
        parent_id = orig.get("parent_id")
        own_id = node["id"]

        # 顶级判断：parent_id 为 None 或自引用
        is_root = (parent_id is None) or (parent_id == own_id)

        if is_root:
            roots.append(node)
        else:
            parent = node_map.get(parent_id)
            if parent is not None:
                parent["children"].append(node)
            else:
                # 孤儿节点（父节点已被删除或不存在）→ 提升为顶级
                roots.append(node)

    # 递归按 sortOrder 排序
    def _sort_tree(nodes: list[dict]) -> None:
        nodes.sort(key=lambda n: n.get("sortOrder", 0))
        for n in nodes:
            if n["children"]:
                _sort_tree(n["children"])

    _sort_tree(roots)
    return roots
