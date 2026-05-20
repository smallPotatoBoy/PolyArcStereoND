// Copyright PolyArcStereo Team. All Rights Reserved.

#include "PolyArcStereoFXModule.h"

DEFINE_LOG_CATEGORY(LogPolyArcStereoFX);

#define LOCTEXT_NAMESPACE "FPolyArcStereoFXModule"

void FPolyArcStereoFXModule::StartupModule()
{
	UE_LOG(LogPolyArcStereoFX, Log, TEXT("PolyArcStereoFX module started"));
	// TODO: 注册 IDisplayClusterPostProcessFactory 子类，暴露
	//   PolyArcStereo.CrossTalk     (M4)
	//   PolyArcStereo.ColumnInterleave (M5)
}

void FPolyArcStereoFXModule::ShutdownModule()
{
	UE_LOG(LogPolyArcStereoFX, Log, TEXT("PolyArcStereoFX module shutting down"));
	// TODO: 反注册工厂
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FPolyArcStereoFXModule, PolyArcStereoFX)
