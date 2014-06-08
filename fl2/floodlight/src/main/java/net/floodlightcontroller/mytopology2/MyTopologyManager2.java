/**
 *    Copyright 2013, Big Switch Networks, Inc.
 *
 *    Licensed under the Apache License, Version 2.0 (the "License"); you may
 *    not use this file except in compliance with the License. You may obtain
 *    a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 *    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 *    License for the specific language governing permissions and limitations
 *    under the License.
 **/

package net.floodlightcontroller.mytopology2;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.annotations.LogMessageCategory;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightService;
import net.floodlightcontroller.routing.Link;
import net.floodlightcontroller.routing.Route;
import net.floodlightcontroller.topology.ITopologyListener;
import net.floodlightcontroller.topology.NodePortTuple;
import net.floodlightcontroller.topology.TopologyInstance;
import net.floodlightcontroller.topology.TopologyManager;

import org.openflow.protocol.OFMessage;
import org.openflow.protocol.OFPacketIn;
import org.openflow.protocol.OFType;

/**
 * Topology manager is responsible for maintaining the controller's notion of
 * the network graph, as well as implementing tools for finding routes through
 * the topology.
 */
@LogMessageCategory("Network Topology")
public class MyTopologyManager2 extends TopologyManager {

	public MyTopologyManager2() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public int getTopologyComputeInterval() {
		// TODO Auto-generated method stub
		return super.getTopologyComputeInterval();
	}

	@Override
	public void setTopologyComputeInterval(int time_ms) {
		// TODO Auto-generated method stub
		super.setTopologyComputeInterval(time_ms);
	}

	@Override
	protected void handleMiscellaneousPeriodicEvents() {
		// TODO Auto-generated method stub
		super.handleMiscellaneousPeriodicEvents();
	}

	@Override
	public boolean updateTopology() {
		// TODO Auto-generated method stub
		return super.updateTopology();
	}

	@Override
	public void linkDiscoveryUpdate(List<LDUpdate> updateList) {
		// TODO Auto-generated method stub
		super.linkDiscoveryUpdate(updateList);
	}

	@Override
	public void linkDiscoveryUpdate(LDUpdate update) {
		// TODO Auto-generated method stub
		super.linkDiscoveryUpdate(update);
	}

	@Override
	public Date getLastUpdateTime() {
		// TODO Auto-generated method stub
		return super.getLastUpdateTime();
	}

	@Override
	public void addListener(ITopologyListener listener) {
		// TODO Auto-generated method stub
		super.addListener(listener);
	}

	@Override
	public boolean isAttachmentPointPort(long switchid, short port) {
		// TODO Auto-generated method stub
		return super.isAttachmentPointPort(switchid, port);
	}

	@Override
	public boolean isAttachmentPointPort(long switchid, short port,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.isAttachmentPointPort(switchid, port, tunnelEnabled);
	}

	@Override
	public long getOpenflowDomainId(long switchId) {
		// TODO Auto-generated method stub
		return super.getOpenflowDomainId(switchId);
	}

	@Override
	public long getOpenflowDomainId(long switchId, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getOpenflowDomainId(switchId, tunnelEnabled);
	}

	@Override
	public long getL2DomainId(long switchId) {
		// TODO Auto-generated method stub
		return super.getL2DomainId(switchId);
	}

	@Override
	public long getL2DomainId(long switchId, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getL2DomainId(switchId, tunnelEnabled);
	}

	@Override
	public boolean inSameOpenflowDomain(long switch1, long switch2) {
		// TODO Auto-generated method stub
		return super.inSameOpenflowDomain(switch1, switch2);
	}

	@Override
	public boolean inSameOpenflowDomain(long switch1, long switch2,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.inSameOpenflowDomain(switch1, switch2, tunnelEnabled);
	}

	@Override
	public boolean isAllowed(long sw, short portId) {
		// TODO Auto-generated method stub
		return super.isAllowed(sw, portId);
	}

	@Override
	public boolean isAllowed(long sw, short portId, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.isAllowed(sw, portId, tunnelEnabled);
	}

