---
code_root: app/planadversity
server: www.planadversity.com
domainname: planadversity.com
mode: Prod
deployment_name: planadversity
locale: en_US.UTF-8
timezone: America/New_York
port_number: 45001
project_repo: https://github.com/powellc/planadversity.git
branch: master
dbpass: lkjsdz;kj89j923lkjsdflKJSDFlkj.dfs  
postgis: False
bower: True
sentry_key: http://5459725bf64840eeb128c7a684b25d0a:0b5e27ca46754e10828d77c55ce01e2b@sentry.onec.me/2
secret_key: ALKJSDFLKXJCOVIJSELKJFEWLKJSLDFKJLEKJ-KLEJWLFEKJ