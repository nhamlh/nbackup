import telnetlib
import re
from connection_exceptions import *


class CiscoDevice:

    def __init__(self,
                 hostname,
                 username=None,
                 password=None,
                 enable=None
                 ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.enable = enable

        self.TIMEOUT = 3

    def get_config_by_telnet(self):
        '''
        get configuration from cisco device through telnet connection.
        '''
        try:
            tn = telnetlib.Telnet(self.hostname)
        except Exception:
            raise TelnetConnectionError

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

        if result.endswith('>'):
            tn.write('enable' + '\n' + self.enable + '\n')
            result = tn.read_until('#', self.TIMEOUT)
            if result.endswith('#') is False:
                raise TelnetEnableError

        # get configuration
        tn.write('term length 0' + '\n')
        tn.read_until('#', self.TIMEOUT),
        tn.write('show run' + '\n')
        tn.write('exit' + '\n')
        result = tn.read_all()

        tn.close()
        return result


class JuniperDevice:

    def __init__(self,
                 hostname,
                 username=None,
                 password=None,
                 ):
        self.hostname = hostname
        self.username = username
        self.password = password

        self.TIMEOUT = 3

    def get_config_by_telnet(self):
        '''
        get configuration from juniper device through telnet connection.
        '''
        try:
            tn = telnetlib.Telnet(self.hostname)
        except Exception:
            raise TelnetConnectionError
            exit()

        # login
        result = tn.read_until('Password: ', self.TIMEOUT)
        if result.endswith('login: '):
            tn.write(self.username + '\n')
            tn.read_until('Password: ', self.TIMEOUT)
            tn.write(self.password + '\n')
        elif result.endswith('Password: '):
            tn.write(self.password + '\n')
        else:
            raise TelnetAuthenticationError

        # get user permission
        tn.read_until('>', self.TIMEOUT)
        tn.write('show cli authorization | no-more' + '\n')
        result = tn.read_until('>', self.TIMEOUT)

        # user doesn't have view-configuration permission
        view_configuration = re.findall('view-configuration', result)
        if view_configuration is []:
            raise TelnetAuthenticationError

        # get configuration
        tn.write('show configuration | no-more' + '\n')
        tn.write('exit' + '\n')
        result = tn.read_all()

        tn.close()
        return result
