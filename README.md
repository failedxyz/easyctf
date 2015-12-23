# EasyCTF 2016

Platform for the EasyCTF 2016 competition.

## Installation

If you have Vagrant installed, setting up the platform should be a piece of cake.

1. Navigate to the root directory of this project.
2. Perform a `vagrant up` to create a virtual machine using the Vagrantfile.
3. Perform a `vagrant ssh` to SSH into the virtual machine.
4. Once you're inside the virtual machine, run `deploy` to start the server.
5. Open [localhost:8080](http://localhost:8080) on your local machine to see if it works.

If you have any issues during installation, file an issue.

## Notes

**Resources** : Flask, MySQL


Main Pages:
- login.html
- register.html
- scoreboard.html
- problems.html
- account.html
- programming.html
- chat.html
- about.html
- forgot_password.html
- logout.html
- rules.html
- team.html
- shell.html
- updates.html
- resetpassword.html

Color Scheme: &#35;69D2E7 | &#35;A7DBDB | &#35;E0E4CC | &#35;F38630 | &#35;FA6900

Setting Up The Environment
----------
1. Download [VirtualBox](https://www.virtualbox.org) and [Vagrant](https://www.vagrantup.com)
2. Run `vagrant up` to create the Virtual Machine according to `Vagrantfile`
3. Run `vagrant ssh` to connect to the Virtual Machine
4. Run `./deploy` to deploy the site
5. View the site on port 8000
