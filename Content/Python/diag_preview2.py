"""
更深入的 preview 诊断：
- 列出 DCRA 上所有组件
- 检查 ConfigData 是否真的有 cluster node / viewports
- 强制重启 cluster preview
"""

import unreal

# 找到 DCRA
subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dcra = None
for a in subsys.get_all_level_actors():
    cls = a.get_class().get_name()
    if "BP_PolyArc" in cls or "DisplayClusterRoot" in cls:
        dcra = a
        break

if not dcra:
    unreal.log_error("DCRA not found")
else:
    unreal.log(f"=== DCRA found: {dcra.get_actor_label()} ===")

    # 1. 列出所有组件
    unreal.log("--- Components ---")
    for c in dcra.get_components_by_class(unreal.SceneComponent):
        unreal.log(f"  [{c.get_class().get_name()}] {c.get_name()}  loc={c.get_world_location()}")

    # 2. CurrentConfigData
    unreal.log("--- CurrentConfigData ---")
    try:
        cfg = dcra.get_editor_property("CurrentConfigData")
        if not cfg:
            unreal.log_error("CurrentConfigData is None!")
        else:
            unreal.log(f"  ConfigData: {cfg}")
            try:
                cluster = cfg.get_editor_property("Cluster")
                if cluster:
                    nodes = cluster.get_editor_property("Nodes")
                    unreal.log(f"  Nodes count: {len(nodes) if nodes else 0}")
                    if nodes:
                        for key in nodes.keys():
                            node = nodes[key]
                            vps = node.get_editor_property("Viewports")
                            unreal.log(f"    Node '{key}': {len(vps) if vps else 0} viewports")
                            if vps:
                                for vpkey in vps.keys():
                                    vp = vps[vpkey]
                                    cam = vp.get_editor_property("Camera")
                                    proj = vp.get_editor_property("ProjectionPolicy")
                                    proj_type = proj.get_editor_property("Type") if proj else "?"
                                    proj_params = proj.get_editor_property("Parameters") if proj else {}
                                    unreal.log(f"      vp '{vpkey}': Camera='{cam}' Policy type='{proj_type}' params={dict(proj_params) if proj_params else {}}")
                scene = cfg.get_editor_property("Scene")
                if scene:
                    cams = scene.get_editor_property("Cameras")
                    screens = scene.get_editor_property("Screens")
                    unreal.log(f"  Scene.Cameras: {list(cams.keys()) if cams else []}")
                    unreal.log(f"  Scene.Screens: {list(screens.keys()) if screens else []}")
            except Exception as e:
                unreal.log_warning(f"  reading cluster: {e}")
    except Exception as e:
        unreal.log_warning(f"cannot read CurrentConfigData: {e}")

unreal.log("=== diag2 done ===")
