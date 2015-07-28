import sys
import telnetlib
from connection_exceptions import *

class Connection:
    def __init__(self, host, username=None, password=None, enable=None):
        self.host = host
        self.username = username
        self.password = password
        self.enable = enable

        TIMEOUT=3


    def getConfigByTelnet(self):
        '''
        get configuration from cisco device through telnet connection.
        '''
        try:
            tn = telnetlib.Telnet(self.host)
        except Exception:
            raise TelnetConnectionError
            exit()

        # login
        result = tn.read_until('Password: ', self.TIMEOUT)
        if result.endswith('Username: '):
            tn.write(self.username + '\n')
            tn.read_until('Password: ', self.TIMEOUT)
            tn.write(self.password + '\n')
        elif result.endswith('Password: '):
            tn.write(self.password + '\n')
        else:
            raise TelnetAuthenticationError


        # enter privilege mode
        result = tn.read_until('#', self.TIMEOUT)
        if not result.endswith('#') and not result.endswith('>'):
            raise TelnetAuthenticationError
            exit()
        if result.endswith('>'):
            tn.write('enable' + '\n' + self.enable + '\n')
            result = tn.read_until('#', self.TIMEOUT)
            if result.endswith('#') is False:
                raise TelnetEnableError
                exit()


        #get file config
        tn.write('term length 0' + '\n')
        tn.read_until('#', self.TIMEOUT),
        tn.write('show run\n')
        result = tn.read_until("#", self.TIMEOUT)
        f = open(self.host + '_running-config.txt', 'wt')
        f.write(result)
        f.close()

        tn.write('show vlan\n')
        result = tn.read_until("#", self.TIMEOUT)
        f = open(self.host + '_vlan.txt', 'wt')
        f.write(result)
        f.close()

        tn.close()
