import datetime
import os
import subprocess

project = 'secret_santa'
image_name = ''


def build_image(env, date):
    image_file = image_name + ':' + env + '__' + date

    docker_file = f'docker/{env}.Dockerfile'

    os.system(f"docker build -t {image_file} -f {docker_file} .")
    os.system(f"docker push {image_file}")

    return image_file


result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
branch = result.stdout.decode('utf-8').strip()

os.system(f"git pull")

date = datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')

links = []
for type_of_image in ['api', 'telegram_bot']:
    image_link = build_image(type_of_image, date)
    links.append(image_link)

for link in links:
    print('====================================')
    print(f"\033[94m Update the Rancher IMAGE: {link} \033[0m")
    print('====================================')
