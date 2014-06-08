from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
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

		pc11 = self.addHost( 'pc11', ip = '10.0.0.1' )
		sv12 = self.addHost( 'sv12', ip = '10.0.0.2' )
		sv13 = self.addHost( 'sv13', ip = '10.0.0.3' )
		
		sw = {}
		for i in xrange(1,9):
			s = 'sw%d'%i
			p = 6633+i # start from 6634
			sw[s] = self.addSwitch (s, listenPort = p )

		bw = 10
		self.addLink( sw['sw1'], sw['sw3'], bw=bw )
		self.addLink( sw['sw1'], sw['sw4'], bw=bw )
		self.addLink( sw['sw2'], sw['sw3'], bw=bw )
		self.addLink( sw['sw2'], sw['sw4'], bw=bw )
		self.addLink( sw['sw3'], sw['sw4'], bw=bw )
		self.addLink( sw['sw3'], sw['sw5'], bw=bw )
		self.addLink( sw['sw3'], sw['sw6'], bw=bw )
		self.addLink( sw['sw4'], sw['sw5'], bw=bw )
		self.addLink( sw['sw4'], sw['sw6'], bw=bw )
		self.addLink( sw['sw5'], sw['sw6'], bw=bw )
		self.addLink( sw['sw5'], sw['sw7'], bw=bw )
		self.addLink( sw['sw5'], sw['sw8'], bw=bw )
		self.addLink( sw['sw6'], sw['sw7'], bw=bw )
		
		self.addLink( sw['sw1'], pc11, bw=bw )
		self.addLink( sw['sw7'], sv12, bw=bw )
		self.addLink( sw['sw8'], sv13, bw=bw )
		
topos = { 'mytopo': ( lambda: MyTopo() ) }

if __name__ == '__main__':
	setLogLevel('info')
	topo = MyTopo()
	net = Mininet( topo = topo, switch=OVSSwitch, link=TCLink, build=False, autoSetMacs=True )
	c0 = RemoteController('c0', ip='127.0.0.1')
	net.addController(c0)
	net.build()
	net.start()
	CLI( net )
	net.stop()

