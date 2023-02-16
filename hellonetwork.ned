//
// Copyright (C) 2017 Christoph Sommer <sommer@ccs-labs.org>
//
// Documentation for these modules is at http://veins.car2x.org/
//
// SPDX-License-Identifier: GPL-2.0-or-later
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//


import inet.physicallayer.wireless.common.contract.packetlevel.IAnalogModel;
import inet.showcases.wireless.power.PowerConsumptionShowcase;
import inet.showcases.mobility.basic.BasicMobilityShowcase;

//import inet.showcases.mobility.spatial.SpatialMobilityShowcase;
//import inet.node.inet.AdhocHost;
import inet.node.inet.WirelessHost;
import inet.node.contract.INetworkNode;
//import inet.physicallayer.wireless.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
//import inet.node.inet.StandardHost;
//import inet.physicallayer.wireless.ieee80211.packetlevel.Ieee80211RadioMedium;
import org.car2x.veins.subprojects.veins_inet.VeinsInetCar;
//import inet.physicallayer*.ieee80211.packetlevel.Ieee80211DimensionalRadioMedium;
import inet.physicallayer.wireless.unitdisk.UnitDiskRadioMedium;    //represents the shared physical medium where all of our communication takes place.
																	// Responisble for signal propagation, attrition, interference, other physical phenomena
import inet.physicallayer.wireless.common.contract.packetlevel.IRadioMedium;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;   //assigns all host addresses 
import inet.visualizer.common.IntegratedVisualizer;

//import org.car2x.veins.nodes.RSU;
//import org.car2x.veins.nodes.Scenario;
import org.car2x.veins.subprojects.veins_inet.examples.veins_inet.Scenario;




network hellonetwork extends Scenario
{
    parameters:
        int numDrones;
        @display("bgb=620,476");

    types:
        channel myChannel extends ned.DelayChannel
        {
            delay = 100ms;
        }

    submodules:
        //rsu[4]: VeinsInetRSU {
            //@display("p=150,140;b=10,10,oval;r=40");
        //    @display("p=150,140;b=10,10,rect;r=30;i=veins/sign/yellowdiamond;is=vs");
        //}

//        visualizer: IntegratedVisualizer {
  //          @display("p=43,98");
    //    }

        drone[numDrones]: <default("WirelessHost")> like INetworkNode {
            @display("i=misc/drone");
        }

        GCS: <default("WirelessHost")> like INetworkNode {
            @display("p=300,360;i=device/antennatower;is=vl");
        }





        radioMedium: <default("UnitDiskRadioMedium")> like IRadioMedium {
            parameters:
                @display("p=43,232");
        }


        configurator: Ipv4NetworkConfigurator {
            parameters:
                @display("p=43,167");
        }



}







