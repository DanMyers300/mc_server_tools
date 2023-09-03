import subprocess

cmd = ['python3', 'mc_server_tools/backup.py']
subprocess.Popen(cmd).wait()
print('Backup complete!')
