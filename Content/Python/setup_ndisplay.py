"""
PolyArcStereoND nDisplay 一键安装脚本

功能：
    1) 把 Config/PolyArcStereo.ndisplay 文本配置 import 进 UE，变成
       一个 DisplayClusterBlueprint 资产，路径 /Game/nDisplay/BP_PolyArcStereo
    2) 在当前打开的关卡里 spawn 一个该 blueprint 的实例（DisplayClusterRootActor）

用法（UE 控制台 / Output Log）：
    py D:/Claude/UE5/PolyArcStereoND/Content/Python/setup_ndisplay.py

成功后可在场景里选中 ADisplayClusterRootActor，Details 里能看到 4 个 viewports
和 4 个 Screen 组件 (Sub0..Sub3) 以及 SweetSpot camera。
"""

import unreal
import os

PROJECT_DIR = unreal.Paths.project_dir()
NDISPLAY_FILE = os.path.normpath(os.path.join(PROJECT_DIR, "Config", "PolyArcStereo.ndisplay"))
DEST_PACKAGE_PATH = "/Game/nDisplay"
DEST_ASSET_NAME = "BP_PolyArcStereo"
DEST_FULL_PATH = f"{DEST_PACKAGE_PATH}/{DEST_ASSET_NAME}"

def import_ndisplay_blueprint():
    """Import .ndisplay JSON → DisplayClusterBlueprint asset."""
    if not os.path.exists(NDISPLAY_FILE):
        unreal.log_error(f"NDISPLAY config not found: {NDISPLAY_FILE}")
        return None

    # 确保目标目录存在
    if not unreal.EditorAssetLibrary.does_directory_exist(DEST_PACKAGE_PATH):
        unreal.EditorAssetLibrary.make_directory(DEST_PACKAGE_PATH)

    # 已存在则先删旧的（方便重跑脚本迭代）
    if unreal.EditorAssetLibrary.does_asset_exist(DEST_FULL_PATH):
        unreal.log_warning(f"Existing asset will be replaced: {DEST_FULL_PATH}")
        unreal.EditorAssetLibrary.delete_asset(DEST_FULL_PATH)

    # 走 AssetTools 的导入 API
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", NDISPLAY_FILE)
    task.set_editor_property("destination_path", DEST_PACKAGE_PATH)
    task.set_editor_property("destination_name", DEST_ASSET_NAME)
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)
    task.set_editor_property("replace_existing", True)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])

    imported = task.get_editor_property("imported_object_paths")
    if not imported:
        unreal.log_error("Import failed: no objects imported. Check Output Log for parser errors.")
        return None

    unreal.log(f"Imported: {imported[0]}")
    return imported[0]

def spawn_root_actor(blueprint_path):
    """在当前关卡里 spawn DisplayClusterRootActor (用刚导入的 blueprint)。"""
    bp = unreal.EditorAssetLibrary.load_asset(blueprint_path)
    if not bp:
        unreal.log_error(f"Failed to load blueprint at {blueprint_path}")
        return None

    # 获取它的生成类（GeneratedClass）
    generated_class = bp.generated_class() if hasattr(bp, "generated_class") else None
    if generated_class is None:
        # 备用：直接用 blueprint 的 class
        generated_class = bp
        unreal.log_warning(f"blueprint.generated_class() unavailable, using blueprint object directly: {bp}")

    subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    spawn_loc = unreal.Vector(0.0, 0.0, 100.0)
    spawn_rot = unreal.Rotator(0.0, 0.0, 0.0)
    actor = subsys.spawn_actor_from_class(generated_class, spawn_loc, spawn_rot)
    if actor:
        actor.set_actor_label("PolyArcStereoRig_ND")
        unreal.log(f"Spawned: {actor.get_actor_label()} at {spawn_loc}")
    else:
        unreal.log_error("spawn_actor_from_class returned None")
    return actor

# -------- main --------
unreal.log("=== PolyArcStereoND nDisplay setup ===")
unreal.log(f"NDISPLAY file: {NDISPLAY_FILE}")
imported_path = import_ndisplay_blueprint()
if imported_path:
    spawn_root_actor(imported_path)
else:
    unreal.log_error("Setup aborted (import failed).")
unreal.log("=== done ===")
