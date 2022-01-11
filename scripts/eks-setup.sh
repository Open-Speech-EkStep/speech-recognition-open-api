echo "Install AWS cli"
export TZ=Europe/Minsk && sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > sudo  /etc/timezone && sudo apt-get update && sudo apt-get install -y awscli
echo "Install and confgure kubectl aws-iam-authenticator"
sudo curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator && sudo chmod +x ./aws-iam-authenticator && sudo cp ./aws-iam-authenticator /bin/aws-iam-authenticator
echo  "Install latest awscli version"
sudo apt install unzip && curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" && unzip awscli-bundle.zip &&./awscli-bundle/install -b ~/bin/aws
echo "Get the kubeconfig file "
export KUBECONFIG=$HOME/.kube/kubeconfig && /home/circleci/bin/aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER_NAME