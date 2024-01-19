import socket
import re
import common_ports


def get_open_ports(target, port_range, verbose=False):
  open_ports = []

  ip, error_message = set_connection(target, port_range, open_ports)
  if ip is None:
    return error_message

  host = set_host(ip)

  result_string = set_result_string(ip, host)

  if verbose:
    last_string = print_verbose(open_ports, result_string)
    return last_string

  return open_ports


def set_connection(target, port_range, open_ports):
  try:
    ip = socket.gethostbyname(target)

    for port in range(port_range[0], port_range[1] + 1):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      socket.setdefaulttimeout(1)

      if s.connect_ex((ip, port)) == 0:
        open_ports.append(port)
      s.close()

    return ip, None  # Return ip and no error

  except KeyboardInterrupt:
    return None, "Exiting program"
  except socket.gaierror:
    if re.search('[a-zA-Z]', target):
      return None, "Error: Invalid hostname"
    else:
      return None, "Error: Invalid IP address"
  except socket.error:
    return None, "Error: Invalid IP address"


def set_host(ip):
  try:
    host = socket.gethostbyaddr(ip)[0]
    return host
  except socket.herror:
    return None


def set_result_string(ip, host):
  final_string = "Open ports for"

  if host is not None:
    final_string += " {url} ({ip})".format(url=host, ip=ip)
  else:
    final_string += " {ip}".format(ip=ip)
  final_string += "\n"
  return final_string


def print_verbose(open_ports, result_string):
  header = "PORT     SERVICE\n"
  body = ""
  for port in open_ports:
    service_name = common_ports.ports_and_services.get(port, 'Unknown')
    body += "{p}".format(p=port) + " " * (9 - len(str(port))) + "{s}".format(
        s=service_name)
    if open_ports[len(open_ports) - 1] != port:
      body += "\n"
  return str(result_string + header + body)
