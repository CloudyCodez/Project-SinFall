#pragma once

#include "GrandCrossRmiTypes.h"
namespace SevenDSBulkGrowthC2S {


	//Message ID that replies to each RMI method. 
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinAwakenAtOnce = (::Proud::RmiID)(13571+1);
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinTranscendAtOnce = (::Proud::RmiID)(13571+2);
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinEvolutionAtOnce = (::Proud::RmiID)(13571+3);
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinOverEvolutionAtOnce = (::Proud::RmiID)(13571+4);
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinExclusiveSkillAtOnce = (::Proud::RmiID)(13571+5);

	// List that has RMI ID.
	extern ::Proud::RmiID g_RmiIDList[];
	// RmiID List Count
	extern int g_RmiIDListCount;

}


 

// Forward declarations


// Declarations