	@Override
	public boolean isIncomingBroadcastAllowed(long sw, short portId) {
		// TODO Auto-generated method stub
		return super.isIncomingBroadcastAllowed(sw, portId);
	}

	@Override
	public boolean isIncomingBroadcastAllowed(long sw, short portId,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.isIncomingBroadcastAllowed(sw, portId, tunnelEnabled);
	}

	@Override
	public Set<Short> getPortsWithLinks(long sw) {
		// TODO Auto-generated method stub
		return super.getPortsWithLinks(sw);
	}

	@Override
	public Set<Short> getPortsWithLinks(long sw, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getPortsWithLinks(sw, tunnelEnabled);
	}

	@Override
	public Set<Short> getBroadcastPorts(long targetSw, long src, short srcPort) {
		// TODO Auto-generated method stub
		return super.getBroadcastPorts(targetSw, src, srcPort);
	}

	@Override
	public Set<Short> getBroadcastPorts(long targetSw, long src, short srcPort,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getBroadcastPorts(targetSw, src, srcPort, tunnelEnabled);
	}

	@Override
	public NodePortTuple getOutgoingSwitchPort(long src, short srcPort,
			long dst, short dstPort) {
		// TODO Auto-generated method stub
		return super.getOutgoingSwitchPort(src, srcPort, dst, dstPort);
	}

	@Override
	public NodePortTuple getOutgoingSwitchPort(long src, short srcPort,
			long dst, short dstPort, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getOutgoingSwitchPort(src, srcPort, dst, dstPort,
				tunnelEnabled);
	}

	@Override
	public NodePortTuple getIncomingSwitchPort(long src, short srcPort,
			long dst, short dstPort) {
		// TODO Auto-generated method stub
		return super.getIncomingSwitchPort(src, srcPort, dst, dstPort);
	}

	@Override
	public NodePortTuple getIncomingSwitchPort(long src, short srcPort,
			long dst, short dstPort, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getIncomingSwitchPort(src, srcPort, dst, dstPort,
				tunnelEnabled);
	}

	@Override
	public boolean isInSameBroadcastDomain(long s1, short p1, long s2, short p2) {
		// TODO Auto-generated method stub
		return super.isInSameBroadcastDomain(s1, p1, s2, p2);
	}

	@Override
	public boolean isInSameBroadcastDomain(long s1, short p1, long s2,
			short p2, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.isInSameBroadcastDomain(s1, p1, s2, p2, tunnelEnabled);
	}

	@Override
	public boolean isBroadcastDomainPort(long sw, short port) {
		// TODO Auto-generated method stub
		return super.isBroadcastDomainPort(sw, port);
	}

	@Override
	public boolean isBroadcastDomainPort(long sw, short port,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.isBroadcastDomainPort(sw, port, tunnelEnabled);
	}

	@Override
	public boolean isConsistent(long oldSw, short oldPort, long newSw,
			short newPort) {
		// TODO Auto-generated method stub
		return super.isConsistent(oldSw, oldPort, newSw, newPort);
	}

	@Override
	public boolean isConsistent(long oldSw, short oldPort, long newSw,
			short newPort, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super
				.isConsistent(oldSw, oldPort, newSw, newPort, tunnelEnabled);
	}

	@Override
	public boolean inSameL2Domain(long switch1, long switch2) {
		// TODO Auto-generated method stub
		return super.inSameL2Domain(switch1, switch2);
	}

	@Override
	public boolean inSameL2Domain(long switch1, long switch2,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.inSameL2Domain(switch1, switch2, tunnelEnabled);
	}

	@Override
	public NodePortTuple getAllowedOutgoingBroadcastPort(long src,
			short srcPort, long dst, short dstPort) {
		// TODO Auto-generated method stub
		return super
				.getAllowedOutgoingBroadcastPort(src, srcPort, dst, dstPort);
	}

	@Override
	public NodePortTuple getAllowedOutgoingBroadcastPort(long src,
			short srcPort, long dst, short dstPort, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getAllowedOutgoingBroadcastPort(src, srcPort, dst,
				dstPort, tunnelEnabled);
	}

