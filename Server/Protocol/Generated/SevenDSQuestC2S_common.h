#pragma once

#include "GrandCrossRmiTypes.h"
namespace SevenDSQuestC2S {


	//Message ID that replies to each RMI method. 
               
    static const ::Proud::RmiID Rmi_CG_RequestQuestStart = (::Proud::RmiID)(10800+1);
               
    static const ::Proud::RmiID Rmi_CG_RequestQuestProgress = (::Proud::RmiID)(10800+2);
               
    static const ::Proud::RmiID Rmi_CG_RequestQuestClear = (::Proud::RmiID)(10800+3);

	// List that has RMI ID.
	extern ::Proud::RmiID g_RmiIDList[];
	// RmiID List Count
	extern int g_RmiIDListCount;

}


 

// Forward declarations


// Declarations



