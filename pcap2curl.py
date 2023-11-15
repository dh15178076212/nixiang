import json
import sys, os
from scapy.all import PcapReader, re, Raw, TCP

if os.path.exists('./curl_POST.txt'):
    os.remove('./curl_POST.txt')
if os.path.exists('./curl_GET.txt'):
    os.remove('./curl_GET.txt')

if os.path.exists('./error.txt'):
    os.remove('./error.txt')

curl_GET = open('./curl_GET.txt', 'a', encoding='utf-8')
curl_POST = open('./curl_POST.txt', 'a', encoding='utf-8')
error = open('./error.txt', 'a', encoding='utf-8')

VALID_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH"
]  # see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods


def md_get(url, lines, method='GET'):
    headers = []
    host_name = ''
    for line in lines:
        if ":" in line:
            headers.append("-H '{}'".format(line))
        if "Host:" in line:
            host_header = re.search("^Host: (.*)", line)
            host_name = host_header.group(1)

    proto_host = 'http://{}/'.format(host_name)
    if not url.startswith(proto_host):
        url = "{}{}".format(proto_host, url[1:] if url[0] == "/" else url)
    curl = "curl '{}' \\\n -X {} \\\n ".format(url, method)
    curl += " \\\n ".join(headers)
    return curl


def md_post(url, lines, method='POST'):
    headers = []
    host_name = ''
    parsms = ''
    for line in lines:

        if "Host:" in line:
            host_header = re.search("^Host: (.*)", line)
            host_name = host_header.group(1)
            continue
        if ": " in line:
            headers.append("-H '{}'".format(line))
            continue
        else:
            try:
                json.loads(line) # 报错则表示为 data
                parsms = "--json " + f"\'{line}\'"
            except:
                parsms = "--data-raw " + "\"" + line + "\""

    proto_host = 'http://{}/'.format(host_name)
    # if 'searchCompanyV3' in url:
    #     print()
    if not url.startswith(proto_host):
        url = "{}{}".format(proto_host, url[1:] if url[0] == "/" else url)
    curl = "curl '{}' \\\n -X {} \\\n ".format(url, method)
    curl += " \\\n ".join(headers)
    curl += " \\\n " + parsms
    return curl


def payload2curl(p):
    # list(filter(lambda x : x > 31 and x < 127, [i for i in p]))
    lines = re.compile("[\n\r]+").split(p.decode('utf-8'))
    # print('lines = ', lines)
    start_line = re.search("^([A-Z]+) ([^ ]+) (HTTP\/[0-9\/]+)", lines[0])
    method = start_line.group(1)
    url = start_line.group(2)
    version = start_line.group(3)  # Never used

    if method not in VALID_METHODS:
        return

    del lines[0]
    if method == 'GET':
        cmd = md_get(url, lines)
        curl_GET.write(cmd)
        curl_GET.write('\n\n')
        return cmd
    if method == 'POST':
        cmd = md_post(url, lines)
        curl_POST.write(cmd)
        curl_POST.write('\n\n')
        return cmd


def main(infile, port):
    with PcapReader(infile) as packets:
        for p in packets:
            if p.haslayer(TCP) and p.haslayer(Raw) and p[TCP].dport == port:
                payload = p[Raw].load
                try:
                    cmd = payload2curl(payload)
                    if cmd:
                        print(cmd)
                        print('\n')
                except:
                    error.write(str(payload))
                    error.write('\n')
                    error.write('\n')
                    continue
    curl_GET.close()
    curl_POST.close()
    error.close()


if __name__ == "__main__":
    # 参数1: 某pcap文件, 参数2: 目标端口
    infile = r"pro.pcap"
    port = 443
    main(infile, port)
