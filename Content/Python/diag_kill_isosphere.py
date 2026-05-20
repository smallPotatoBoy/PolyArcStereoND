"""
关掉 nDisplay 的 StageIsosphere 占位 mesh - 它把 sweet spot 包在球内，
导致所有 sub-camera 拍到的都是它的内壁灰色。
"""
import unreal

subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dcra = None
for a in subsys.get_all_level_actors():
    if "BP_PolyArc" in a.get_class().get_name():
        dcra = a
        break

if dcra:
    # 1. 关 bPreviewStageGeometryMesh
    try:
        dcra.set_editor_property("bPreviewStageGeometryMesh", False)
        unreal.log("Set bPreviewStageGeometryMesh = False")
    except Exception as e:
        unreal.log_warning(f"  prop set: {e}")

    # 2. 直接隐藏 IsoSphere 和 StageGeometry 组件
    for c in dcra.get_components_by_class(unreal.SceneComponent):
        cls = c.get_class().get_name()
        if "Isosphere" in cls or "StageGeometry" in cls or "StageIso" in cls:
            try:
                c.set_visibility(False, propagate_to_children=True)
                unreal.log(f"Hidden: {c.get_name()} ({cls})")
            except Exception as e:
                unreal.log_warning(f"  hide {c.get_name()}: {e}")

    # 3. 重新 dump Sub0 RT 看是不是有真实内容了
    screens = dcra.get_components_by_class(unreal.DisplayClusterScreenComponent)
    for s in screens:
        if s.get_name() == "Sub0":
            tex = s.get_materials()[0].get_texture_parameter_value("Preview")
            import os
            out_dir = unreal.Paths.project_saved_dir() + "PolyArcStereo"
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            unreal.RenderingLibrary.export_render_target(dcra, tex, out_dir, "Sub0_PreviewRT_after.png")
            unreal.log(f"Re-dumped Sub0 → {out_dir}/Sub0_PreviewRT_after.png")
            break

unreal.log("=== done ===")
