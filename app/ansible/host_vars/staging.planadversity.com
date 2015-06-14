---
code_root: app/hacklabs
server: staging.hacklabs.me
domainname: hacklabs.me
mode: Stage
deployment_name: hacklabs
locale: en_US.UTF-8
timezone: America/New_York
port_number: 45001
project_repo: http://github.com/powellc/hacklabs.git
branch: master
dbpass: lkjxz;vkjsdaijlaksjdl;kj3
postgis: False
secret_key: LKJSDAELKJELFJKSOIJLPJPWEFLJSDFJEFKJE-EFKJDFXFJJ