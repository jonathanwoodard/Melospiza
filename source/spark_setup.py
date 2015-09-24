# fish function to launch spark cluster:
# spark_cluster
# This will initialize a cluster of 1 master and 19 worker m4.large instances on us west-2.
# The instances can by resized after stopping them - need to be resized individually
# In EC2 console:
#   stop instance
#   select Actions -> Instance Settings -> Change Instance Type
#   restart from terminal with the followin command:
#       /opt/spark/spark-1.4.1-bin-hadoop2.4/ec2/spark-ec2 -k jwoodard-aws-key -i ~/.ssh/jwoodard-aws-key.pem start spark
#   login to cluster
# fish function to log in to spark cluster:
# spark_login

# Need to create script to install automatically, or set up profile for instances

# cluster setup for fft:
#
yum install -y tmux
yum install -y pssh
yum install -y python27 python27-devel
yum install -y freetype-devel libpng-devel
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python27
easy_install-2.7 pip
easy_install py4j

pip2.7 install ipython==2.0.0
pip2.7 install pyzmq==14.6.0
pip2.7 install jinja2==2.7.3
pip2.7 install tornado==4.2

pip2.7 install boto3
pip2.7 install numpy
pip2.7 install sklearn
pip2.7 install scipy

# Install on workers:

pssh -h /root/spark-ec2/slaves yum install -y python27 python27-devel
pssh -h /root/spark-ec2/slaves "wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python27"
pssh -h /root/spark-ec2/slaves easy_install-2.7 pip
pssh -h /root/spark-ec2/slaves pip2.7 install boto3
pssh -t 10000 -h /root/spark-ec2/slaves pip2.7 install numpy
pssh -t 10000 -h /root/spark-ec2/slaves pip2.7 install sklearn
pssh -t 10000 -h /root/spark-ec2/slaves pip2.7 install scipy
#
# Start tmux
tmux new -s notebook
#
# Start ipython notebook
IPYTHON_OPTS="notebook --ip=0.0.0.0" /root/spark/bin/pyspark --executor-memory 4G --driver-memory 4G
