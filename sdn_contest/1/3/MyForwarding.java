package net.floodlightcontroller.myforwarding;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.util.AppCookie;
import net.floodlightcontroller.forwarding.Forwarding;
import net.floodlightcontroller.packet.Ethernet;
import net.floodlightcontroller.routing.IRoutingDecision;

import org.openflow.protocol.OFFlowMod;
import org.openflow.protocol.OFMatch;
import org.openflow.protocol.OFPacketIn;
import org.openflow.protocol.OFPacketOut;
import org.openflow.protocol.OFType;
import org.openflow.protocol.Wildcards;
import org.openflow.protocol.Wildcards.Flag;
import org.openflow.protocol.action.OFAction;
import org.openflow.protocol.action.OFActionDataLayerDestination;
import org.openflow.protocol.action.OFActionOutput;

public class MyForwarding extends Forwarding {

	int server = 0;
	int count = 0;
	long sw4_id = 4;
	long sw5_id = 5;
	int my_FULL_INT = (1 << 22) - 1;
	@Override
	public net.floodlightcontroller.core.IListener.Command processPacketInMessage(
			IOFSwitch sw, OFPacketIn pi, IRoutingDecision decision,
			FloodlightContext cntx) {
		// TODO Auto-generated method stub
		// Read in packet data headers by using OFMatch
		//System.out.println("FULL_INT = " + Integer.toBinaryString(Wildcards.FULL.getInt()));
		OFMatch match = new OFMatch();
		match.loadFromPacket(pi.getPacketData(), pi.getInPort());

		Ethernet eth = IFloodlightProviderService.bcStore.get(cntx,
				IFloodlightProviderService.CONTEXT_PI_PAYLOAD);

		long sid = sw.getId();

		if (sid == sw4_id) {
			if (eth.getSourceMAC().toString().equals("00:00:00:00:00:01")) {
				
				int src_port = match.getTransportSource() & 0xFFFF;
				int dst_port = match.getTransportDestination() & 0xFFFF;
				//System.out.println("src_port = " + src_port);
				//System.out.println("dst_port = " + dst_port);
				if (dst_port == 80) {
					count++;
					//if(count%2==0)
					{
						server = 1 - server;
					}
					String destinationMACAddress = "00:00:00:00:00:0"
							+ (server + 2);
					eth.setDestinationMACAddress(destinationMACAddress);
					OFFlowMod fm = (OFFlowMod) floodlightProvider
							.getOFMessageFactory().getMessage(OFType.FLOW_MOD);
					List<OFAction> actions = new ArrayList<OFAction>();
					OFAction action = new OFActionDataLayerDestination(eth
							.getDestinationMAC().toBytes());
					OFActionOutput action_2 = new OFActionOutput();
					action_2.setPort((short) 0xfffb);// FLOOD,actual only port 2
					actions.add(action);
					actions.add(action_2);
					long cookie = AppCookie.makeCookie(FORWARDING_APP_ID, 0);

					fm.setCookie(cookie)
							.setCommand(OFFlowMod.OFPFC_ADD)
							//.setHardTimeout((short) 10)
							// FLOWMOD_DEFAULT_HARD_TIMEOUT
							.setIdleTimeout((short) 5)
							// FLOWMOD_DEFAULT_IDLE_TIMEOUT
							.setBufferId(OFPacketOut.BUFFER_ID_NONE)
							.setMatch(match)
							.setActions(actions)
							.setLengthU(
									OFFlowMod.MINIMUM_LENGTH
											+ action.getLengthU()
											+ action_2.getLengthU()); // +OFActionOutput.MINIMUM_LENGTH);

					Wildcards wildcards = Wildcards.FULL
							.matchOn(Flag.DL_TYPE)
							.matchOn(Flag.NW_PROTO)
							.matchOn(Flag.NW_SRC)
							.matchOn(Flag.NW_DST)
							//.matchOn(Flag.TP_DST)
							//.matchOn(Flag.TP_SRC)
							.withNwDstMask(32)
							.withNwSrcMask(32)
							;
					fm.setMatch(match.clone().setWildcards(wildcards));
					try {
						if (log.isDebugEnabled()) {
							log.debug(
									"write drop flow-mod sw={} match={} flow-mod={}",
									new Object[] { sw, match, fm });
						}
						messageDamper.write(sw, fm, cntx);
						//doFlood(sw, pi, cntx);
						return net.floodlightcontroller.core.IListener.Command.CONTINUE;
					} catch (IOException e) {
						log.error("Failure writing drop flow mod", e);
					}
				}
				// un-tcp flow from pc1 to s2 or s3
				
				if(eth.getDestinationMAC().toString().equals("00:00:00:00:00:02") 
						||eth.getDestinationMAC().toString().equals("00:00:00:00:00:03")){
					this.myForward(sw, pi, cntx, (short)2);
				}else{
					
				}
				//this.doFlood(sw, pi, cntx);
			} else if(eth.getSourceMAC().toString().equals("00:00:00:00:00:02")
					|| eth.getSourceMAC().toString().equals("00:00:00:00:00:03")) {
				if(eth.getDestinationMAC().toString().equals("00:00:00:00:00:01")){
					this.myForward(sw, pi, cntx, (short)1);
				}else{
					super.processPacketInMessage(sw, pi, decision, cntx);
					return net.floodlightcontroller.core.IListener.Command.CONTINUE;
				}
				
			}else{
				super.processPacketInMessage(sw, pi, decision, cntx);
				return net.floodlightcontroller.core.IListener.Command.CONTINUE;
			}
		}else if(sid == sw5_id) {
			if(eth.getDestinationMAC().toString().equals("00:00:00:00:00:01")){
				this.myForward(sw, pi, cntx, (short)3);
			}else if(eth.getDestinationMAC().toString().equals("00:00:00:00:00:02")){
				this.myForward(sw, pi, cntx, (short)1);
			}else if(eth.getDestinationMAC().toString().equals("00:00:00:00:00:03")){
				this.myForward(sw, pi, cntx, (short)2);
			}else{
				//this.myForward(sw, pi, cntx, (short) 0xfffb);
				super.processPacketInMessage(sw, pi, decision, cntx);
				return net.floodlightcontroller.core.IListener.Command.CONTINUE;
			}
		}else{
			System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!sid = " + sid);
		}
		doFlood(sw, pi, cntx);
		//super.processPacketInMessage(sw, pi, decision, cntx);
		return net.floodlightcontroller.core.IListener.Command.CONTINUE;

	}
	
