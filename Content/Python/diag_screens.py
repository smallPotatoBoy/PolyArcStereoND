"""
查 4 块 Screen 组件实际的 mesh / visibility / material 状态。
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
    screens = dcra.get_components_by_class(unreal.DisplayClusterScreenComponent)
    unreal.log(f"Found {len(screens)} screen components")
    for s in screens:
        name = s.get_name()
        unreal.log(f"--- {name} ---")
        # Visibility
        try:
            unreal.log(f"  visible={s.is_visible()}  hidden_in_game={s.is_hidden_in_game()}")
        except Exception as e:
            unreal.log_warning(f"  visibility query: {e}")
        # Mesh
        try:
            mesh = s.get_editor_property("static_mesh") if hasattr(s, "get_editor_property") else None
            unreal.log(f"  static_mesh: {mesh}")
        except Exception as e:
            unreal.log_warning(f"  mesh query: {e}")
        # Material
        try:
            mats = s.get_materials() if hasattr(s, "get_materials") else None
            unreal.log(f"  materials: {[m.get_name() if m else None for m in (mats or [])]}")
        except Exception as e:
            unreal.log_warning(f"  material query: {e}")
        # Transform
        loc = s.get_world_location()
        scale = s.get_relative_transform().scale3d
        unreal.log(f"  world_loc=({loc.x:.2f},{loc.y:.2f},{loc.z:.2f}) scale=({scale.x:.2f},{scale.y:.2f},{scale.z:.2f})")
        # Try to force visible
        try:
            s.set_visibility(True, propagate_to_children=True)
            s.set_hidden_in_game(False)
            unreal.log(f"  forced visible=True, hidden_in_game=False")
        except Exception as e:
            unreal.log_warning(f"  force visible: {e}")
unreal.log("=== done ===")