	@Override
	public NodePortTuple getAllowedIncomingBroadcastPort(long src, short srcPort) {
		// TODO Auto-generated method stub
		return super.getAllowedIncomingBroadcastPort(src, srcPort);
	}

	@Override
	public NodePortTuple getAllowedIncomingBroadcastPort(long src,
			short srcPort, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getAllowedIncomingBroadcastPort(src, srcPort,
				tunnelEnabled);
	}

	@Override
	public Set<Long> getSwitchesInOpenflowDomain(long switchDPID) {
		// TODO Auto-generated method stub
		return super.getSwitchesInOpenflowDomain(switchDPID);
	}

	@Override
	public Set<Long> getSwitchesInOpenflowDomain(long switchDPID,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getSwitchesInOpenflowDomain(switchDPID, tunnelEnabled);
	}

	@Override
	public Set<NodePortTuple> getBroadcastDomainPorts() {
		// TODO Auto-generated method stub
		return super.getBroadcastDomainPorts();
	}

	@Override
	public Set<NodePortTuple> getTunnelPorts() {
		// TODO Auto-generated method stub
		return super.getTunnelPorts();
	}

	@Override
	public Set<NodePortTuple> getBlockedPorts() {
		// TODO Auto-generated method stub
		return super.getBlockedPorts();
	}

	@Override
	public Route getRoute(long src, long dst, long cookie) {
		// TODO Auto-generated method stub
		return super.getRoute(src, dst, cookie);
	}

	@Override
	public Route getRoute(long src, long dst, long cookie, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getRoute(src, dst, cookie, tunnelEnabled);
	}

	@Override
	public Route getRoute(long src, short srcPort, long dst, short dstPort,
			long cookie) {
		// TODO Auto-generated method stub
		return super.getRoute(src, srcPort, dst, dstPort, cookie);
	}

	@Override
	public Route getRoute(long src, short srcPort, long dst, short dstPort,
			long cookie, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super
				.getRoute(src, srcPort, dst, dstPort, cookie, tunnelEnabled);
	}

	@Override
	public boolean routeExists(long src, long dst) {
		// TODO Auto-generated method stub
		return super.routeExists(src, dst);
	}

	@Override
	public boolean routeExists(long src, long dst, boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.routeExists(src, dst, tunnelEnabled);
	}

	@Override
	public ArrayList<Route> getRoutes(long srcDpid, long dstDpid,
			boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getRoutes(srcDpid, dstDpid, tunnelEnabled);
	}

	@Override
	public String getName() {
		// TODO Auto-generated method stub
		return super.getName();
	}

	@Override
	public boolean isCallbackOrderingPrereq(OFType type, String name) {
		// TODO Auto-generated method stub
		return super.isCallbackOrderingPrereq(type, name);
	}

	@Override
	public boolean isCallbackOrderingPostreq(OFType type, String name) {
		// TODO Auto-generated method stub
		return super.isCallbackOrderingPostreq(type, name);
	}

	@Override
	public net.floodlightcontroller.core.IListener.Command receive(
			IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
		// TODO Auto-generated method stub
		return super.receive(sw, msg, cntx);
	}

	@Override
	public Collection<Class<? extends IFloodlightService>> getModuleServices() {
		// TODO Auto-generated method stub
		return super.getModuleServices();
	}

	@Override
	public Map<Class<? extends IFloodlightService>, IFloodlightService> getServiceImpls() {
		// TODO Auto-generated method stub
		return super.getServiceImpls();
	}

	@Override
	public Collection<Class<? extends IFloodlightService>> getModuleDependencies() {
		// TODO Auto-generated method stub
		return super.getModuleDependencies();
	}

	@Override
	public void init(FloodlightModuleContext context)
			throws FloodlightModuleException {
		// TODO Auto-generated method stub
		super.init(context);
	}

	@Override
	protected void registerTopologyDebugEvents()
			throws FloodlightModuleException {
		// TODO Auto-generated method stub
		super.registerTopologyDebugEvents();
	}

