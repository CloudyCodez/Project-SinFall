#pragma once

#include "GrandCrossRmiTypes.h"
namespace SevenDSDevelopmentC2S {


	//Message ID that replies to each RMI method. 
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinLevelUpBySkinMaterial = (::Proud::RmiID)(10080+1);
               
    static const ::Proud::RmiID Rmi_Reserved02 = (::Proud::RmiID)(10080+2);
               
    static const ::Proud::RmiID Rmi_Reserved03 = (::Proud::RmiID)(10080+3);
               
    static const ::Proud::RmiID Rmi_Reserved04 = (::Proud::RmiID)(10080+4);
               
    static const ::Proud::RmiID Rmi_CG_RequestSkinAwaken = (::Proud::RmiID)(10080+5);

	// List that has RMI ID.
	extern ::Proud::RmiID g_RmiIDList[];
	// RmiID List Count
	extern int g_RmiIDListCount;

}


 

// Forward declarations


// Declarations



