// Copyright PolyArcStereo Team. All Rights Reserved.

using UnrealBuildTool;

public class PolyArcStereoFX : ModuleRules
{
	public PolyArcStereoFX(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicIncludePaths.AddRange(new string[] { });
		PrivateIncludePaths.AddRange(new string[] { });

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
			"RHI",
			"RenderCore",
			"Renderer",
			"Projects",
			// nDisplay public modules
			"DisplayCluster",
			"DisplayClusterConfiguration",
			"DisplayClusterShaders",
		});

		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"Slate",
			"SlateCore",
		});
	}
}
