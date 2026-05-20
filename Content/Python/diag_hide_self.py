"""
假设：sub-screen mesh 互相遮挡，拍到全是别的屏的灰色背面。
方案：让 sub-screen mesh 对所有 SceneCapture / nDisplay capture 视图不可见
"""
import unreal

subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dcra = None
for a in subsys.get_all_level_actors():
    if "BP_PolyArc" in a.get_class().get_name():
        dcra = a
        break

if dcra:
    screens = dcra.get_components_by_class(unreal.DisplayClusterScreenComponent)
    for s in screens:
        # 关键：bOwnerNoSee = 不让本 actor 自己的相机看到这个 mesh
        # 但 SceneCapture/nDisplay capture 都是这个 DCRA 拥有的，所以 OwnerNoSee 应该够
        try:
            s.set_editor_property("bOwnerNoSee", True)
            unreal.log(f"{s.get_name()}: set bOwnerNoSee=True")
        except Exception as e:
            unreal.log_warning(f"{s.get_name()} OwnerNoSee: {e}")

        # 备选：bRenderInMainPass / bRenderInDepthPass
        try:
            s.set_editor_property("bRenderInMainPass", True)  # 主 viewport 还能看到
            s.set_editor_property("bRenderInDepthPass", True)
        except Exception:
            pass

    # 重新 dump Sub0
    s0 = next((s for s in screens if s.get_name() == "Sub0"), None)
    if s0:
        tex = s0.get_materials()[0].get_texture_parameter_value("Preview")
        import os
        out_dir = unreal.Paths.project_saved_dir() + "PolyArcStereo"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        unreal.RenderingLibrary.export_render_target(dcra, tex, out_dir, "Sub0_PreviewRT_hidden.png")
        unreal.log(f"Re-dumped → Sub0_PreviewRT_hidden.png")

unreal.log("=== done ===")
