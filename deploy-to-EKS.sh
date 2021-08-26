#!/bin/bash
echo "Install AWS cli"
export TZ=Europe/Minsk && sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > sudo  /etc/timezone && sudo apt-get update && sudo apt-get install -y awscli
echo "Install and confgure kubectl"
sudo curl -L https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl && sudo chmod +x /usr/local/bin/kubectl
echo "Install and confgure kubectl aws-iam-authenticator"
sudo curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator && sudo chmod +x ./aws-iam-authenticator && sudo cp ./aws-iam-authenticator /bin/aws-iam-authenticator
echo  "Install latest awscli version"
sudo apt install unzip && curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" && unzip awscli-bundle.zip &&./awscli-bundle/install -b ~/bin/aws
echo "Get the kubeconfig file "
export KUBECONFIG=$HOME/.kube/kubeconfig && /home/circleci/bin/aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER_NAME
echo "Install and configuire helm"
sudo curl -L https://storage.googleapis.com/kubernetes-helm/helm-v2.11.0-linux-amd64.tar.gz | tar xz && sudo mv linux-amd64/helm /bin/helm && sudo rm -rf linux-amd64
echo "Initialize helm"
helm init --client-only --kubeconfig=$HOME/.kube/kubeconfig
echo "Install tiller plugin"
helm plugin install https://github.com/rimusz/helm-tiller --kubeconfig=$HOME/.kube/kubeconfig
helm tiller start-ci
export HELM_HOST=127.0.0.1:44134
result=$(eval helm ls | grep ekstep-model-api)
if [ $? -ne "0" ]; then
   helm install --timeout 180s ekstep-model-api asr-model-v2 --namespace test --create-namespace
else
   helm upgrade --timeout 180s ekstep-model-api asr-model-v2 --namespace test --create-namespace
fi
echo "stop tiller"
helm tiller stop
