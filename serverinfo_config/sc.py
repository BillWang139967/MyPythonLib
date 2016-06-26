#-*- coding: utf-8 -*-
#
"""Package for reading and writing server configurations
"""

import os
import si
import shutil

#{{{raw_loadconfig
def raw_loadconfig(filepath, return_sort=False, delimiter='=', quoter=' "\'', overwrite=True):
    """Read config from file.
    """
    if not os.path.exists(filepath): return None
    config = {}
    if return_sort: sortlist = []
    with open(filepath) as f:
        for line in f:
            pair = line.strip().split(delimiter)
            if len(pair) != 2: continue
            k, v = [x.strip(quoter) for x in pair]
            if return_sort: sortlist.append(k)
            if overwrite:
                config[k] = v
            else:
                if not config.has_key(k): config[k] = []
                config[k].append(v)
    if return_sort:
        return (config, sortlist)
    else:
        return config

#}}}
#{{{raw_saveconfig
def raw_saveconfig(filepath, config, sortlist=[], delimiter='=', quoter='"'):
    """Write config to file.
    """
    if not os.path.exists(filepath): return False
    lines = []

    # write the item in sortlist first
    if len(sortlist) > 0:
        for k in sortlist:
            if config.has_key(k):
                line = '%s=%s\n' % (k, config[k])
                del config[k]
                lines.append(line)

    # then write the rest items
    for k,v in config.iteritems():
        if isinstance(v, list):
            for vv in v:
                line = '%s%s%s%s%s\n' % (k,delimiter,quoter,vv,quoter)
                lines.append(line)
        else:
            line = '%s%s%s%s%s\n' % (k,delimiter,quoter,v,quoter)
            lines.append(line)

    with open(filepath, 'w') as f: f.writelines(lines)
    return True

#}}}
#{{{loadconfig
def loadconfig(filepath, keymap, delimiter='=', quoter=' "\''):
    """Load config from file and parse it to dict.
    """
    raw_config = raw_loadconfig(filepath)
    if raw_config == None: return None
    config = dict((keymap[k],v) for k,v in raw_config.iteritems() if keymap.has_key(k))
    return config
#}}}
#{{{saveconfig
def saveconfig(filepath, keymap, config, delimiter='=', read_quoter=' "\'', write_quoter='"'):
    """Save config to file.
    """
    raw_config, sortlist = raw_loadconfig(filepath, return_sort=True, delimiter=delimiter, quoter=read_quoter)
    if raw_config == None: return False
    for k,v in config.iteritems():
        if keymap.has_key(k):
            raw_config[keymap[k]] = v
    return raw_saveconfig(filepath, raw_config, sortlist, delimiter=delimiter, quoter=write_quoter)
#}}}
class Server(object):
    #{{{network
    @classmethod
    def ifconfig(self, ifname, config=None):
        """Read or write single interface's config.
        
        Pass None to parameter config (as default) to read config,
        or pass a dict type to config to write config.
        """
        dist = si.Server.dist()
        if dist['name'] in ('centos', 'redhat'):
            cfile = '/etc/sysconfig/network-scripts/ifcfg-%s' % ifname
            cmap = {
                'DEVICE': 'name',
                'HWADDR': 'mac',
                'IPADDR': 'ip',
                'NETMASK': 'mask',
                'GATEWAY': 'gw',
            }
            if config == None:
                return loadconfig(cfile, cmap)
            else:
                cmap_reverse = dict((v,k) for k, v in cmap.iteritems())
                return saveconfig(cfile, cmap_reverse, config)
        else:
            return None

    @classmethod
    def ifconfigs(self):
        """Read config of all interfaces.
        """
        configs = {}
        ifaces = si.Server.netifaces()
        for iface in ifaces:
            ifname = iface['name']
            config = Server.ifconfig(ifname)
            if config:
                configs[ifname] = config
        return configs
    #}}}
    #{{{dns
    @classmethod
    def nameservers(self, nameservers=None):
        """Read or write nameservers to config file.
        
        Pass None to parameter config (as default) to read config,
        or pass a dict type to config to write config.
        """
        nspath = '/etc/resolv.conf'
        if nameservers == None:
            nameservers = raw_loadconfig(nspath, delimiter=' ', overwrite=False)
            if nameservers:
                return nameservers['nameserver']
            else:
                return []
        else:
            return raw_saveconfig(nspath, 
                                   {'nameserver': nameservers},
                                   delimiter=' ', quoter='')
    #}}}
if __name__ == '__main__':
    print
    #{{{configure network
    # read network config
    config = Server.ifconfig('eth0')
    print '* Config of eth0:'
    if config.has_key('mac'): print '  HWADDR: %s' % config['mac']
    if config.has_key('ip'): print '  IPADDR: %s' % config['ip']
    if config.has_key('mask'): print '  NETMASK: %s' % config['mask']
    if config.has_key('gw'): print '  GATEWAY: %s' % config['gw']
    print

    # write config
    print '* Write back config of eth0:'
    print '  Return: %s ' % str(Server.ifconfig('eth0', config))
    print
    
    configs = Server.ifconfigs()
    for ifname, config in configs.iteritems():
        print '* Config of %s:' % ifname
        if config.has_key('mac'): print '  HWADDR: %s' % config['mac']
        if config.has_key('ip'): print '  IPADDR: %s' % config['ip']
        if config.has_key('mask'): print '  NETMASK: %s' % config['mask']
        if config.has_key('gw'): print '  GATEWAY: %s' % config['gw']
        print
    
    #}}}
    #{{{configure dns
    nameservers = Server.nameservers()
    print '* Nameservers:'
    for nameserver in nameservers:
        print '  %s' % nameserver
    print

    print '* Write back nameservers:'
    print '  Return: %s ' % str(Server.nameservers(nameservers))
    print
    #}}}
