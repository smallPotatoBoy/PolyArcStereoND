// Copyright PolyArcStereo Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

DECLARE_LOG_CATEGORY_EXTERN(LogPolyArcStereoFX, Log, All);

/**
 * PolyArcStereoFX: nDisplay PostProcess 扩展，覆盖 M4（Cross-Talk 矩阵补偿）
 * 与 M5（隔列交错最终合成）。
 *
 * 模块在 PostEngineInit 阶段注册 IDisplayClusterPostProcessFactory，
 * 让 nDisplay 配置里能用 "PolyArcStereo.CrossTalk" 和 "PolyArcStereo.ColumnInterleave"
 * 两类 PostProcess 名称。
 */
class FPolyArcStereoFXModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
