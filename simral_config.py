USERNAME="gilang_2021"
PASSWORD="1234567a"
database="2021"

SIMRAL_URL="https://simral.bogorkab.go.id/2021/"

"""
FORM DATA Login SIMRAL
login: Login
lived_cfg: appl_config_bogorkab_2021.php
nama_login: gilang_2021
password: 1234567a
captcha_code: 7
"""

"""
HOME HEADER
POST /2021/ HTTP/1.1
Host: simral.bogorkab.go.id
Connection: keep-alive
Content-Length: 107
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: https://simral.bogorkab.go.id
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://simral.bogorkab.go.id/2021/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=rrn3b13l9rh4cgr4qi9gh08n44
"""

CAPTCHA_JS_CONVERT="""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = 100; cnv.height = 40;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """