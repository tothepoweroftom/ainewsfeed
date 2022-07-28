# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/helloworld

# Deploy to Cloud Run
gcloud run deploy helloworld \
--image gcr.io/${GOOGLE_CLOUD_PROJECT}/helloworld