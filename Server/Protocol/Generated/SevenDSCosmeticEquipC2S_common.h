#pragma once

#include "GrandCrossRmiTypes.h"
namespace SevenDSCosmeticEquipC2S {


	//Message ID that replies to each RMI method. 
               
    static const ::Proud::RmiID Rmi_CG_RequestCostumeEquip = (::Proud::RmiID)(10092+1);
               
    static const ::Proud::RmiID Rmi_CG_RequestCostumeUnEquip = (::Proud::RmiID)(10092+2);

	// List that has RMI ID.
	extern ::Proud::RmiID g_RmiIDList[];
	// RmiID List Count
	extern int g_RmiIDListCount;

}


 

// Forward declarations


// Declarations



