"""
诊断 nDisplay editor preview 为什么不显示画面。
打印 DCRA 的关键 preview 属性 + 强制启用一遍 + 找 viewport / 检查是否 realtime。

用法（UE 控制台）：
    py D:/Claude/UE5/PolyArcStereoND/Content/Python/diag_preview.py
"""

import unreal

subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = subsys.get_all_level_actors()
dcra = None
for a in actors:
    cls_name = a.get_class().get_name()
    if "DisplayClusterRoot" in cls_name or "BP_PolyArc" in cls_name:
        dcra = a
        break

if not dcra:
    unreal.log_error("No DisplayClusterRootActor found in level")
else:
    unreal.log(f"=== DCRA: {dcra.get_actor_label()} class={dcra.get_class().get_name()} ===")

    # 关键 preview 属性
    props_to_read = [
        "bPreviewEnable",
        "PreviewNodeId",
        "PreviewRenderTargetRatioMult",
        "bPreviewEnablePostProcess",
        "bFreezePreviewRender",
        "bPreviewICVFXFrustums",
    ]
    for p in props_to_read:
        try:
            v = dcra.get_editor_property(p)
            unreal.log(f"  {p} = {v}")
        except Exception as e:
            unreal.log_warning(f"  {p}: cannot read ({e})")

    # 强制再设一遍 + 触发刷新
    unreal.log("--- forcing preview settings ---")
    try:
        dcra.set_editor_property("bPreviewEnable", True)
        dcra.set_editor_property("PreviewNodeId", "node_main")
        dcra.set_editor_property("PreviewRenderTargetRatioMult", 1.0)
        dcra.set_editor_property("bPreviewEnablePostProcess", True)
        dcra.set_editor_property("bFreezePreviewRender", False)
        unreal.log("Forced settings applied. Now check Details > Preview tab.")
    except Exception as e:
        unreal.log_error(f"Failed to force settings: {e}")

# 检查编辑器 viewport 是否 Realtime
unreal.log("--- editor viewports realtime state ---")
try:
    editor_subsys = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    # API 可能没有直接 read realtime；用 console command 强制开
    unreal.SystemLibrary.execute_console_command(None, "r.AllowOcclusionQueries 1")
    unreal.log("  (no direct realtime probe; press Ctrl+R in viewport to toggle)")
except Exception as e:
    unreal.log_warning(f"  cannot probe viewport: {e}")

unreal.log("=== diag done ===")
