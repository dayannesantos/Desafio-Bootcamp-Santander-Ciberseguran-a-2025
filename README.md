# Desafio Bootcamp – Exploração do Metasploitable 2 com Kali Linux & Medusa

## Objetivos do Projeto

- Configurar um laboratório com Kali Linux (atacante) e Metasploitable 2 (alvo).
- Executar ataques simulados de brute-force com Medusa.
- Enumerar e explorar serviços vulneráveis (FTP, SSH, SMB, HTTP, etc).
- Documentar comandos, técnicas e resultados.
- Apresentar recomendações de mitigação para os problemas encontrados.

## Ambiente de Laboratório

- VirtualBox com rede interna (host-only).
- VMs utilizadas:
  - Kali Linux (Atacante)
  - Metasploitable 2 (Alvo)

## Etapas do trabalho

### 1 - Reconhecimento
`nmap -sV -sC -p- 192.168.56.103 -oN scan.txt`

- sV → versão dos serviços
- sC → scripts padrões (NSE)
- -p- → todas as portas
- oN → salva em arquivo

#### Serviços identificados:
| Porta         | Serviço    | Versão / Observação                                  |
| ------------- | ---------- | ---------------------------------------------------- |
| **21/tcp**    | FTP        | vsftpd 2.3.4 (permite login anônimo)                 |
| **22/tcp**    | SSH        | OpenSSH 4.7p1 Debian 8ubuntu1                        |
| **23/tcp**    | Telnet     | Linux telnetd                                        |
| **25/tcp**    | SMTP       | Postfix smtpd (SSLv2 habilitado, VRFY ativado)       |
| **53/tcp**    | DNS        | ISC BIND 9.4.2                                       |
| **80/tcp**    | HTTP       | Apache httpd 2.2.8 (Ubuntu) – Página Metasploitable2 |
| **111/tcp**   | RPCbind    | v2 – associado a serviços NFS e mountd               |
| **139/tcp**   | SMB        | Samba 3.X – NetBIOS-SSN (WORKGROUP)                  |
| **445/tcp**   | SMB        | Samba 3.0.20-Debian (WORKGROUP)                      |
| **512/tcp**   | exec       | netkit-rsh rexecd                                    |
| **513/tcp**   | login      | rlogind (OpenBSD/Solaris)                            |
| **514/tcp**   | shell      | Netkit rshd                                          |
| **1099/tcp**  | Java-RMI   | GNU Classpath grmiregistry                           |
| **1524/tcp**  | bindshell  | Root shell backdoor (intencional no Metasploitable2) |
| **2049/tcp**  | NFS        | Network File System (versões 2-4)                    |
| **2121/tcp**  | FTP        | ProFTPD 1.3.1                                        |
| **3306/tcp**  | MySQL      | MySQL 5.0.51a-3ubuntu5                               |
| **3632/tcp**  | DistCCD    | distccd v1 (compilação distribuída vulnerável)       |
| **5432/tcp**  | PostgreSQL | 8.3.0 - 8.3.7                                        |
| **5900/tcp**  | VNC        | Protocolo 3.3 (autenticação VNC)                     |
| **6000/tcp**  | X11        | Exposto (access denied, mas detectado)               |
| **6667/tcp**  | IRC        | UnrealIRCd (backdoor conhecido)                      |
| **6697/tcp**  | IRC        | UnrealIRCd (TLS?)                                    |
| **8009/tcp**  | AJP13      | Apache Jserv Protocol v1.3                           |
| **8180/tcp**  | HTTP       | Apache Tomcat/5.5 (Manager App pode estar exposto)   |
| **8787/tcp**  | DRb (Ruby) | Ruby DRb RMI (Ruby 1.8)                              |
| **43202/tcp** | mountd     | RPC mountd 1-3                                       |
| **51473/tcp** | status     | RPC status v1                                        |
| **54071/tcp** | Java-RMI   | GNU Classpath grmiregistry                           |
| **54953/tcp** | nlockmgr   | RPC nlockmgr 1-4                                     |

### 2 - Ataques de Força Bruta (Medusa)
### FTP 2.3.4
`medusa -h 192.168.56.103 -u msfadmin -P small.txt -M ftp`
<img width="1069" height="198" alt="image" src="https://github.com/user-attachments/assets/403126c6-dc5a-4419-b4b3-dcb2ed5939d5" />
#### ✅ Credenciais encontradas: msfadmin:msfadmin
- Login anônimo ativo ✅
- Listagem de diretório possível (mesmo que vazio) ✅
- Permissão de escrita ❌ (não é permitido)
- Backdoor via vsftpd

#### Backdoor via vsftpd
<img width="973" height="295" alt="image" src="https://github.com/user-attachments/assets/79167b3a-2b89-459d-b22b-a2e555549329" />

- Serviço: FTP (vsftpd 2.3.4)
- Exploit usado: exploit/unix/ftp/vsftpd_234_backdoor
- Resultado: Shell remota como root.
- Impacto: Comprometimento total do sistema via backdoor embutido.
- Mitigação: Atualizar o vsftpd para versão corrigida; desabilitar login anônimo.

### SSH
`medusa -h 192.168.56.103 -u msfadmin -P small.txt -M ssh`
<img width="1066" height="197" alt="image" src="https://github.com/user-attachments/assets/8d49bae6-acc1-4a30-b94d-509993ba7428" />
#### ✅ Acesso remoto válido confirmado

### SMB
`enum4linux -a 192.168.56.103 | tee enum4_output.txt `

`medusa -h 192.168.56.103 -U users.txt -p pass.txt -M smbnt`
<img width="1067" height="199" alt="image" src="https://github.com/user-attachments/assets/3aededed-50fc-4e1c-9682-99cd58a83c3d" />
#### ✅ Enumerando usuários do sistema + tentativa de password spraying.

### 3 - Exploração adicional
### HTTP
`dirb http://192.168.56.103 -o result.txt`
#### ✅ Descoberta com dirb + salvando a saída em arquivo

### 4 - Evidências
- Screenshots dos scans (nmap).
- Capturas de acessos bem-sucedidos (FTP, SSH, SMB).

### 5 - Mitigações Recomendadas

- Desabilitar serviços desnecessários (Telnet, FTP anônimo, etc).
- Usar senhas fortes e autenticação multifator.
- Restringir acessos via firewall.
- Manter serviços e pacotes sempre atualizados.
- Segmentar rede para reduzir a superfície de ataque.

### 6 - Conclusão
#### Este laboratório mostrou como um atacante pode:

- Mapear serviços expostos.
- Descobrir credenciais fracas via força bruta.
- Escalar o ataque explorando vulnerabilidades conhecidas.

Mais importante que explorar, foi **documentar e refletir sobre medidas de prevenção** — exatamente o que se espera de um pentester ou analista de segurança.
