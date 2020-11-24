import sys
import re
import configparser

HOST_FORMAT_HELP = "Single host: <host name>.<cloud type>.cloudera.com\n" \
    "Multiple hosts: <group name>{<index range>}.<cloud type>.cloudera.com\n" \
    "Multiple hosts: <group name>{index,index,index}.<cloud type>.cloudera.com"

'''Regex pattern to parse host strings like ve03{01..14}.halxg.cloudera.com'''
HOSTS_REGEX_PATTERN1 = re.compile(r"^([a-z][a-z0-9-]+[a-z0-9])[{\[]([0-9][0-9]*)\.\.([0-9][0-9]*)[}\]]\.(.*)")

'''Regex pattern to parse host strings like ia01{02,04,06,08,10,12}.halxg.cloudera.com'''
HOSTS_REGEX_PATTERN2 = re.compile(r"^([a-z][a-z0-9-]+[a-z0-9])[{\[](.*)[}\]]\.(.*)")

'''Regex pattern to parse individual hosts like ve0301.halxg.cloudera.com'''
HOSTS_REGEX_PATTERN3 = re.compile(r"^([a-z][a-z0-9-]+[a-z0-9])\.(.*)")

class EqualsSpaceRemover:
    output_file = None
    def __init__(self, new_output_file):
        self.output_file = new_output_file

    def write(self, what):
        self.output_file.write(what.replace(" = ", "=", 1))

def extract_hosts_from_str(hosts):
    """
    Parses given host strings using regulare expression and return parsed hostnames as list
    """
    all_hosts = list()
    details = list()
    for host_string in hosts:
        if HOSTS_REGEX_PATTERN1.match(host_string):
            match = HOSTS_REGEX_PATTERN1.match(host_string)
            hosts_list = get_hosts_pattern1(match.group(1), \
                                            match.group(2), \
                                            match.group(3), \
                                            match.group(4))
        elif HOSTS_REGEX_PATTERN2.match(host_string):
            match = HOSTS_REGEX_PATTERN2.match(host_string)
            hosts_list = get_hosts_pattern2(match.group(1), match.group(2), match.group(3))
        elif HOSTS_REGEX_PATTERN3.match(host_string):
            match = HOSTS_REGEX_PATTERN3.match(host_string)
            hosts_list = list()
            hosts_list.append(host_string)
        else:
            raise Exception("Unexpected hosts pattern: '%s'. " \
                        "Please specify hosts as follows:'%s'" % (host_string, HOST_FORMAT_HELP))

        details.append(f"No. of nodes parsed for host string '{host_string}' = {len(hosts_list)}")
        all_hosts.extend(hosts_list)
    return all_hosts, details

def get_hosts_pattern1(name, start_offset, end_offset, hostgroup):
    """
    Method to parse hosts like 've03{01..14}.halxg.cloudera.com' using regular expression
    """
    hosts_list = list()
    for host_offset in range(int(start_offset), int(end_offset)+1):
        if host_offset <= 9 and start_offset.startswith("0"):
            host = f"{name}0{host_offset}.{hostgroup}"
        else:
            host = f"{name}{host_offset}.{hostgroup}"
        hosts_list.append(host)
    return hosts_list

def get_hosts_pattern2(name, host_index, hostgroup):
    """
    Method to parse hosts like 'ia01{02,04,08,10}.halxg.cloudera.com' using regular expression
    """
    hosts_list = list()
    for host_offset in host_index.split(","):
        host = f"{name}{host_offset}.{hostgroup}"
        hosts_list.append(host)
    return hosts_list

def write_ansible_invetory_file(hosts_list, key_location):
    """
    Takes a list and creates an ansible inventory (INI) file
    """

    key_location = f'"{key_location}"'
    config = configparser.ConfigParser()
    for host_index, host_name in enumerate(hosts_list):
        if  0 <= host_index <= 4:
            group = f'master{host_index+1}'
            config.add_section(group)
            config.set(group, f'{host_name} ansible_user=systest ansible_ssh_private_key_file', key_location)
        elif  5 <= host_index <= 7:
            group = f'worker{host_index-4}'
            config.add_section(group)
            config.set(group, f'{host_name} ansible_user=systest ansible_ssh_private_key_file', key_location)
        else:
            group = f'allworkers{host_index-7}'
            config.add_section(group)
            config.set(group, f'{host_name}  ansible_user=systest ansible_ssh_private_key_file', key_location)

    with open('inventory/static_50nodes', 'w') as outfile:
        config.write(EqualsSpaceRemover(outfile))

def main():
    """
    Starting method
    """
    if len(sys.argv) <= 1:
        print("Please specify hosts as follows:'%s'" % (HOST_FORMAT_HELP))
        sys.exit(1)
    hosts = sys.argv[1].split(":")
    hosts_list, details = extract_hosts_from_str(hosts)
    print(details)
    print(hosts_list)
    write_ansible_invetory_file(hosts_list, "~/arun/systest.pem")

main()
