package net.floodlightcontroller.mytopology2;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

import com.google.common.cache.LoadingCache;

import net.floodlightcontroller.routing.BroadcastTree;
import net.floodlightcontroller.routing.Link;
import net.floodlightcontroller.routing.Route;
import net.floodlightcontroller.routing.RouteId;
import net.floodlightcontroller.servicechaining.ServiceChain;
import net.floodlightcontroller.topology.Cluster;
import net.floodlightcontroller.topology.NodePortTuple;
import net.floodlightcontroller.topology.TopologyInstance;

public class MyTopologyInstance2 extends TopologyInstance {

	public MyTopologyInstance2() {
		super();
		// TODO Auto-generated constructor stub
	}

	public MyTopologyInstance2(Map<Long, Set<Short>> switchPorts,
			Map<NodePortTuple, Set<Link>> switchPortLinks,
			Set<NodePortTuple> broadcastDomainPorts) {
		super(switchPorts, switchPortLinks, broadcastDomainPorts);
		// TODO Auto-generated constructor stub
	}

	public MyTopologyInstance2(Map<Long, Set<Short>> switchPorts,
			Set<NodePortTuple> blockedPorts,
			Map<NodePortTuple, Set<Link>> switchPortLinks,
			Set<NodePortTuple> broadcastDomainPorts,
			Set<NodePortTuple> tunnelPorts) {
		super(switchPorts, blockedPorts, switchPortLinks, broadcastDomainPorts,
				tunnelPorts);
		// TODO Auto-generated constructor stub
	}

	@Override
	protected Set<Cluster> getClusters() {
		// TODO Auto-generated method stub
		return super.getClusters();
	}

	@Override
	public void compute() {
		// Step 1: Compute clusters ignoring broadcast domain links
		// Create nodes for clusters in the higher level topology
		// Must ignore blocked links.
		identifyOpenflowDomains();

		// Step 1.1: Add links to clusters
		// Avoid adding blocked links to clusters
		addLinksToOpenflowDomains();

		// Step 2. Compute shortest path trees in each cluster for
		// unicast routing. The trees are rooted at the destination.
		// Cost for tunnel links and direct links are the same.
		calculateShortestPathTreeInClusters();

		// Step 3. Compute broadcast tree in each cluster.
		// Cost for tunnel links are high to discourage use of
		// tunnel links. The cost is set to the number of nodes
		// in the cluster + 1, to use as minimum number of
		// clusters as possible.
		calculateBroadcastNodePortsInClusters();

		// Step 4. print topology.
		printTopology();
	}

	@Override
	public void printTopology() {
		// TODO Auto-generated method stub
		super.printTopology();
	}

	@Override
	protected void addLinksToOpenflowDomains() {
		// TODO Auto-generated method stub
		super.addLinksToOpenflowDomains();
	}

	@Override
	public void identifyOpenflowDomains() {
		// TODO Auto-generated method stub
		super.identifyOpenflowDomains();
	}

	@Override
	public Set<NodePortTuple> getBlockedPorts() {
		// TODO Auto-generated method stub
		return super.getBlockedPorts();
	}

	@Override
	protected Set<Link> getBlockedLinks() {
		// TODO Auto-generated method stub
		return super.getBlockedLinks();
	}

	@Override
	protected boolean isBlockedLink(Link l) {
		// TODO Auto-generated method stub
		return super.isBlockedLink(l);
	}

	@Override
	protected boolean isBlockedPort(NodePortTuple npt) {
		// TODO Auto-generated method stub
		return super.isBlockedPort(npt);
	}

	@Override
	protected boolean isTunnelPort(NodePortTuple npt) {
		// TODO Auto-generated method stub
		return super.isTunnelPort(npt);
	}

	@Override
	protected boolean isTunnelLink(Link l) {
		// TODO Auto-generated method stub
		return super.isTunnelLink(l);
	}

