# SVG Paint

SVG Paint is a paint program.  You log into it. You can paint pictures with custom set paintbrushes.  
You can even save your artwork, load it back up later, and continue where you left off.

# How to Install

### Prerequisites
This project was built on a 64-bit Linux Mint which is a variant on Ubuntu.  Here is what you need to have setup to start.

1.  Oracle VirtualBox.
2.  Git
3.  Ansible
4.  Vagrant
5.  Access to a BASH shell
6.  A web browser that plays well with HTML5.  (This project was tested on Chrome 51)

### Installation steps
1.  In the shell, change directory over to the project directory of your choice.
2.  git clone https://github.com/pcote/basemachine.git
3.  git clone https://github.com/pcote/svgpaint.git
4.  Change directory over to the basemachine project.  There should be a Vagrantfile file there.  This is important.
5. vagrant up.  Go grab a cup of coffee.  This will take a few minutes.
6.  Change directory over to the svgpaint folder.
7.  ./clearknowhosts - This command ensures that clear out the $HOME/.ssh.known_hosts file is cleared for the next step.
8.  ./provisiondev.sh - This will deploy the svgpaint app to the basemachine server.
9.  Open up /etc/hosts on your host machine.  Add the following line: 127.0.0.1       svgpaint.com
10.  Open up a browser and go to http://svgpaint.com:8080

# Usage

##User setup
###Creating a user
Creating a user is simple.  On the login screen, just pick a username and password on the right hand form and hit "Create User".

###Logging In
Logging is is also simple.  Go to the left hand form.  Fill in the username, fill in the password, and log in.
Easy as that.

###Loading and Saving Drawings
#### Saving
1.  Fill in the name of the drawing in the "File Name" field.
2.  In the top menu, click File... -> save.

#### Loading
1.  Fill in the name of the drawing in the "File Name" field that you want to load.
2.  In the top menu, click File... -> load.


