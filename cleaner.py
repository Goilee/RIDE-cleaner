import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

INTERVAL_IN_SECONDS = 300

# удаляет контейнер и возвращает вывод команды
def docker_remove(id):
    cmd = f'docker rm -f {id}'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-1]
    print(f'Removed: {result}')
    return result

# возвращает номер последней строки, содержащей подстроку line
def find_last_line_in_logs(container, substr):
    cmd = f'''docker logs {container} 2>&1 | grep -n "{substr}" | tail --lines=1'''
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")
    try:
        lineNumber = int(result[0:result.index(':')])
        return lineNumber
    except ValueError:
        return -1

# возвращает список айднишников
def get_running_containers():
    cmd = 'docker ps -q --filter "ancestor=ride"'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = process.communicate()[0].decode("utf-8")
    return result.splitlines()

def cleaner():
    for container in get_running_containers():
        clientEnter = find_last_line_in_logs(container, "Set client")
        clientExit = find_last_line_in_logs(container, "All contributions have been stopped")
        print (f'Container {container}: entered {clientEnter}, exited {clientExit}')
        if (clientExit > clientEnter):
            docker_remove(container)

scheduler = BlockingScheduler()
scheduler.add_job(cleaner, 'interval', seconds=INTERVAL_IN_SECONDS)
scheduler.start()
