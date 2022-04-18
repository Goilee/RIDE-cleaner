import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler


def docker_remove(id):
    cmd = f'docker rm -f {id}'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-1]
    print(result)
    return result

# возвращает номер последней строки, содержащей подстроку line
def find_last_line_in_logs(container, substr):
    cmd = f'''docker logs {container} 2>&1 | grep -n "{substr}" | tail --lines=1'''
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")
    lineNumber = int(result[0:result.index(':')])
    return lineNumber


def cleaner(container):
    clientEnter = find_last_line_in_logs(container, "Set client")
    clientExit = find_last_line_in_logs(container, "All contributions have been stopped")
    if (clientExit > clientEnter):
        print("REMOVED")
        docker_remove(conteiner)


conteiner = "ride"

scheduler = BlockingScheduler()
scheduler.add_job(cleaner, 'interval', [conteiner], seconds=1)
scheduler.start()
