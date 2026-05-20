"""
强制触发 nDisplay preview render + 检查 MID 上的 texture 参数实际值
"""
import unreal

subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dcra = None
for a in subsys.get_all_level_actors():
    if "BP_PolyArc" in a.get_class().get_name():
        dcra = a
        break

if not dcra:
    unreal.log_error("DCRA not found")
else:
    unreal.log(f"=== DCRA: {dcra.get_actor_label()} ===")

    # 列所有 display device 组件，看是不是有"双胞胎"
    dds = dcra.get_components_by_class(unreal.DisplayClusterDisplayDeviceBaseComponent) if hasattr(unreal, 'DisplayClusterDisplayDeviceBaseComponent') else []
    if not dds:
        # try generic name
        for c in dcra.get_components_by_class(unreal.SceneComponent):
            cls_name = c.get_class().get_name()
            if "DisplayDevice" in cls_name:
                dds.append(c)
    unreal.log(f"--- DisplayDevice components ({len(dds)}) ---")
    for d in dds:
        unreal.log(f"  [{d.get_class().get_name()}] {d.get_name()}")

    # 检查每块屏的 MID 上的 texture 参数
    unreal.log("--- Each Sub's material texture params ---")
    screens = dcra.get_components_by_class(unreal.DisplayClusterScreenComponent)
    for s in screens:
        mats = s.get_materials()
        for i, m in enumerate(mats):
            if m is None:
                continue
            try:
                # Cast to MID
                mid = unreal.MaterialInstanceDynamic.cast(m) if hasattr(unreal.MaterialInstanceDynamic, 'cast') else m
                tex_params = ['Preview', 'PreviewTexture', 'Texture', 'BaseColor', 'MainTexture']
                for tp in tex_params:
                    try:
                        v = mid.get_texture_parameter_value(tp) if hasattr(mid, 'get_texture_parameter_value') else None
                        if v:
                            unreal.log(f"    {s.get_name()} mat[{i}].{tp} = {v}")
                    except Exception:
                        pass
            except Exception as e:
                unreal.log_warning(f"    {s.get_name()} mat[{i}]: {e}")

    # 强制触发 preview render
    unreal.log("--- Forcing preview render ---")

    # 直接调 ADisplayClusterRootActor::TickPreviewRenderer 不可见；用 marker 改 property 触发 reconfig
    try:
        # 关 → 开，触发 cycle
        dcra.set_editor_property("bPreviewEnable", False)
        dcra.set_editor_property("bPreviewEnable", True)
        unreal.log("Toggled bPreviewEnable False→True")
    except Exception as e:
        unreal.log_warning(f"toggle bPreviewEnable: {e}")

    # 强制 mark render
    try:
        dcra.modify()
        dcra.rerun_construction_scripts()
        unreal.log("Reran construction scripts on DCRA")
    except Exception as e:
        unreal.log_warning(f"rerun_construction_scripts: {e}")

unreal.log("=== done ===")
