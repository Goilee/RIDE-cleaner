import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler


def docker_remove(id):
    cmd = f'docker rm -f {id}'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-1]
    print(result)
    return result


def check_closing_logs(conteiner):
    cmd = f'''docker logs {conteiner} 2>&1 | grep "Changed application state from 'ready' to 'closing_window'"'''
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-2]
    result = result[10:]

    return result


def cleaner(conteiner):
    result = check_closing_logs(conteiner)
    print(result)
    if result == "Changed application state from 'ready' to 'closing_window'":
        print("REMOVED")
        docker_remove(conteiner)


conteiner = "471e32e7ff13"

scheduler = BlockingScheduler()
scheduler.add_job(cleaner, 'interval', [conteiner], seconds=1)
scheduler.start()