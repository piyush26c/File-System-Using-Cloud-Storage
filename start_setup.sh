echo "File Systems Using Cloud Storage"
echo "Creating a VM and installing dependencies."

echo "Creating Server VM instace..."
gcloud compute instances create eccfsassignmentvm --project=piyush-chaudhari-fall2023 --zone=us-central1-a --machine-type=e2-medium --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default --metadata=^,@^ssh-keys=piyrchau:ecdsa-sha2-nistp256\ AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDtb7Ur/2uVDIs9M3ddNkHvqoDp92/R4JcXVGS1oO2twfds7KRiBxUWx/qKvr7aku7BC\+0sKM3O1WJ80vmiNf6E=\ google-ssh\ \{\"userName\":\"piyrchau@iu.edu\",\"expireOn\":\"2023-11-02T16:42:39\+0000\"\} --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=829646497935-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server,https-server,lb-health-check --create-disk=auto-delete=yes,boot=yes,device-name=eccfsvm,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20231101,mode=rw,size=10,type=projects/piyush-chaudhari-fall2023/zones/us-central1-a/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=goog-ec-src=vm_add-gcloud --reservation-affinity=any
echo "VM successfully created."


echo "Doing SSH into VM instance..."
sleep 60
gcloud compute ssh eccfsassignmentvm --project=piyush-chaudhari-fall2023 --zone=us-central1-a <<EOF
echo "SSH successful."

echo "Cloning the eccfsassignment (from piyush chaudhari github.iu.edu account) repository into VM instance..."
git clone https://piyrchau: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@github.iu.edu/piyrchau/eccfsassignment.git
echo "Repository cloned successfully."

sudo apt-get update

cd eccfsassignment/

echo "Installing project requirements in VM instance..."
chmod +x install_requirements.sh
sudo ./install_requirements.sh
echo "Installation completed successfully."

echo "Done"
EOF
