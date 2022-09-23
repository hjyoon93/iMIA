from flask import Flask, request, render_template
import glob
import os
import json
import datetime

white_list = [{'src': '192.168.100.40'  , 'dst': '192.168.100.115', 'port': '502'},
              {'src': '192.168.100.40', 'dst': '192.168.100.5', 'port' : '502' },
              {'src': '192.168.100.12', 'dst': '192.168.100.40', 'port' : '502' },
              {'src': '192.168.100.10', 'dst': '192.168.100.5', 'port': '2404'},
              {'src': '192.168.100.45', 'dst': '192.168.100.5', 'port': '44818'}
             ]

mac_addr = [{'ip' : '192.168.100.40', 'mac' :'00:80:f4:14:f2:32'},
            {'ip' : '192.168.100.115', 'mac' :'00:01:23:3e:86:3c'},
            {'ip' : '192.168.100.5', 'mac' : '00:0d:48:31:c4:fe'},
            {'ip' : '192.168.100.45', 'mac' : '00:0f:73:00:0f:51'},
            {'ip' : '192.168.100.10', 'mac' : '00:80:f4:15:2b:0f'}
            ]

prev_port = 0
orig_port = 0
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('network.html')

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/viewnode', methods = ['GET'])
def viewnode():
    node = request.args.get('node')
    list_of_files = glob.glob('./logs/events/*.log')
    protocs = {"TCP":0,"UDP":0,"DNS":0,"DHCP":0,"ICMP":0,"ModbusTCP":0,"CIP":0,"IEC104":0,"Others":0}
    latest_file = max(list_of_files, key=os.path.getctime)
    events_lines = []
    with open(latest_file,"r") as f:
        line = f.readline()
        while line:
            src_ip = line.split(",")[1]
            dst_ip = line.split(",")[2]
            # print(ip, node)
            if str(src_ip)==str(node) or str(dst_ip)==str(node):
                events_lines.append(line.split(",")[-2])
            line = f.readline()
    # lines = lines[::-1]
    for line in events_lines:
        if line in protocs.keys():
            protocs[line]+=1
        else:
            protocs["Others"]+=1
    
    for key, value in protocs.items():
        protocs[key] = round((protocs[key]/len(events_lines))*100)
    print(protocs)
    return render_template('viewnode.html', node=node, protocs=protocs)

@app.route('/3d')
def three():
    return render_template('index.html')

@app.route('/lineCharts')
def lineCharts():
    return render_template('live.html')

@app.route('/pie')
def pie():
    global prev_port
    global orig_port
    list_of_files = glob.glob('./logs/incidents/*.log') 
    latest_file = max(list_of_files, key=os.path.getctime)
    alert_file = './logs/incidents/alert.csv'
    incidents_lines = []
    malicious_events = {"TCP":0,"UDP":0,"DNS":0,"DHCP":0,"ICMP":0,"ModbusTCP":0,"CIP":0,"IEC104":0,"Others":0}
    normal_events = {"TCP":0,"UDP":0,"DNS":0,"DHCP":0,"ICMP":0,"ModbusTCP":0,"CIP":0,"IEC104":0,"Others":0}
    with open(latest_file,"r") as f:
        line = f.readline()
        while line:
            incidents_lines.append(line.split(",")[-1][:-1])
            line = f.readline()
    with open(alert_file,"r") as f:
        line = f.readline()
        while line:
            words = line.split(',')
            flag = 0
            if len(words)>0 and words[0]!='':
                for __ in mac_addr:
                    if (words[0] == __['ip'] and words[6]!=['mac']) or (words[2] == __['ip'] and words[7] != __['mac']):
                        inci =  words[-1]
                        lines.append(inci)
                        flag = 1
                
                if flag == 1:
                    line = f.readline()
                    continue

                for _ in white_list:
                    if words[0] == _['src'] and words[2] == _['dst'] and words[1] == _['port'] or words[0] == _['src'] and words[2] == _['dst'] and words[3] == _['port'] or   words[2] == _['src'] and words[0] == _['dst'] and words[1] == _['port'] or words[2] == _['src'] and words[0] == _['dst'] and words[3] == _['port']:
                        flag = 1
                        break
                
                if words[0] == '192.168.100.12' and words[2] == '192.168.100.40' or words[0] == '192.168.100.40' and words[2] == '192.168.100.12':
                    if prev_port == 0:
                        prev_port = orig_port = words[1] if words[1]!='502' else words[3]
                    else:
                        tmp = words[1] if words[1]!='502' else words[3]
                        print(tmp, prev_port, orig_port)
                        if prev_port != tmp and tmp == orig_port:
                            inci = words[-1]
                            lines.append(inci)
                        prev_port = tmp

                if flag == 0:
                    if(words[1] == '502' or words[3] == '502'):
                        words[-1] = 'ModbusTCP'
                    elif(words[1] == '2404' or words[3] == '2404'):
                        words[-1] = 'IEC104'
                    elif(words[1] == '44818' or words[3] == '44818'):
                        words[-1] = 'CIP'
                    inci = words[-1]
                    lines.append(inci)
            line = f.readline()
    for line in incidents_lines:
        # print(line)
        if line in malicious_events.keys():
            malicious_events[line]+=1
        else:
            malicious_events["Others"]+=1
    
    # malicious_events = malicious_events/len(incidents_lines)
    list_of_files = glob.glob('./logs/events/*.log') 
    latest_file = max(list_of_files, key=os.path.getctime)
    events_lines = []
    with open(latest_file,"r") as f:
        line = f.readline()
        while line:
            events_lines.append(line.split(",")[-2])
            line = f.readline()
    # lines = lines[::-1]
    for line in events_lines:
        if line in normal_events.keys():
            normal_events[line]+=1
        else:
            normal_events["Others"]+=1
    
    try:
        for key, value in malicious_events.items():
            malicious_events[key] = malicious_events[key]/len(incidents_lines)
    except:
        pass
    for key, value in normal_events.items():
        normal_events[key] = normal_events[key]/len(events_lines)
    print(malicious_events)
    print(normal_events)
    return render_template('pie.html', malicious_events=malicious_events, normal_events=normal_events)
    
