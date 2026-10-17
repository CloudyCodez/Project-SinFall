#pragma once

#include "GrandCrossRmiTypes.h"
namespace SevenDSQuestS2C {


	//Message ID that replies to each RMI method. 
               
    static const ::Proud::RmiID Rmi_CG_RequestQuestStartOK = (::Proud::RmiID)(14184+1);
               
    static const ::Proud::RmiID Rmi_CG_RequestQuestProgressOK = (::Proud::RmiID)(14184+2);
               
    static const ::Proud::RmiID Rmi_CG_RequestQuestClearOK = (::Proud::RmiID)(14184+3);

	// List that has RMI ID.
	extern ::Proud::RmiID g_RmiIDList[];
	// RmiID List Count
	extern int g_RmiIDListCount;

}


 

// Forward declarations


// Declarations



