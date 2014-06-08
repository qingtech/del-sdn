package net.floodlightcontroller.mytopology2;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import net.floodlightcontroller.routing.RouteId;
import net.floodlightcontroller.topology.NodePortTuple;


public class MyFlowList {
	
	private static MyFlowList instance;
	//String key = null;//srcDevice->dstDevice
	//route path:List<NodePortTuple> switchPortList = route.getPath();
	private Map<RouteId, List<NodePortTuple>> new_flows =  null;
	private Map<RouteId, List<NodePortTuple>> old_flows =  null;
	private MyFlowList(){
		new_flows =  new HashMap<RouteId, List<NodePortTuple>>();
	}
	public static MyFlowList getInstance(){
		if(instance == null){
			instance = new MyFlowList();
		}
		return instance;
	}
	
	public void add(RouteId rid, List<NodePortTuple> path){
		if(new_flows==null){
			new_flows =  new HashMap<RouteId, List<NodePortTuple>>();
		}
		if(!new_flows.containsKey(rid)){
			new_flows.put(rid, path);
		}
	}
	public Map<RouteId, List<NodePortTuple>> getNewFlows(){
		return new_flows;
	}
	public void MoveToOldFlows(){
		if(this.old_flows==null){
			this.old_flows = new HashMap<RouteId, List<NodePortTuple>>();
		}
		for(RouteId rid : this.new_flows.keySet()){
			this.old_flows.put(rid, this.new_flows.get(rid));
		}
		this.new_flows =  new HashMap<RouteId, List<NodePortTuple>>();
	}

}
