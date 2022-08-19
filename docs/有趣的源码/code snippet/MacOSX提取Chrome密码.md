# macOS提取chrome密码

`Login Data`文件一般位于`~/Library/Application Support/Google/Chrome/Default/Login Data`

需要注意,当chrome在运行时`Login Data`将处于占用状态,无法直接读取.可以先将此文件复制出来.

账号密码存储在`logins`中,其数据结构如下:

![](/assets/images/MacOSX提取Chrome密码/2022-08-19-16-53-20.png)

手动获取加密串的方法:

![](/assets/images/MacOSX提取Chrome密码/2022-08-19-17-00-55.png)

获取获取加密串之后,将其赋值给`security`,后续不用改动代码


```py3
import hashlib
import os
import sqlite3
import binascii
import base64
import subprocess

db = sqlite3.connect("Login Data")

with db:
    cur = db.execute("select origin_url,username_value,password_value from logins;")
    values = cur.fetchall()
security = os.popen("security find-generic-password -wa 'Chrome'").read().replace("\n", "")
# 此处会弹出密码输入确认,需要输入两次密码,或者在第一次输入之后点击始终信任,则后续不需要再输入密码
key = hashlib.pbkdf2_hmac("sha1", security.encode(), b"saltysalt", 1003)[:16]
# salt混淆串一般固定为saltysalt,除非后续chrome更改此内容
hex_key = binascii.hexlify(key)
iv = ''.join(('20', ) * 16)


def decrypt(hex_enc_password)->str:

    try:
        command = "openssl enc -base64 -d -aes-128-cbc -iv '{}' -K {} <<< {} 2>/dev/null".format(iv, hex_key.decode(), hex_enc_password.decode())
        decrypted = os.popen(command).read()
    except subprocess.CalledProcessError:
        decrypted = "n/a"
    return decrypted

for web, user, pwd in values:
    # pwd_b64 = base64.b64encode(pwd)
    # command = f"openssl enc -base64 -d -aes-128-cbc -v {iv} '{key.decode()}' -K '{pwd_b64.decode()}'"
    # pwd_str = os.popen(command).read()
    pwd_b46 = base64.b64encode(pwd[3:])
    if pwd_b46:
        pwd_str = decrypt(pwd_b46)
    else:
        pwd_str = ""
    print(f"url:{web}\n\tU:{user}\n\tP:{pwd_str}")
```