	@Override
	public void startUp(FloodlightModuleContext context) {
		// TODO Auto-generated method stub
		super.startUp(context);
	}

	@Override
	protected void addRestletRoutable() {
		// TODO Auto-generated method stub
		super.addRestletRoutable();
	}

	@Override
	protected net.floodlightcontroller.core.IListener.Command dropFilter(
			long sw, OFPacketIn pi, FloodlightContext cntx) {
		// TODO Auto-generated method stub
		return super.dropFilter(sw, pi, cntx);
	}

	@Override
	public void doMultiActionPacketOut(byte[] packetData, IOFSwitch sw,
			Set<Short> ports, FloodlightContext cntx) {
		// TODO Auto-generated method stub
		super.doMultiActionPacketOut(packetData, sw, ports, cntx);
	}

	@Override
	protected Set<Short> getPortsToEliminateForBDDP(long sid) {
		// TODO Auto-generated method stub
		return super.getPortsToEliminateForBDDP(sid);
	}

	@Override
	protected void doFloodBDDP(long pinSwitch, OFPacketIn pi,
			FloodlightContext cntx) {
		// TODO Auto-generated method stub
		super.doFloodBDDP(pinSwitch, pi, cntx);
	}

	@Override
	protected net.floodlightcontroller.core.IListener.Command processPacketInMessage(
			IOFSwitch sw, OFPacketIn pi, FloodlightContext cntx) {
		// TODO Auto-generated method stub
		return super.processPacketInMessage(sw, pi, cntx);
	}

	@Override
	public List<LDUpdate> applyUpdates() {
		// TODO Auto-generated method stub
		return super.applyUpdates();
	}

	@Override
	protected void addOrUpdateSwitch(long sw) {
		// TODO Auto-generated method stub
		super.addOrUpdateSwitch(sw);
	}

	@Override
	public void addTunnelPort(long sw, short port) {
		// TODO Auto-generated method stub
		super.addTunnelPort(sw, port);
	}

	@Override
	public void removeTunnelPort(long sw, short port) {
		// TODO Auto-generated method stub
		super.removeTunnelPort(sw, port);
	}

	@Override
	public boolean createNewInstance() {
		// TODO Auto-generated method stub
		return createNewInstance("internal");
	}

	@Override
	protected boolean createNewInstance(String reason) {
		Set<NodePortTuple> blockedPorts = new HashSet<NodePortTuple>();

		if (!linksUpdated)
			return false;

		Map<NodePortTuple, Set<Link>> openflowLinks;
		openflowLinks = new HashMap<NodePortTuple, Set<Link>>();
		Set<NodePortTuple> nptList = switchPortLinks.keySet();

		if (nptList != null) {
			for (NodePortTuple npt : nptList) {
				Set<Link> linkSet = switchPortLinks.get(npt);
				if (linkSet == null)
					continue;
				openflowLinks.put(npt, new HashSet<Link>(linkSet));
			}
		}

		// Identify all broadcast domain ports.
		// Mark any port that has inconsistent set of links
		// as broadcast domain ports as well.
		Set<NodePortTuple> broadcastDomainPorts = identifyBroadcastDomainPorts();

		// Remove all links incident on broadcast domain ports.
		for (NodePortTuple npt : broadcastDomainPorts) {
			if (switchPortLinks.get(npt) == null)
				continue;
			for (Link link : switchPortLinks.get(npt)) {
				removeLinkFromStructure(openflowLinks, link);
			}
		}

		// Remove all tunnel links.
		for (NodePortTuple npt : tunnelPorts) {
			if (switchPortLinks.get(npt) == null)
				continue;
			for (Link link : switchPortLinks.get(npt)) {
				removeLinkFromStructure(openflowLinks, link);
			}
		}

		MyTopologyInstance2 nt = new MyTopologyInstance2(switchPorts,
				blockedPorts, openflowLinks, broadcastDomainPorts, tunnelPorts);
		nt.compute();
		// We set the instances with and without tunnels to be identical.
		// If needed, we may compute them differently.
		currentInstance = nt;
		currentInstanceWithoutTunnels = nt;

		TopologyEventInfo topologyInfo = new TopologyEventInfo(0, nt
				.getClusters().size(),
				new HashMap<Long, List<NodePortTuple>>(), 0);
		evTopology
				.updateEventWithFlush(new TopologyEvent(reason, topologyInfo));
		return true;
	}