@app.route('/incidents')
def incidents():
    global prev_port
    global orig_port
    list_of_files = glob.glob('./logs/incidents/*.log') 
    alert_file = "./logs/incidents/alert.csv"
    latest_file = max(list_of_files, key=os.path.getctime)
    lines = []
    prev = []
    with open(latest_file,"r") as f:
        line = f.readline()
        line = line.rstrip()
        count = 1
        while line:
            k = line.split(",")
            if k[1:] == prev[1:]:
                count += 1
                prev = k
            elif len(prev)==0:
                prev = k
            elif k[1:] != prev[1:]:
                print(k[1:], prev[1:])
                prev[0] += " ==>" + str(count)
                lines.append(prev)
                prev = k
                count = 1
            
            line = f.readline()
            line = line.rstrip()
        if len(prev) != 0:
            prev[0] += " ==>" + str(count)
            lines.append(prev)
    # print(lines)
    alert_lines = [] 
    with open(alert_file,"r") as f:
        line = f.readline()
        # print(line)
        while line:
            words = line.split(',')
            flag = 0
            if len(words)>0 and words[0]!='':
                for __ in mac_addr:
                    if (words[1] == __['ip'] and words[7]!=['mac']) or (words[3] == __['ip'] and words[8] != __['mac']):
                        inci = [words[1], words[3], "Possible IP spoofing", words[6]]
                        alert_lines.append(inci)
                        flag = 1
                
                if flag == 1:
                    line = f.readline()
                    continue

                for _ in white_list:
                    if words[1] == _['src'] and words[3] == _['dst'] and words[2] == _['port'] or words[1] == _['src'] and words[3] == _['dst'] and words[4] == _['port'] or   words[3] == _['src'] and words[1] == _['dst'] and words[2] == _['port'] or words[3] == _['src'] and words[1] == _['dst'] and words[4] == _['port']:
                        flag = 1
                        break
                
                if words[1] == '192.168.100.12' and words[3] == '192.168.100.40' or words[1] == '192.168.100.40' and words[3] == '192.168.100.12':
                    if prev_port == 0:
                        prev_port = orig_port = words[2] if words[2]!='502' else words[4]
                    else:
                        tmp = words[2] if words[2]!='502' else words[4]
                        # print(tmp, prev_port, orig_port)
                        if prev_port != tmp and tmp == orig_port:
                            inci = [words[1], words[3], "Possible MITM (Port Change)", words[6]]
                            alert_lines.append(inci)
                        prev_port = tmp

                if flag == 0:
                    if(words[2] == '502' or words[4] == '502'):
                        words[-1] = 'ModbusTCP'
                    elif(words[2] == '2404' or words[4] == '2404'):
                        words[-1] = 'IEC104'
                    elif(words[2] == '44818' or words[4] == '44818'):
                        words[-1] = 'CIP'
                    inci = [words[0],words[1], words[3], words[5], words[6]]
                    alert_lines.append(inci)
            line = f.readline()
    # print(alert_lines)
    prev = []
    count = 1
    for alert_line in alert_lines:
        if alert_line[1:] == prev[1:]:
            count += 1
            prev = alert_line
        elif len(prev)==0:
            prev = alert_line
        elif alert_line[1:] != prev[1:]:
            # print(alert_line[1:], prev[1:])
            prev[0] += " ==>" + str(count)
            lines.append(prev)
            prev = alert_line
            count = 1
    if len(prev)!=0:
        prev[0] += " ==>" + str(count)
        lines.append(prev)
    
    date = []
    for i in lines:
        date.append(i[0])
    lines.sort(key=lambda date: date)
    # print(lines)
    lines = lines[::-1]
    return render_template('incidents.html', data=lines)

@app.route('/events')
def events():
    list_of_files = glob.glob('./logs/events/*.log') 
    latest_file = max(list_of_files, key=os.path.getctime)
    lines = []
    with open(latest_file,"r") as f:
        line = f.readline()
        while line:
            lines.append(line.split(","))
            line = f.readline()
    lines = lines[::-1]
    return render_template('events.html', data=lines)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=False)