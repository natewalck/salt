'''
Module for returning statistics about a minion
'''
import subprocess
import re

def uptime():
    '''
    Return the uptime for this minion

    CLI Example:
    salt '*' stats.uptime
    '''
    return subprocess.Popen(['uptime'],
            stdout=subprocess.PIPE).communicate()[0].strip()

def loadavg():
    '''
    Return the load averages for this minion

    CLI Example:
    salt '*' stats.loadavg
    '''
    comps = open('/proc/loadavg', 'r').read().strip()
    loadavg = comps.split()
    return { 
        '1-min':  loadavg[1],
        '5-min':  loadavg[2],
        '15-min': loadavg[3],
    }

def cpustats():
    '''
    Return the CPU stats for this minon

    CLI Example:
    salt '*' stats.cpustats
    '''
    stats = open('/proc/stat', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        if comps[0] == 'cpu':
            ret[comps[0]] = {
                'user':    comps[1],
                'nice':    comps[2],
                'system':  comps[3],
                'idle':    comps[4],
                'iowait':  comps[5],
                'irq':     comps[6],
                'softirq': comps[7],
                'steal':   comps[8],
            }
        elif comps[0] == 'intr':
            ret[comps[0]] = {
                'total': comps[1],
                'irqs' : comps[2:],
            }
        elif comps[0] == 'softirq':
            ret[comps[0]] = {
                'total':    comps[1],
                'softirqs': comps[2:],
            }
        else:
            ret[comps[0]] = comps[1]
    return ret

def meminfo():
    '''
    Return the CPU stats for this minon

    CLI Example:
    salt '*' stats.meminfo
    '''
    stats = open('/proc/meminfo', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        comps[0] = comps[0].replace(':', '')
        ret[comps[0]] = {
            'value':    comps[1],
        }
        if len(comps) > 2:
            ret[comps[0]]['unit'] = comps[2]
    return ret

def cpuinfo():
    ''' 
    Return the CPU info for this minon

    CLI Example:
    salt '*' stats.cpuinfo
    '''
    stats = open('/proc/cpuinfo', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split(':')
        comps[0] = comps[0].strip()
        if comps[0] == 'flags':
            ret[comps[0]] = comps[1].split()
        else:
            comps[1] = comps[1].strip()
            ret[comps[0]] = comps[1]
    return ret 

