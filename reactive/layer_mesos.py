from charms.reactive import when, when_not, set_state
from charmhelpers.core.hookenv import status_set, log, resource_get
from subprocess import check_call, CalledProcessError, call, check_output, Popen
from charmhelpers.core import hookenv
from charms.reactive.helpers import data_changed
from charmhelpers.core.host import mkdir

mesos_directory="/opt/mesos"

@when_not('java.ready')
def update_java_status():
    status_set('blocked', 'Waiting for Java.')

@when_not('marathon.installed')
def install_layer_mesos():
    mkdir('/opt/marathon')
    marathon = resource_get("software")
    check_output(["tar", "xvfz", marathon, "--strip-components=1", "-C", '/opt/marathon'])
    set_state('marathon.installed')
    status_set('waiting', 'Apache Mesos Installed, Awaiting Configuration')



@when('zookeeper.joined')
@when_not('zookeeper.ready')
def wait_for_zookeeper(zookeeper):
    """
         We always run in Distributed mode, so wait for Zookeeper to become available.
    """
    hookenv.status_set('waiting', 'Waiting for Zookeeper to become available')

@when('java.ready')
@when('zookeeper.ready')
@when_not('marathon.running')
def configure(java, zookeeper):
    """
        Configure Zookeeper for the first time.
        This will set memory limits. By default we use a % model for memory calculations.
        This allows us to automatically scale the drillbit depending on where it is installed.
    """
    status_set('active', 'Starting Marathon')
    zklist = ''
    for zk_unit in zookeeper.zookeepers():
        zklist += add_zookeeper(zk_unit['host'], zk_unit['port'])
    zklist = zklist[:-1]
    start_mesos(zklist)
    hookenv.open_port('8080')
    set_state('marathon.running')
    status_set('active', 'Marathon up and running')

def start_mesos(zookeepers):
    check_call(['/opt/marathon/bin/start','--master', 'zk://'+zookeepers+'/mesos', '--zk', 'zk://'+zookeepers+'/marathon'])
