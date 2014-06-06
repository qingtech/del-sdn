from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

import sys,os

def cur_file_dir():
	path = sys.path[0]
	if os.path.isdir(path):
		return path
	elif os.path.isfile(path):
		return os.path.dirname(path)
class MyTopo( Topo ):

	def __init__( self ):

		Topo.__init__( self )

		pc1 = self.addHost( 'pc1', ip = '10.0.0.1' )
		sv2 = self.addHost( 'sv2', ip = '10.0.0.2' )
		sv3 = self.addHost( 'sv3', ip = '10.0.0.3' )
		
		sw4 = self.addSwitch ('sw4', listenPort=6634 )
		sw5 = self.addSwitch ('sw5', listenPort=6635 )
		#sw0.listenPort( 6634 )
		#sw1.listenPort( 6635 )

		self.addLink( pc1, sw4, 0, 0 )
		self.addLink( sv2, sw5, 0, 0 )
		self.addLink( sv3, sw5, 0, 1 )
		self.addLink( sw4, sw5, 1, 2 )
		
		
topos = { 'mytopo': ( lambda: MyTopo() ) }

if __name__ == '__main__':
	setLogLevel('info')
	topo = MyTopo()
	net = Mininet( topo = topo, switch=OVSSwitch, build=False, autoSetMacs=True )
	c1 = RemoteController('c1', ip='127.0.0.1')
	net.addController(c1)
	net.build()
	for h in net.hosts:
		#if h.name == 'pc1':
		#	h.cmd('ping sv2')
		h.cmd(cur_file_dir()+'/init_net')
	net.start()
	CLI( net )
	net.stop()

