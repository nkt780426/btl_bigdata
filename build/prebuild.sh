#!/bin/bash
sudo apt-get update
sudo apt-get upgrade -y
sudo update-alternatives --config java

# Cài java, mặc định cài java 17
sudo apt-get install oracle-java17-installer -y
echo "Install java successfully!"
echo "--------------------------------------------------------------------------"

# Cài spark, thay đổi phiên bản bằng cách thay đổi đường dẫn sau
SPARK_URL="https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz"
SPARK_TGZ="spark-3.5.0-bin-hadoop3.tgz"
wget $SPARK_URL
tar -xvzf $SPARK_TGZ
rm $SPARK_TGZ
echo "Install apache spark successfully!"
echo "--------------------------------------------------------------------------"

# Cài đặt helm và tải bitnami repo

curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
echo "Install helm successfully!"
echo "--------------------------------------------------------------------------"

# Cài đặt kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
echo "Install kubectl successfully!"

# Cài đặt Certbot để tạo chứng chỉ ssl
sudo apt-get install certbot -y
echo "Install Certbot successfully!"

echo "--------------------------------------------------------------------------"
echo -e "\U1F44F \U1F44F \U1F44F Prepare sucessfully to build project! \U1F44F \U1F44F \U1F44Fs"
echo "--------------------------------------------------------------------------"