	@Override
	public boolean isBroadcastDomainLink(Link l) {
		// TODO Auto-generated method stub
		return super.isBroadcastDomainLink(l);
	}

	@Override
	public boolean isBroadcastDomainPort(NodePortTuple npt) {
		// TODO Auto-generated method stub
		return super.isBroadcastDomainPort(npt);
	}

	@Override
	protected BroadcastTree dijkstra(Cluster c, Long root,
			Map<Link, Integer> linkCost, boolean isDstRooted) {
		HashMap<Long, Link> nexthoplinks = new HashMap<Long, Link>();
		// HashMap<Long, Long> nexthopnodes = new HashMap<Long, Long>();
		HashMap<Long, Integer> cost = new HashMap<Long, Integer>();
		int w;

		for (Long node : c.getLinks().keySet()) {
			nexthoplinks.put(node, null);
			// nexthopnodes.put(node, null);
			cost.put(node, MAX_PATH_WEIGHT);
		}

		HashMap<Long, Boolean> seen = new HashMap<Long, Boolean>();
		PriorityQueue<NodeDist> nodeq = new PriorityQueue<NodeDist>();
		nodeq.add(new NodeDist(root, 0));
		cost.put(root, 0);
		while (nodeq.peek() != null) {
			NodeDist n = nodeq.poll();
			Long cnode = n.getNode();
			int cdist = n.getDist();
			if (cdist >= MAX_PATH_WEIGHT)
				break;
			if (seen.containsKey(cnode))
				continue;
			seen.put(cnode, true);

			for (Link link : c.getLinks().get(cnode)) {
				Long neighbor;

				if (isDstRooted == true)
					neighbor = link.getSrc();
				else
					neighbor = link.getDst();

				// links directed toward cnode will result in this condition
				if (neighbor.equals(cnode))
					continue;

				if (seen.containsKey(neighbor))
					continue;

				if (linkCost == null || linkCost.get(link) == null)
					w = 1;
				else
					w = linkCost.get(link);

				int ndist = cdist + w; // the weight of the link, always 1 in
										// current version of floodlight.
				if (ndist < cost.get(neighbor)) {
					cost.put(neighbor, ndist);
					nexthoplinks.put(neighbor, link);
					// nexthopnodes.put(neighbor, cnode);
					NodeDist ndTemp = new NodeDist(neighbor, ndist);
					// Remove an object that's already in there.
					// Note that the comparison is based on only the node id,
					// and not node id and distance.
					nodeq.remove(ndTemp);
					// add the current object to the queue.
					nodeq.add(ndTemp);
				}
			}
		}

		BroadcastTree ret = new BroadcastTree(nexthoplinks, cost);
		return ret;
	}

	@Override
	protected void calculateShortestPathTreeInClusters() {
		System.out
				.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!calculateShortestPathTreeInClusters");
		// System.out.println("********************************************************");
		// System.out.println("pathcache.size::::::"+this.pathcache.size());
		// MyFlowList.getInstance(switchPortLinks);
		pathcache.invalidateAll();
		// System.out.println("!!!!!!!arter inval!!!!!!!pathcache.size::::::"+this.pathcache.size());
		destinationRootedTrees.clear();

		// create linkCost-------------------------------------
		// Map<Link, Integer> linkCost = new HashMap<Link, Integer>();
		// int tunnel_weight = switchPorts.size() + 1;
		//
		// for (NodePortTuple npt : tunnelPorts) {
		// if (switchPortLinks.get(npt) == null)
		// continue;
		// for (Link link : switchPortLinks.get(npt)) {
		// if (link == null)
		// continue;
		// linkCost.put(link, tunnel_weight);
		// }
		// }
		// /------------------------------------------------------
		// /#####################################################################
		Map<Link, Integer> linkCost = MyFlowList.getInstance().getLinkCost();
		// /#####################################################################
		for (Cluster c : clusters) {
			for (Long node : c.getLinks().keySet()) {
				BroadcastTree tree = dijkstra(c, node, linkCost, true);
				destinationRootedTrees.put(node, tree);
			}
		}
		// ################################################################################
		// for(Long dst:destinationRootedTrees.keySet()){
		// //Map<Long, BroadcastTree>
		// System.out.println("dst:"+dst);
		// BroadcastTree bt = destinationRootedTrees.get(dst);
		// for(Long src:bt.getLinks().keySet()){
		// System.out.println("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
		// System.out.println("from "+src +
		// " to "+dst+",cost:"+bt.getCosts().get(src));
		// System.out.print(src);
		// Link tmp_link = bt.getLinks().get(src);
		// if(tmp_link == null) {
		// System.out.println();
		// continue;
		// }
		// Long tmp_dst = tmp_link.getDst();
		// while(tmp_dst!=dst){
		// System.out.print(">>"+tmp_dst);
		// tmp_link = bt.getLinks().get(tmp_dst);
		// tmp_dst = tmp_link.getDst();
		// }
		// System.out.println(">>"+dst);
		// }
		// }
		// ################################################################################
	}

