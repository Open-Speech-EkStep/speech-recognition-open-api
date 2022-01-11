echo ${GOOGLE_AUTH} > ${HOME}/gcp-key.json
pip3 install google_compute_engine
gcloud auth activate-service-account --key-file ${HOME}/gcp-key.json
gcloud --quiet config set project ${GCP_PROJECT}
gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_CLUSTER_REGION} --project ${GCP_PROJECT}