DOCUMENTS = [
    {
        "document_id": 0,
        "title": "Private Tool Customer User Deletion via MySQL",
        "department": "Database Operations",
        "doc_type": "runbook",
        "effective_date": "2025-08-01",
        "is_current": True,
        "text": (
            "To delete a customer user from the Private Tool database upon ticket request: "
            "1. SSH to the Private Tool server and launch MySQL: mysql -u admin -p. "
            "2. Select the mandatory application database: USE domains;. "
            "3. Execute the deletion query: DELETE FROM customers WHERE user_name IN ('target_username');. "
            "4. Verify removal: SELECT * FROM customers WHERE user_name = 'target_username';. "
            "Safety Warning: Always verify you ran 'USE domains;' and double-check SQL syntax before executing DELETE statements."
        ),
    },
    {
        "document_id": 1,
        "title": "eMatrix Tool User Account Deletion via Azure DevOps",
        "department": "DevOps",
        "doc_type": "procedure",
        "effective_date": "2025-09-01",
        "is_current": True,
        "text": (
            "Current workflow for deleting users in eMatrix: "
            "1. Download SQL query attachment from the support ticket. "
            "2. Log in to Azure DevOps portal. "
            "3. Open and edit the eMatrix SQL script file with target parameters. "
            "4. Review SQL syntax carefully, then commit and trigger the execution pipeline. "
            "Safety Warning: Validate all parameters before committing changes."
        ),
    },
    {
        "document_id": 2,
        "title": "Legacy eMatrix User Deletion via SQL Server SSMS",
        "department": "DevOps",
        "doc_type": "old notice",
        "effective_date": "2022-03-15",
        "is_current": False,
        "text": (
            "Legacy process for eMatrix user deletion (retained for historical reference only): "
            "1. RDP to Windows Server 10.245.100.10. "
            "2. Open SQL Server Management Studio (SSMS) from taskbar. "
            "3. Right-click Matrix_db and select New Query. "
            "4. Paste SQL query from ticket Word file and execute (F5). "
            "Notice: This direct access method was replaced in 2025 by Azure DevOps pipeline execution."
        ),
    },
    {
        "document_id": 3,
        "title": "E-Signature Application Server File Deployment",
        "department": "Application Support",
        "doc_type": "procedure",
        "effective_date": "2025-08-15",
        "is_current": True,
        "text": (
            "Deploying files for E-Signature ticketing: "
            "1. Connect to App Server 10.129.134.10 via SSH as root. "
            "2. Locate target destination directory specified in the deployment plan. "
            "3. Transfer and deploy application files via SCP/SFTP. "
            "4. Verify file permissions and ownership post-transfer. "
            "Safety Warning: Always verify target destination directory path before copying files."
        ),
    },
    {
        "document_id": 4,
        "title": "E-Signature Database Maintenance & Backup Execution",
        "department": "Database Operations",
        "doc_type": "runbook",
        "effective_date": "2025-08-20",
        "is_current": True,
        "text": (
            "Running queries for E-Signature ticketing deployments: "
            "1. Connect to DB Server 10.129.199.10 via SSH as root. "
            "2. Take pre-execution backup: mysqldump -u root -p bank_transfer_tickets > /root/backup.sql. "
            "3. Log in to MySQL: mysql -p, then switch DB: USE bank_transfer_tickets;. "
            "4. Execute deployment SQL script. "
            "Safety Warning: Never execute deployment SQL without creating a mysqldump backup first."
        ),
    },
    {
        "document_id": 5,
        "title": "IBM IIB / ACE Environment Topology Discovery",
        "department": "Middleware",
        "doc_type": "guide",
        "effective_date": "2025-09-10",
        "is_current": True,
        "text": (
            "To verify IBM Integration Bus (IIB) and ACE 11 topology: "
            "1. Check dev server 10.129.188.10 or test nodes 10.129.105.10 / 106.10 (LB: 10.129.109.10). "
            "2. On ACE11test1 (10.129.153.10) or test2 (10.129.155.10), log in as mqm user. "
            "3. Execute 'mqsilist' to discover active Queue Managers (MQM1 or MQM2) and Integration Nodes (BRK1 or BRK2). "
            "Use this topology map before initiating deployments or service restarts."
        ),
    },
    {
        "document_id": 6,
        "title": "Remedy MobileBroker Cluster Startup Post-Reboot",
        "department": "Middleware",
        "doc_type": "runbook",
        "effective_date": "2025-09-05",
        "is_current": True,
        "text": (
            "When DC-Linux restarts MobileBroker servers RemdMB-APP1 through APP6 (10.30.196.10-201.10, LB: 10.30.206.10:7800-7805): "
            "1. The broker will be down. Stop queue manager cleanly: endmqm -i MQM. "
            "2. Start queue manager: strmqm MQM1 (or MQM2/MQM depending on host mapping). "
            "3. Start integration broker manually: mqsistart BRK1 -w 600 (or BRK2). "
            "4. Verify status: mqsilist BRK1."
        ),
    },
    {
        "document_id": 7,
        "title": "IBM MQ Queue & Backout Queue Creation",
        "department": "Middleware",
        "doc_type": "procedure",
        "effective_date": "2025-08-25",
        "is_current": True,
        "text": (
            "To define application and backout queues in IBM MQ: "
            "1. Launch MQSC console: runmqsc MQM1. "
            "2. Define backout queue: DEFINE QL(SARESPONSEADPCLEARCACHE.BOQ);. "
            "3. Define local queue with linked backout queue: DEFINE QL(SARESPONSEADPCLEARCACHE) BOQNAME(SARESPONSEADPCLEARCACHE.BOQ);. "
            "4. Enter END to exit MQSC and commit definitions."
        ),
    },
    {
        "document_id": 8,
        "title": "ESB Provider & Gateway Properties Modification",
        "department": "Middleware",
        "doc_type": "procedure",
        "effective_date": "2025-08-10",
        "is_current": True,
        "text": (
            "Updating ESB configuration properties: "
            "1. Navigate to /var/esb/config/. "
            "2. Backup existing property files: cp provider.properties provider.properties.bak && cp gateway.properties gateway.properties.bak. "
            "3. Modify endpoints or timeouts in provider.properties and gateway.properties. "
            "4. Verify changes before saving. "
            "Safety Warning: Always backup property files with date extensions prior to editing."
        ),
    },
    {
        "document_id": 9,
        "title": "IBM IIB Execution Group Inspection & Creation",
        "department": "Middleware",
        "doc_type": "guide",
        "effective_date": "2025-09-12",
        "is_current": True,
        "text": (
            "Managing Execution Groups (Integration Servers): "
            "1. List execution groups: mqsilist BRK1. "
            "2. Check running applications: mqsilist BRK1 -r | grep running > /home/mqm/running_apps.txt. "
            "3. Find which execution group hosts an adapter: for i in `mqsilist BRK1 | awk '{print $4}' | cut -f 2 -d \"'\"`; do mqsilist BRK1 -e $i; done | grep -i SAResponseAdapter. "
            "4. Create new execution group: mqsicreateexecutiongroup BRK1 -e EXEC_GROUP_NAME."
        ),
    },
    {
        "document_id": 10,
        "title": "IBM IIB BAR File Deployment & Flow Monitoring",
        "department": "Middleware",
        "doc_type": "runbook",
        "effective_date": "2025-09-15",
        "is_current": True,
        "text": (
            "Deploying BAR application archive files: "
            "1. Locate deployed path: mqsilist BRK1 -e WSAdapterRSA -k SAResponseAdapter -d2 | grep Deployed. "
            "2. Backup current deployed BAR archive in backup directory. "
            "3. Deploy new BAR file: mqsideploy BRK1 -e WSAdapterRSA -a SAResponseAdapterWithCache.bar -w 600. "
            "4. Activate flow monitoring: mqsichangeflowmonitoring BRK1 -e WSAdapterRSA -c active -k SAResponseAdapter."
        ),
    },
    {
        "document_id": 11,
        "title": "SOAP Web Service Verification via cURL",
        "department": "Middleware",
        "doc_type": "procedure",
        "effective_date": "2025-07-20",
        "is_current": True,
        "text": (
            "Testing ESB SOAP endpoints post-deployment: "
            "1. Upload payload FILE.xml to user home directory. "
            "2. Execute curl SOAP request: curl --header 'Content-Type: text/xml;charset=UTF-8' "
            "--header 'SOAPAction:http://webservices.company.internal/MWInterface/modify' "
            "--header 'Accept-Encoding: gzip,deflate' --data @FILE.xml [suspicious link removed] -k. "
            "3. Review HTTP response code and XML response body for SOAP faults."
        ),
    },
    {
        "document_id": 12,
        "title": "IBM ACE LDAP System Log Inspection",
        "department": "Middleware",
        "doc_type": "procedure",
        "effective_date": "2025-09-02",
        "is_current": True,
        "text": (
            "Triage LDAP authentication errors on ACE servers: "
            "1. Connect to ACE node (e.g., ACE11test2) as mqm user. "
            "2. Tail system messages filtering for LDAP events: tail -300 /var/log/messages | grep -i ldap. "
            "3. Inspect connection timeouts, bind failures, or invalid credential responses from directory server."
        ),
    },
    {
        "document_id": 13,
        "title": "IBM IIB Integration Node Full Backup",
        "department": "Middleware",
        "doc_type": "procedure",
        "effective_date": "2025-08-30",
        "is_current": True,
        "text": (
            "Creating backup archives of integration nodes: "
            "1. Log in as mqm user to the broker host. "
            "2. Execute broker backup command: mqsibackupbroker BRK1 -d /var/mqsi/backups/. "
            "3. Verify creation of the generated .zip backup file containing broker configuration, deployed flows, and metadata."
        ),
    },
    {
        "document_id": 14,
        "title": "Emergency Outage API Disablement in ESB",
        "department": "Middleware",
        "doc_type": "runbook",
        "effective_date": "2025-09-18",
        "is_current": True,
        "text": (
            "Disabling a failing API endpoint during production incidents: "
            "1. Confirm Eventum / CR change ticket number to identify exact property mapping. "
            "2. Navigate to /var/esb/config/ and backup providers.properties. "
            "3. Edit providers.properties: search for the target service (e.g., operational_status). "
            "4. Invalidate the URL (e.g., modify protocol http->https, change destination port or IP). "
            "Safety Warning: Always backup providers.properties before altering production routing."
        ),
    },
    {
        "document_id": 15,
        "title": "IBM MQ /var/mqm 100% Full Disk Space Recovery",
        "department": "Storage",
        "doc_type": "runbook",
        "effective_date": "2025-09-08",
        "is_current": True,
        "text": (
            "P1 Emergency Recovery when /var/mqm is at 100% disk usage: "
            "1. Request DC-Linux to take a 5-day VM snapshot of the server immediately. "
            "2. Inspect errors directory: cd /var/mqm/errors/ && du -sh * 2>/dev/null | grep G. "
            "3. Delete space-consuming FDC files (e.g., rm -rf AMQ7247.0.FDC). "
            "4. Export queue definitions: dmpmqcfg -m MQM > MQM_backup.mqsc. "
            "5. Stop broker and QM: mqsistop -i BRK1 && endmqm -i MQM. "
            "6. Restart QM and broker: strmqm MQM && mqsistart BRK1 -w 600. "
            "7. Restore queues if necessary: runmqsc MQM < MQM_backup.mqsc."
        ),
    },
    {
        "document_id": 16,
        "title": "Force-Killing Unresponsive IBM MQ Queue Manager Processes",
        "department": "Middleware",
        "doc_type": "runbook",
        "effective_date": "2025-09-08",
        "is_current": True,
        "text": (
            "When endmqm hangs or fails to terminate Queue Manager: "
            "1. Inspect active MQ processes: ps -ef | grep mqm. "
            "2. Identify the amqzxma0 process ID (e.g., PID 79895). "
            "3. Terminate process: kill -9 79895. "
            "4. Verify process termination: ps -ef | grep 79895. "
            "5. Re-run endmqm -i MQM to clear internal shared memory locks. "
            "6. Check status: dspmq -m MQM (reports 'Ended unexpectedly'). "
            "7. Start QM cleanly: strmqm MQM."
        ),
    },
    {
        "document_id": 17,
        "title": "TE-Broker Message Flow Restart Post-Reboot",
        "department": "Middleware",
        "doc_type": "procedure",
        "effective_date": "2025-08-28",
        "is_current": True,
        "text": (
            "Restarting core flows on TE-Broker nodes (.35, .36, .40, .41): "
            "1. Restart ManageTicket flow: mqsistopmsgflow BRK1 -e ManageTicket && mqsistartmsgflow BRK1 -e ManageTicket. "
            "2. Restart SubmitProductOrder flow: mqsistopmsgflow BRK1 -e SubmitProductOrder && mqsistartmsgflow BRK1 -e SubmitProductOrder. "
            "3. Verify flow status is active via mqsilist."
        ),
    },
    {
        "document_id": 18,
        "title": "Linux Middleware Log File Truncation (Zero-Byte Release)",
        "department": "Storage",
        "doc_type": "procedure",
        "effective_date": "2025-09-04",
        "is_current": True,
        "text": (
            "Reclaiming disk space on active log files without breaking open file descriptors: "
            "1. Check disk utilization: df -h /var/mqsi. "
            "2. Navigate to component directory: cd /var/mqsi/components/BRK1/<uuid>/. "
            "3. Check file size: ls -lhrt stdout (e.g., 15G stdout). "
            "4. Empty file to 0 bytes safely: truncate -s 0 stdout. "
            "Safety Warning: Never use 'rm' on an actively written stdout file; active processes will retain the deleted inode and disk space will not free."
        ),
    },
    {
        "document_id": 19,
        "title": "Apache Tomcat catalina.out Log Rotation & Compression",
        "department": "Storage",
        "doc_type": "runbook",
        "effective_date": "2025-08-18",
        "is_current": True,
        "text": (
            "Managing Tomcat disk space and log growth: "
            "1. Identify partition usage using df -h and find large logs: du -sh * 2>/dev/null | grep G. "
            "2. Navigate to /opt/tomcat/apache-tomcat-[version]/logs/. "
            "3. Move active log: mv catalina.out catalina.out.$(date +%F). "
            "4. Restart Tomcat: sudo systemctl restart tomcat. "
            "5. Compress rotated log in background: gzip catalina.out.$(date +%F) &. "
            "6. Verify recovered space with df -h."
        ),
    },
    {
        "document_id": 20,
        "title": "SSL/TLS Certificate Import into Java TrustStore (cacerts)",
        "department": "Security",
        "doc_type": "procedure",
        "effective_date": "2025-09-14",
        "is_current": True,
        "text": (
            "Importing an external partner certificate into Java cacerts: "
            "1. Upload certificate file Cert_Name.cer to target home directory. "
            "2. Import certificate using keytool: keytool -import -alias 'TargetServiceCert' -keystore /path/to/jre/lib/security/cacerts -file ~/Cert_Name.cer -storepass changeit -noprompt. "
            "3. Restart dependent application service (e.g., sudo systemctl restart tomcat). "
            "Safety Warning: Always specify a unique alias to prevent overwriting existing certificates."
        ),
    },
    {
        "document_id": 21,
        "title": "Remote SSL/TLS Certificate Extraction via OpenSSL",
        "department": "Security",
        "doc_type": "procedure",
        "effective_date": "2025-09-11",
        "is_current": True,
        "text": (
            "Extracting public certificates from remote HTTPS service endpoints: "
            "1. Test network connectivity: nc -v target_ip target_port. "
            "2. Connect and extract PEM certificate block: openssl s_client -connect target_ip:target_port 2>/dev/null </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > Cert_Name.cer. "
            "3. Inspect certificate validity: openssl x509 -in Cert_Name.cer -text -noout. "
            "4. Deliver Cert_Name.cer to integration team."
        ),
    },
    {
        "document_id": 22,
        "title": "ADSL Portal IIS Service Verification Post-Maintenance",
        "department": "Windows Administration",
        "doc_type": "checklist",
        "effective_date": "2025-08-22",
        "is_current": True,
        "text": (
            "Verifying ADSL Portal post-Windows update: "
            "1. RDP to ADSL Portal Node 1 (10.249.10.10) and Node 2 (10.249.11.10). "
            "2. Open IIS Manager (inetmgr). "
            "3. Verify World Wide Web Publishing Service is running. "
            "4. Verify all hosted application pools and portal websites show status 'Started'."
        ),
    },
    {
        "document_id": 23,
        "title": "ADSL Task Scheduler Maintenance Window Adjustment",
        "department": "Windows Administration",
        "doc_type": "runbook",
        "effective_date": "2025-08-22",
        "is_current": True,
        "text": (
            "Adjusting scheduled tasks on ADSL Web Node 1 (10.249.15.10) and Node 2 (10.249.16.10): "
            "1. Open Task Scheduler (taskschd.msc). "
            "2. Modify triggers for 'Automation' (24-hour cycle) and 'Automation-Other' (12-hour cycle). "
            "3. Align task start times to the nearest appropriate post-patching maintenance window. "
            "4. Example: If updates end at 9 PM on 29/7, set Automation to 8 PM on 30/7 and Automation-Other to 5 AM on 30/7."
        ),
    },
    {
        "document_id": 24,
        "title": "BMC Remedy Application & Email Engine Maintenance Sequencing",
        "department": "Windows Administration",
        "doc_type": "runbook",
        "effective_date": "2025-09-07",
        "is_current": True,
        "text": (
            "Managing services during Windows updates on Remedy servers CSAPPINTGPRD1-3 (10.66.165.10-167.10): "
            "1. Stop BMC Action Request System Server. "
            "2. Stop BMC Remedy Email Engine. "
            "3. Stop Apache Tomcat 9.0 Tomcat9. "
            "4. Release server to DC-Win for reboot. "
            "5. Post-reboot: Start AR System Server, start Email Engine, and restart Apache Tomcat 9.0. "
            "Safety Warning: If services started automatically post-reboot, do NOT restart AR System; only Tomcat must be restarted."
        ),
    },
    {
        "document_id": 25,
        "title": "BMC Remedy Web & Smart Reporting Maintenance Sequencing",
        "department": "Windows Administration",
        "doc_type": "runbook",
        "effective_date": "2025-09-07",
        "is_current": True,
        "text": (
            "Managing services during Windows updates on Remedy Web and Reporting tiers: "
            "1. On CSWEBINTGPRD1-5 (10.66.37.10-41.10) and CSWEBPRD1-5 (10.66.5.10-9.10), stop Apache Tomcat 9.0 Tomcat9 before reboot. "
            "2. On Smart Reporting servers CSRPTPRD1-3 (10.66.101.10-103.10), stop BMC Smart Reporting service before reboot. "
            "3. Following server reboot, start services and restart Tomcat 9.0."
        ),
    },
    {
        "document_id": 26,
        "title": "SiteScope Middleware Network Connectivity & Port Triage",
        "department": "Network",
        "doc_type": "runbook",
        "effective_date": "2025-09-16",
        "is_current": True,
        "text": (
            "Triaging SiteScope telnet/network error alerts: "
            "1. Log in to source monitor host IBM-IIB-PreProd-2 (10.129.36.10). "
            "2. Test port connectivity matching the alert target: "
            "nc -v 10.247.18.10 80 (OMS), nc -v 10.247.91.10 80 (Matrix), nc -v 10.143.228.10 1521 (MW DB), "
            "nc -v 10.131.3.10 443 (CSO), or nc -v 10.246.105.10 443 (WEPG). "
            "3. If connection times out or fails, reply to ticket and notify Network Security: 'Access not working from our side'."
        ),
    },
    {
        "document_id": 27,
        "title": "SiteScope ADSL Hop Gateway Ping Triage",
        "department": "Network",
        "doc_type": "runbook",
        "effective_date": "2025-09-16",
        "is_current": True,
        "text": (
            "Triaging SiteScope ping failure alerts from ADSL-WEB4 (10.249.16.10) to Hop IP 10.16.144.98: "
            "1. Log in to 10.249.16.10 via SSH or RDP. "
            "2. Run ICMP ping test: ping 10.16.144.98. "
            "3. If packet loss occurs, trace route with tracert / traceroute to isolate network gateway drop. "
            "4. Escalate to Network Operations with hop failure point."
        ),
    },
    {
        "document_id": 28,
        "title": "IVR Application FBB.war Cluster Rollout",
        "department": "Deployments",
        "doc_type": "runbook",
        "effective_date": "2025-08-20",
        "is_current": True,
        "text": (
            "Deploying updated FBB.war to IVR production clusters: "
            "1. Download FBB.war from test node CC-IVRAPP01 (10.0.81.10). "
            "2. Backup current WAR on all prod nodes (CC-IVRAPP02 through CC-IVRAPP22): cp FBB.war FBB.war.$(date +%F). "
            "3. Upload new FBB.war to seed node 10.0.82.10 and distribute via SCP to /opt/tomcat/apache-tomcat-9.0.8/webapps/ on all cluster nodes. "
            "4. Restart Tomcat on each node: sudo systemctl restart tomcat.service. "
            "Safety Warning: Always backup the existing WAR file across all nodes before distributing the new artifact."
        ),
    },
    {
        "document_id": 29,
        "title": "IVR Application FBB.war Cluster Rollback",
        "department": "Deployments",
        "doc_type": "runbook",
        "effective_date": "2025-08-20",
        "is_current": True,
        "text": (
            "Rolling back failed FBB.war deployment on IVR clusters: "
            "1. On all prod nodes CC-IVRAPP02 to CC-IVRAPP22, navigate to /opt/tomcat/apache-tomcat-9.0.8/webapps/. "
            "2. Restore previous backup: mv FBB.war.<backup_date> FBB.war. "
            "3. Restart Tomcat: sudo systemctl restart tomcat.service. "
            "4. Check catalina.out to confirm clean application context initialization."
        ),
    },
    {
        "document_id": 30,
        "title": "IVR Audio Prompts, Configs & Shared Library Deployment",
        "department": "Deployments",
        "doc_type": "runbook",
        "effective_date": "2025-08-26",
        "is_current": True,
        "text": (
            "Deploying IVR assets across cluster nodes: "
            "1. Prompts: scp prompt folders to /opt/tomcat/ivrprompts/. "
            "2. Configs: scp JSON configs to /opt/tomcat/ivrconfig/. "
            "3. Shared Libraries: In /opt/tomcat/ivrlib/, backup we-integeration.jar and we-client.jar, then scp updated JARs from source server 10.2.39.10. "
            "4. Perform rolling Tomcat restart node by node: sudo /opt/tomcat/apache-tomcat-9.0.91/bin/shutdown.sh && sudo startup.sh."
        ),
    },
    {
        "document_id": 31,
        "title": "Legacy Direct Root SSH Access Policy 2022",
        "department": "Security",
        "doc_type": "old notice",
        "effective_date": "2022-01-10",
        "is_current": False,
        "text": (
            "Historical notice on server administrative access: "
            "Under the 2022 server access guidelines, administrators connected directly to Linux hosts using root SSH on port 22 with static keys. "
            "Notice: This policy is obsolete. Effective 2025, direct root SSH on port 22 is disabled; all connections must route through Teleport bastion hosts on port 2222 with MFA."
        ),
    },
]