	@Override
	protected void calculateBroadcastTreeInClusters() {
		// TODO Auto-generated method stub
		super.calculateBroadcastTreeInClusters();
	}

	@Override
	protected void calculateBroadcastNodePortsInClusters() {
		// TODO Auto-generated method stub
		super.calculateBroadcastNodePortsInClusters();
	}

	@Override
	protected Route buildroute(RouteId id) {
		// TODO Auto-generated method stub
		return super.buildroute(id);
	}

	@Override
	protected int getCost(long srcId, long dstId) {
		// TODO Auto-generated method stub
		return super.getCost(srcId, dstId);
	}

	@Override
	protected boolean routeExists(long srcId, long dstId) {
		// TODO Auto-generated method stub
		return super.routeExists(srcId, dstId);
	}

	@Override
	protected Route getRoute(ServiceChain sc, long srcId, short srcPort,
			long dstId, short dstPort, long cookie) {
		// Return null the route source and desitnation are the
		// same switchports.
		// ------------------------replace by next
		// part---------------------------------
		if (false) {
			if (srcId == dstId && srcPort == dstPort)
				return null;

			List<NodePortTuple> nptList;
			NodePortTuple npt;
			Route r = getRoute(srcId, dstId, 0);

			if (r == null && srcId != dstId)
				return null;

			if (r != null) {
				nptList = new ArrayList<NodePortTuple>(r.getPath());
			} else {
				// r == null and srcId = dstId
				nptList = new ArrayList<NodePortTuple>();
			}
			npt = new NodePortTuple(srcId, srcPort);
			nptList.add(0, npt); // add src port to the front
			npt = new NodePortTuple(dstId, dstPort);
			nptList.add(npt); // add dst port to the end

			RouteId id = new RouteId(srcId, dstId);
			r = new Route(id, nptList);
			return r;
			// ----------------------------------------------------------------
		} else {
			synchronized (this) {
				// #######################################################################
				if (srcId == dstId && srcPort == dstPort)
					return null;
				RouteId rid = new RouteId(srcId, dstId);
				List<NodePortTuple> path = MyFlowList.getInstance()
						.getEstablishedFlows().get(rid);
				if (path != null) {
					return new Route(rid, path);
				}
				Boolean isDstRooted = true;
				// Map<Link, Integer> linkCost =
				// MyFlowList.getInstance().getLinkCost();
				if (MyFlowList.getInstance().getLinkCost() == null
						|| MyFlowList.getInstance().getEstablishedFlows()
								.size() == 0) {
					MyFlowList.getInstance().initLinkCost(switchPortLinks);
				}
				Map<Link, Integer> tmpLinkCost = MyFlowList.getInstance()
						.getTmpLinkCost(rid);
				Long root = dstId;
				// defalut only one cluster
				Cluster c = (Cluster) clusters.toArray()[0];
				BroadcastTree bt = this.dijkstra(c, root, tmpLinkCost,
						isDstRooted);
				Long dst = dstId;
				Long src = srcId;
				Route my_result = null;
				System.out
						.println("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
				// System.out.println("flow size:"+MyFlowList.getInstance().getEstablishedFlows().size());
				// System.out.println("linkCost size:"+MyFlowList.getInstance().getLinkCost().size());
				System.out.println("from " + src + " to " + dst + ",cost:"
						+ bt.getCosts().get(src));
				System.out.print(src);
				Link tmp_link = bt.getLinks().get(src);
				if (tmp_link == null) {
					System.out.println();
					// return my_result;
				} else {
					// my_result = new Route();
					path = new ArrayList<NodePortTuple>();
					NodePortTuple npt1 = new NodePortTuple(tmp_link.getSrc(),
							tmp_link.getSrcPort());
					NodePortTuple npt2 = new NodePortTuple(tmp_link.getDst(),
							tmp_link.getDstPort());
					path.add(npt1);
					path.add(npt2);
					Long tmp_dst = tmp_link.getDst();
					while (tmp_dst != dst) {
						System.out.print(">>" + tmp_dst);
						tmp_link = bt.getLinks().get(tmp_dst);
						tmp_dst = tmp_link.getDst();
						npt1 = new NodePortTuple(tmp_link.getSrc(),
								tmp_link.getSrcPort());
						npt2 = new NodePortTuple(tmp_link.getDst(),
								tmp_link.getDstPort());
						path.add(npt1);
						path.add(npt2);
					}
					// ///////////////
					npt1 = new NodePortTuple(srcId, srcPort);
					path.add(0, npt1); // add src port to the front
					npt2 = new NodePortTuple(dstId, dstPort);
					path.add(npt2); // add dst port to the end
					// ///////////////
					my_result = new Route(new RouteId(srcId, dstId), path);
					System.out.println(">>" + dst);
				}
				// #################create new flow########################
				RouteId new_rid = (my_result.getId());
				// ###################record new flow in MyFLowList#######
				MyFlowList.getInstance().add(new_rid, my_result.getPath(),
						switchPortLinks);
				// #######################################################
				return my_result;
				// System.out.println("myresult:"+my_result);
				// System.out.println("r       :"+r);
			}
		}

	}

	// NOTE: Return a null route if srcId equals dstId. The null route
	// need not be stored in the cache. Moreover, the LoadingCache will
	// throw an exception if null route is returned.
	@Override
	protected Route getRoute(long srcId, long dstId, long cookie) {
		// Return null route if srcId equals dstId
		if (srcId == dstId)
			return null;

		RouteId id = new RouteId(srcId, dstId);
		Route result = null;

		try {
			// System.out.println(Thread.currentThread()+": before getRoute pathcache.size::~~~~::::"+this.pathcache.size());
			// System.out.println("+++++++++++++++++++++++++++++++++++++++++++++");
			// System.out.println("befor pathcache.szie::::::"+this.pathcache.size());//3
			// this.calculateShortestPathTreeInClusters();
			result = pathcache.get(id);
			// System.out.println("after pathcache.szie::::::"+this.pathcache.size());//0
			// System.out.println("_____________________________________________");
			// System.out.println(Thread.currentThread()+": after getRoute pathcache.size:::~~~~:::"+this.pathcache.size());
		} catch (Exception e) {

			log.error("{}", e);
		}

		if (log.isTraceEnabled()) {
			log.trace("getRoute: {} -> {}", id, result);
		}
		// System.out.println("!!!!!!!!!result:::" + result);

		return result;
	}

	@Override
	protected BroadcastTree getBroadcastTreeForCluster(long clusterId) {
		// TODO Auto-generated method stub
		return super.getBroadcastTreeForCluster(clusterId);
	}

	@Override
	protected boolean isInternalToOpenflowDomain(long switchid, short port) {
		// TODO Auto-generated method stub
		return super.isInternalToOpenflowDomain(switchid, port);
	}

	@Override
	public boolean isAttachmentPointPort(long switchid, short port) {
		// TODO Auto-generated method stub
		return super.isAttachmentPointPort(switchid, port);
	}

	@Override
	protected long getOpenflowDomainId(long switchId) {
		// TODO Auto-generated method stub
		return super.getOpenflowDomainId(switchId);
	}

	@Override
	protected long getL2DomainId(long switchId) {
		// TODO Auto-generated method stub
		return super.getL2DomainId(switchId);
	}

	@Override
	protected Set<Long> getSwitchesInOpenflowDomain(long switchId) {
		// TODO Auto-generated method stub
		return super.getSwitchesInOpenflowDomain(switchId);
	}

	@Override
	protected boolean inSameOpenflowDomain(long switch1, long switch2) {
		// TODO Auto-generated method stub
		return super.inSameOpenflowDomain(switch1, switch2);
	}

	@Override
	public boolean isAllowed(long sw, short portId) {
		// TODO Auto-generated method stub
		return super.isAllowed(sw, portId);
	}

	@Override
	protected boolean isIncomingBroadcastAllowedOnSwitchPort(long sw,
			short portId) {
		// TODO Auto-generated method stub
		return super.isIncomingBroadcastAllowedOnSwitchPort(sw, portId);
	}

	@Override
	public boolean isConsistent(long oldSw, short oldPort, long newSw,
			short newPort) {
		// TODO Auto-generated method stub
		return super.isConsistent(oldSw, oldPort, newSw, newPort);
	}

	@Override
	protected Set<NodePortTuple> getBroadcastNodePortsInCluster(long sw) {
		// TODO Auto-generated method stub
		return super.getBroadcastNodePortsInCluster(sw);
	}

	@Override
	public boolean inSameBroadcastDomain(long s1, short p1, long s2, short p2) {
		// TODO Auto-generated method stub
		return super.inSameBroadcastDomain(s1, p1, s2, p2);
	}

	@Override
	public boolean inSameL2Domain(long switch1, long switch2) {
		// TODO Auto-generated method stub
		return super.inSameL2Domain(switch1, switch2);
	}

	@Override
	public NodePortTuple getOutgoingSwitchPort(long src, short srcPort,
			long dst, short dstPort) {
		// TODO Auto-generated method stub
		return super.getOutgoingSwitchPort(src, srcPort, dst, dstPort);
	}

	@Override
	public NodePortTuple getIncomingSwitchPort(long src, short srcPort,
			long dst, short dstPort) {
		// TODO Auto-generated method stub
		return super.getIncomingSwitchPort(src, srcPort, dst, dstPort);
	}

	@Override
	public Set<Long> getSwitches() {
		// TODO Auto-generated method stub
		return super.getSwitches();
	}

	@Override
	public Set<Short> getPortsWithLinks(long sw) {
		// TODO Auto-generated method stub
		return super.getPortsWithLinks(sw);
	}

	@Override
	public Set<Short> getBroadcastPorts(long targetSw, long src, short srcPort) {
		// TODO Auto-generated method stub
		return super.getBroadcastPorts(targetSw, src, srcPort);
	}

	@Override
	public NodePortTuple getAllowedOutgoingBroadcastPort(long src,
			short srcPort, long dst, short dstPort) {
		// TODO Auto-generated method stub
		return super
				.getAllowedOutgoingBroadcastPort(src, srcPort, dst, dstPort);
	}

	@Override
	public NodePortTuple getAllowedIncomingBroadcastPort(long src, short srcPort) {
		// TODO Auto-generated method stub
		return super.getAllowedIncomingBroadcastPort(src, srcPort);
	}

}
