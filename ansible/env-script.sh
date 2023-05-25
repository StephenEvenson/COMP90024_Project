pip install --upgrade pip
pip install ansible-core==2.14.4 Jinja2==3.1.2 PyYAML==6.0 openstacksdk
pip install -r requirements.txt
ansible-galaxy collection install ansible.posix community.docker community.general openstack.cloud