	public void myForward(IOFSwitch sw, OFPacketIn pi, FloodlightContext cntx,
			short outport) {
		OFMatch match = new OFMatch();
		match.loadFromPacket(pi.getPacketData(), pi.getInPort());

		OFFlowMod fm = (OFFlowMod) floodlightProvider.getOFMessageFactory()
				.getMessage(OFType.FLOW_MOD);
		List<OFAction> actions = new ArrayList<OFAction>();
		OFActionOutput action = new OFActionOutput();
		action.setPort(outport);
		actions.add(action);
		long cookie = AppCookie.makeCookie(FORWARDING_APP_ID, 0);

		fm.setCookie(cookie)
				.setCommand(OFFlowMod.OFPFC_ADD)
				.setHardTimeout((short) 36000)
				// FLOWMOD_DEFAULT_HARD_TIMEOUT
				.setIdleTimeout((short) 36000)
				// FLOWMOD_DEFAULT_IDLE_TIMEOUT
				.setBufferId(OFPacketOut.BUFFER_ID_NONE)
				.setMatch(match)
				.setActions(actions)
				.setLengthU(OFFlowMod.MINIMUM_LENGTH
						+ action.getLengthU()); // +OFActionOutput.MINIMUM_LENGTH);

		Wildcards wildcards = Wildcards.FULL
				.matchOn(Flag.DL_DST)
				.matchOn(Flag.DL_TYPE)
				.matchOn(Flag.NW_PROTO);
		if(sw.getId() == sw4_id){
			wildcards.matchOn(Flag.TP_SRC);
		}
		fm.setMatch(match.clone().setWildcards(wildcards));
		try {
			if (log.isDebugEnabled()) {
				log.debug("write drop flow-mod sw={} match={} flow-mod={}",
						new Object[] { sw, match, fm });
			}
			messageDamper.write(sw, fm, cntx);
			// doFlood(sw, pi, cntx);
		} catch (IOException e) {
			log.error("Failure writing drop flow mod", e);
		}
	}
}