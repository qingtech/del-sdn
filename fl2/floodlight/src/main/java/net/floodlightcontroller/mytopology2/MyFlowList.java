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
	private Map<Link, Integer> linkCost = null;
	private Map<RouteId, Integer> linkBW = new HashMap<RouteId, Integer>();
	private Map<RouteId, Integer> bw_need = new HashMap<RouteId, Integer>();
	private MyFlowList(){
		established_flows =  new HashMap<RouteId, List<NodePortTuple>>();
		bw_need.put(new RouteId(1L,7L), 95);
		bw_need.put(new RouteId(7L,1L), 80);
		
		//routeId eq link
		int bw = 100;
		linkBW.put(new RouteId(1L,3L), 90);
		linkBW.put(new RouteId(1L,4L), bw);
		linkBW.put(new RouteId(2L,3L), bw);
		linkBW.put(new RouteId(2L,4L), bw);
		linkBW.put(new RouteId(3L,4L), bw);
		linkBW.put(new RouteId(3L,5L), 90);
		linkBW.put(new RouteId(3L,6L), bw);
		linkBW.put(new RouteId(4L,5L), bw);
		linkBW.put(new RouteId(4L,6L), bw);
		linkBW.put(new RouteId(5L,6L), bw);
		linkBW.put(new RouteId(5L,7L), 90);
		linkBW.put(new RouteId(5L,8L), bw);
		linkBW.put(new RouteId(6L,7L), bw);
		linkBW.put(new RouteId(6L,8L), bw);
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
	
//	public synchronized void add(RouteId rid, List<NodePortTuple> path,Map<NodePortTuple,
//            Set<Link>> switchPortLinks){
//		if(established_flows==null){
//			established_flows =  new HashMap<RouteId, List<NodePortTuple>>();
//		}
//		
//		if(!established_flows.containsKey(rid)){
//			established_flows.put(rid, path);
//			//fresh linkCost
//			for(int i=1;i<path.size();i+=2){
//				NodePortTuple npt = path.get(i);
//				//System.out.println("switch:"+npt.getNodeId());
//				Set<Link> links = switchPortLinks.get(npt);
//				if(links == null) continue;
//				for (Link link : links) {
//					if (link == null)
//						continue;
//					if(linkCost.containsKey(link)){
//						int tmp = linkCost.get(link);
//						linkCost.remove(link);
//						linkCost.put(link, tmp+1);
//					}else{
//						linkCost.put(link,2);
//					}
//				}
//			}
//		}
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
					RouteId l; //represition link
					if(link.getSrc()<link.getDst()){
						l = new RouteId(link.getSrc(),link.getDst());
					}else{
						l = new RouteId(link.getDst(),link.getSrc());
					}
					Integer bw = linkBW.get(l);
					Integer need = bw_need.get(rid);
//					if(need == null){
//						need = bw_need.get(new RouteId(rid.getDst(),rid.getSrc()));
//					}
					if(bw!=null&&need!=null){
						if(linkCost.containsKey(link)){
							int b = this.getLinkCostByBW(bw, need);
							int tmp = linkCost.get(link);
							//System.out.println("bw:"+bw+",need:"+need+"\n"+link+"\ntmp::::"+tmp+"\nb=="+b);
							linkCost.remove(link);
							linkCost.put(link, tmp+b);
						}else{
							linkCost.put(link,1 + this.getLinkCostByBW(bw, need));
						}
						continue;
					}
					System.out.println("Can not fin bw an bw_need!!!!!!!!!");
					System.out.println("l  :"+l);
					System.out.println("rid:"+rid);
					if(linkCost.containsKey(link)){
						int tmp = linkCost.get(link);
						linkCost.remove(link);
						linkCost.put(link, tmp+1);
					}else{
						linkCost.put(link,2);
					}
				}
			}
		}
	}
	public synchronized void initLinkCost(Map<NodePortTuple,Set<Link>> switchPortLinks){
		linkCost = new HashMap<Link, Integer>();
		System.out.println("initLinkCost!!!!!!!!!!!!!!!!!");
		for ( NodePortTuple npt : switchPortLinks.keySet()) {
			Set<Link> links = switchPortLinks.get(npt);
			for(Link link:links){
				this.linkCost.put(link, 1);
				//System.out.println(link);
			}
		}
	} 
	public synchronized Map<Link, Integer> getTmpLinkCost(RouteId rid){
		Map<Link, Integer> tmpLinkCost = new HashMap<Link, Integer>();
		//System.out.println("linkCost.size::"+this.getLinkCost().size());
			for (Link link : this.getLinkCost().keySet()) {
				//System.out.println(link);
				Integer bw = linkBW.get(new RouteId(link.getSrc(),link.getDst()));
				if(bw == null){
					bw = linkBW.get(new RouteId(link.getDst(),link.getSrc()));
				}
				Integer need = bw_need.get(rid);
//				if(need == null){
//					need = bw_need.get(new RouteId(rid.getDst(),rid.getSrc()));
//				}
				if(bw!=null&&need!=null){
					int tmp = linkCost.get(link) + this.getLinkCostByBW(bw, need);
					//System.out.println("tmplink"+link+"\n:::tmp::"+tmp);
					tmpLinkCost.put(link, tmp);
					//System.out.println(linkCost.size());
					
				}else{
					System.out.println("can not find bw an need get tmpLinkCost");
					System.out.println("link:"+link);
					System.out.println("rid:"+rid);
				}
				
			}
		return tmpLinkCost;
	} 
	private synchronized Integer getLinkCostByBW(int bw, int need){
		//System.out.println("bw:"+bw+",need:"+bw_need);
		int r = 3;
		if(bw < need){
//			System.out.println("bw < need");
//			System.out.println("!!!!bw:"+bw+",need:"+bw_need);
			r = 6;
		}
		return need*r/bw;
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