	//////////private in super class
	/**
	 * Delete the given link from the data strucure. Returns true if the link
	 * was deleted.
	 * 
	 * @param s
	 * @param l
	 * @return
	 */
	private boolean removeLinkFromStructure(Map<NodePortTuple, Set<Link>> s,
			Link l) {

		boolean result1 = false, result2 = false;
		NodePortTuple n1 = new NodePortTuple(l.getSrc(), l.getSrcPort());
		NodePortTuple n2 = new NodePortTuple(l.getDst(), l.getDstPort());

		if (s.get(n1) != null) {
			result1 = s.get(n1).remove(l);
			if (s.get(n1).isEmpty())
				s.remove(n1);
		}
		if (s.get(n2) != null) {
			result2 = s.get(n2).remove(l);
			if (s.get(n2).isEmpty())
				s.remove(n2);
		}
		return result1 || result2;
	}

	@Override
	protected Set<NodePortTuple> identifyBroadcastDomainPorts() {
		// TODO Auto-generated method stub
		return super.identifyBroadcastDomainPorts();
	}

	@Override
	public void informListeners(List<LDUpdate> linkUpdates) {
		// TODO Auto-generated method stub
		super.informListeners(linkUpdates);
	}

	@Override
	public void addSwitch(long sid) {
		// TODO Auto-generated method stub
		super.addSwitch(sid);
	}

	@Override
	public void removeSwitch(long sid) {
		// TODO Auto-generated method stub
		super.removeSwitch(sid);
	}

	@Override
	protected void addOrUpdateTunnelLink(long srcId, short srcPort, long dstId,
			short dstPort) {
		// TODO Auto-generated method stub
		super.addOrUpdateTunnelLink(srcId, srcPort, dstId, dstPort);
	}

	@Override
	public void addOrUpdateLink(long srcId, short srcPort, long dstId,
			short dstPort, LinkType type) {
		// TODO Auto-generated method stub
		super.addOrUpdateLink(srcId, srcPort, dstId, dstPort, type);
	}

	@Override
	public void removeLink(Link link) {
		// TODO Auto-generated method stub
		super.removeLink(link);
	}

	@Override
	public void removeLink(long srcId, short srcPort, long dstId, short dstPort) {
		// TODO Auto-generated method stub
		super.removeLink(srcId, srcPort, dstId, dstPort);
	}

	@Override
	public void clear() {
		// TODO Auto-generated method stub
		super.clear();
	}

	@Override
	public void clearCurrentTopology() {
		// TODO Auto-generated method stub
		super.clearCurrentTopology();
	}

	@Override
	public Map<Long, Set<Short>> getSwitchPorts() {
		// TODO Auto-generated method stub
		return super.getSwitchPorts();
	}

	@Override
	public Map<NodePortTuple, Set<Link>> getSwitchPortLinks() {
		// TODO Auto-generated method stub
		return super.getSwitchPortLinks();
	}

	@Override
	public Map<NodePortTuple, Set<Link>> getPortBroadcastDomainLinks() {
		// TODO Auto-generated method stub
		return super.getPortBroadcastDomainLinks();
	}

	@Override
	public TopologyInstance getCurrentInstance(boolean tunnelEnabled) {
		// TODO Auto-generated method stub
		return super.getCurrentInstance(tunnelEnabled);
	}

	@Override
	public TopologyInstance getCurrentInstance() {
		// TODO Auto-generated method stub
		return super.getCurrentInstance();
	}

	@Override
	public Set<Short> getPorts(long sw) {
		// TODO Auto-generated method stub
		return super.getPorts(sw);
	}

}
