package net.floodlightcontroller.mytopology2;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import net.floodlightcontroller.routing.Link;
import net.floodlightcontroller.routing.RouteId;
import net.floodlightcontroller.topology.NodePortTuple;


public class MyFlowList {
	
	private static MyFlowList instance;
	//String key = null;//srcDevice->dstDevice
	//route path:List<NodePortTuple> switchPortList = route.getPath();
	private Map<RouteId, List<NodePortTuple>> established_flows =  null;
	private Map<RouteId, List<NodePortTuple>> unestablished_flows =  null;
	private Map<Link, Integer> linkCost = new HashMap<Link, Integer>();
	private Map<Link, Integer> linkBW = new HashMap<Link, Integer>();
	private Map<RouteId, Integer> bw_need = new HashMap<RouteId, Integer>();
	private MyFlowList(){
		established_flows =  new HashMap<RouteId, List<NodePortTuple>>();
		bw_need.put(new RouteId(1L,7L), 100);
		bw_need.put(new RouteId(1L,7L), 100);
		
		linkBW.put(new Link(), 100);
	}
//	private MyFlowList(Map<NodePortTuple, Set<Link>> switchPortLinks){
//		established_flows =  new HashMap<RouteId, List<NodePortTuple>>();
//		this.switchPortLinks = new HashMap<NodePortTuple,
//                Set<Link>>(switchPortLinks);
//		System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!hello");
//		for(NodePortTuple npt: this.switchPortLinks.keySet()){
//			System.out.println("npt :"+npt);
//			System.out.println("link:"+this.switchPortLinks.get(npt));
//		}
//	}
	public static MyFlowList getInstance(){
		if(instance == null){
			instance = new MyFlowList();
		}
		return instance;
	}
	
//	public static MyFlowList getInstance(Map<NodePortTuple, Set<Link>> switchPortLinks){
//		if(instance == null){
//			instance = new MyFlowList(switchPortLinks);
//		}
//		return instance;
//	}
	
	public synchronized void add(RouteId rid, List<NodePortTuple> path,Map<NodePortTuple,
            Set<Link>> switchPortLinks){
		if(established_flows==null){
			established_flows =  new HashMap<RouteId, List<NodePortTuple>>();
		}
		
		if(!established_flows.containsKey(rid)){
			established_flows.put(rid, path);
			//fresh linkCost
			for(int i=1;i<path.size();i+=2){
				NodePortTuple npt = path.get(i);
				//System.out.println("switch:"+npt.getNodeId());
				Set<Link> links = switchPortLinks.get(npt);
				if(links == null) continue;
				for (Link link : links) {
					if (link == null)
						continue;
					if(linkCost.containsKey(link)){
						int tmp = linkCost.get(link);
						linkCost.remove(link);
						linkCost.put(link, tmp+1);
					}else{
						linkCost.put(link,2);
					}
					// System.out.println(link);
					// System.out.print("src switch:"+link.getSrc());
					// System.out.println(",src port:  "+link.getSrcPort());
					// System.out.print("dst switch:"+link.getDst());
					//System.out.println(",dst port:  "+link.getDstPort());
					
				}
			}
		}
	}
	public Map<RouteId, List<NodePortTuple>> getEstablishedFlows(){
		return established_flows;
	}
	public Map<RouteId, List<NodePortTuple>> getUnestablished_flows() {
		return unestablished_flows;
	}
	public void setUnestablished_flows(
			Map<RouteId, List<NodePortTuple>> unestablished_flows) {
		this.unestablished_flows = unestablished_flows;
	}
	public Map<Link, Integer> getLinkCost() {
		return linkCost;
	}
	public void setLinkCost(Map<Link, Integer> linkCost) {
		this.linkCost = linkCost;
	}
}
