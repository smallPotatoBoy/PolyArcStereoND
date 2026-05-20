"""
Spawn 一个普通 SceneCaptureComponent2D 在 sweet spot 位置同朝向，拍到 RT，存 PNG。
如果普通 capture 也是均匀灰 → 场景本身那个方向是空的（rig 位置问题）
如果普通 capture 正常 → nDisplay 特定的渲染问题
"""
import unreal, os

subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dcra = None
sweet_spot = None
for a in subsys.get_all_level_actors():
    if "BP_PolyArc" in a.get_class().get_name():
        dcra = a
        break

if dcra:
    # 找 SweetSpot
    for c in dcra.get_components_by_class(unreal.SceneComponent):
        if c.get_name() == "SweetSpot":
            sweet_spot = c
            break

if not sweet_spot:
    unreal.log_error("SweetSpot not found")
else:
    loc = sweet_spot.get_world_location()
    rot = sweet_spot.get_world_rotation()
    unreal.log(f"Sweet spot world: loc={loc} rot={rot}")

    # Spawn 一个新 actor 装 SceneCapture
    cap_actor_class = unreal.SceneCapture2D
    cap_actor = subsys.spawn_actor_from_class(cap_actor_class, loc, rot)
    if cap_actor:
        cap_actor.set_actor_label("DiagBaselineCapture")
        cap = cap_actor.get_component_by_class(unreal.SceneCaptureComponent2D)
        # 创建 RT
        rt = unreal.RenderingLibrary.create_render_target2d(dcra, 903, 2236, unreal.TextureRenderTargetFormat.RTF_RGBA16F)
        cap.set_editor_property("texture_target", rt)
        cap.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_HDR)
        cap.set_editor_property("bCaptureEveryFrame", True)
        cap.set_editor_property("FOVAngle", 90.0)  # 简单 FoV
        # 强制 capture
        cap.capture_scene()
        unreal.log(f"Captured scene from sweet spot ({loc.x},{loc.y},{loc.z}) with FOV 90°")

        out_dir = unreal.Paths.project_saved_dir() + "PolyArcStereo"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        unreal.RenderingLibrary.export_render_target(dcra, rt, out_dir, "Baseline_Capture.png")
        unreal.log(f"Exported → {out_dir}/Baseline_Capture.png")

        # 清理: destroy 后避免污染场景
        subsys.destroy_actor(cap_actor)
        unreal.log("Destroyed test capture actor")

unreal.log("=== done ===")
