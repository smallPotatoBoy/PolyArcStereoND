"""
导一个 sub-screen 的 preview RT 到 PNG，看是不是真的全白（== 没渲染）
+ 强制触发整个 cluster 渲染一次
"""
import unreal, os

subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dcra = None
for a in subsys.get_all_level_actors():
    if "BP_PolyArc" in a.get_class().get_name():
        dcra = a
        break

if not dcra:
    unreal.log_error("DCRA not found")
else:
    screens = dcra.get_components_by_class(unreal.DisplayClusterScreenComponent)
    s0 = screens[0] if screens else None
    if s0:
        mats = s0.get_materials()
        mid = mats[0]
        tex = mid.get_texture_parameter_value("Preview")
        unreal.log(f"Sub0 Preview tex: {tex} (size={tex.size_x}x{tex.size_y} fmt={tex.render_target_format})")

        out_dir = unreal.Paths.project_saved_dir() + "PolyArcStereo"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        unreal.RenderingLibrary.export_render_target(dcra, tex, out_dir, "Sub0_PreviewRT.png")
        unreal.log(f"Exported to {out_dir}/Sub0_PreviewRT.png")

    # 试 ADisplayClusterRootActor 上各种可能触发 render 的 method
    methods_to_try = ['tick', 'reregister_all_components', 'register_all_actor_tick_functions']
    for m in methods_to_try:
        if hasattr(dcra, m):
            unreal.log(f"DCRA has method '{m}'")
        else:
            unreal.log(f"DCRA does NOT have method '{m}'")

    # 看 actor 是不是真的在 tick
    unreal.log(f"actor.is_actor_tick_enabled: {dcra.is_actor_tick_enabled() if hasattr(dcra, 'is_actor_tick_enabled') else 'N/A'}")

    # 强制 enable tick
    try:
        dcra.set_actor_tick_enabled(True)
        unreal.log("set_actor_tick_enabled(True)")
    except Exception as e:
        unreal.log_warning(f"set_actor_tick_enabled: {e}")

unreal.log("=== done ===")
