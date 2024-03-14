from qgis.core import QgsLayerTreeGroup

__all__ = ["duplicate_groups"]


def duplicate_groups(group_root, appendix: str = " (Copy)") -> QgsLayerTreeGroup:
    parent = group_root.parent
    new_group = parent.addGroup(f"{group_root.name()}{appendix}")
    for child in group_root.children():
        if isinstance(child, QgsLayerTreeGroup):
            duplicate_groups(child, appendix="")  # Only top level
        else:
            new_group.addChildNode(child.clone())

    return new_group
