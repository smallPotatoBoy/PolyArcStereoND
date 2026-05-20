# PolyArcStereoND

UE 5.5.4 project for curved polarized LED stereoscopic display rendering, **rebuilt on top of nDisplay** (replaces the discontinued from-scratch `PolyArcStereo` plugin).

## Why nDisplay

The custom multi-frustum rendering pipeline (4×2 SceneCaptureComponent2D + custom off-axis matrix + manual RHI compositing) we tried in the previous project hit too many UE5 internal coordinate-system conventions, view-space basis traps, and PostProcess re-enable footguns. nDisplay's `Simple` projection policy already implements exactly the same Kooima off-axis math, with all the basis sign conventions handled correctly and the multi-viewport rendering (Lumen/TAA history/shadow cascade) properly shared.

What we keep from the old project:
- Design doc §1.4 (project parameters: L=6720mm, R=12052.62mm, θ=31.948°, 3612×2236 px, etc.)
- Concept of M4 cross-talk compensation and M5 column-interleave output
- Stereo3D544 host project's ScreenGeometryAsset values (re-encoded as nDisplay config)

What we replace:
- M1 (geometry visualization) → `UDisplayClusterScreenComponent` placed in level
- M2 (multi-frustum stereo rig) → nDisplay viewports with `Simple` projection policy
- M3 (sub-RT → canvas compositing) → nDisplay built-in frame composition

What stays our IP (custom `PolyArcStereoFX` plugin under `Plugins/`):
- **M4 Cross-Talk Compensation** → `IDisplayClusterPostProcess::PerformPostProcessViewAfterWarpBlend_RenderThread`
- **M5 Column-Interleave Output** → `IDisplayClusterPostProcess::PerformPostProcessFrameAfterWarpBlend_RenderThread`

## Repo structure

```
PolyArcStereoND/
├── PolyArcStereoND.uproject
├── Source/                           Project module
│   ├── PolyArcStereoND/             (Runtime module, currently empty - room for level scripts)
│   ├── PolyArcStereoND.Target.cs
│   └── PolyArcStereoNDEditor.Target.cs
├── Plugins/
│   └── PolyArcStereoFX/             Our custom nDisplay extension (M4 + M5)
│       ├── PolyArcStereoFX.uplugin
│       └── Source/PolyArcStereoFX/
│           ├── PolyArcStereoFX.Build.cs
│           ├── Public/PolyArcStereoFXModule.h
│           └── Private/PolyArcStereoFXModule.cpp    (factory registration scaffold)
├── Config/
└── Content/                          Future: nDisplayConfig asset, DisplayClusterRootActor blueprint
```

## Build

UE 5.5.4 + Visual Studio 2022. Right-click `PolyArcStereoND.uproject` → "Generate Visual Studio project files" → build the editor target.

```powershell
& 'D:\Program Files\Epic Games\UE_5.5\Engine\Build\BatchFiles\Build.bat' `
  PolyArcStereoNDEditor Win64 Development `
  'D:\Claude\UE5\PolyArcStereoND\PolyArcStereoND.uproject' `
  -WaitMutex -FromMsBuild -MaxParallelActions=2
```

`-MaxParallelActions=2` needed on this machine due to pagefile constraints.

## Plugins enabled

- **nDisplay** (Engine/Plugins/Runtime/nDisplay) — production-ready, `IsBetaVersion: false` in 5.5.4
  - Includes sub-modules: DisplayCluster, DisplayClusterConfiguration, DisplayClusterProjection, DisplayClusterShaders
- **PolyArcStereoFX** (this project's custom plugin)
- ModelingToolsEditorMode (template default, kept)

## Next steps (in this project)

1. Build & launch editor (verify nDisplay enabled, no compile errors)
2. Add a `DisplayClusterRootActor` to a test level
3. Author nDisplay config asset: 4 viewports × 2 eyes, each viewport with `Simple` projection policy pointing at a `DisplayClusterScreenComponent` placed per arc geometry
4. Verify off-axis projection in editor preview (`HasPreviewMesh=true` so Simple policy supports it)
5. Implement M4 cross-talk PostProcess (2×2 matrix compute shader operating on each viewport's post-warp output)
6. Implement M5 column-interleave PostProcess (compute shader picking odd/even columns from L/R eye RT into final canvas)

## Related repos

- (archived) old multi-frustum attempt: <https://github.com/smallPotatoBoy/PolyArcStereo> + <https://github.com/smallPotatoBoy/Stereo3D544>
- Design doc on Feishu: <https://www.feishu.cn/docx/Kijydtwm8oGAPxxNfOicCnKengd>
- Handoff notes on Feishu: <https://eolm6fi2sn.feishu.cn/docx/HgKjdj3I4oCgOfxutfVcGwE4n2r>
