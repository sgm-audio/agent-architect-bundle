---
name: gcloud
description: Comprehensive Google Cloud Platform operations including compute, storage, databases, networking, AI/ML services, authentication, billing, and resource management. Use when working with GCP, Google Cloud services, gcloud CLI, or cloud infrastructure.
---

# Google Cloud Platform (gcloud) Skills

## Compute Engine

### VM Management
- **Creating instances**: Use `gcloud compute instances create` with custom machine types, startup scripts, and metadata
- **Instance templates**: Create reusable templates with `gcloud compute instance-templates create`
- **Managed instance groups**: Set up auto-scaling with `gcloud compute instance-groups managed`
- **Spot/preemptible VMs**: Cost-optimized instances that can be terminated with 30s notice
- **Custom images**: Create and manage custom machine images for faster instance provisioning

### SSH and Access
- **SSH keys management**: Configure project-wide or instance-specific SSH keys
- **OS Login**: Enable OS Login for centralized IAM-based access
- **IAP tunneling**: Use Identity-Aware Proxy for secure tunnel to instances without public IPs
- **Serial console**: Access serial console for debugging boot issues

### GPU and High-Performance Computing
- **GPU attachment**: Add NVIDIA GPUs (T4, V100, A100, H100) to instances
- **Deep Learning VM**: Pre-configured images with CUDA, cuDNN, and ML frameworks
- **Live migration**: Configure high-availability with live migration support

## Google Kubernetes Engine (GKE)

### Cluster Management
- **Autopilot clusters**: Fully managed Kubernetes with automatic provisioning
- **Standard clusters**: User-managed with full control over node pools
- **Private clusters**: Clusters with no public endpoint access
- **Workload identity**: Secure IAM for workloads without service account keys

### Node Pools
- **Node pool operations**: Create, resize, upgrade, and delete node pools
- **Auto-scaling**: Configure cluster autoscaler and node auto-provisioning
- **Spot nodes**: Cost optimization with preemptible node pools
- **GPU node pools**: Add GPU-enabled nodes for ML workloads

### Workload Deployment
- **kubectl context**: Configure `gcloud container clusters get-credentials`
- **Deploy applications**: Use `kubectl apply` with manifests
- **Service mesh**: Istio and Anthos Service Mesh integration

## Cloud Storage

### Bucket Operations
- **Create buckets**: `gsutil mb` or `gcloud storage buckets create` with location and class
- **Bucket policies**: Set uniform bucket-level access or fine-grained permissions
- **Lifecycle rules**: Auto-delete or archive objects based on age
- **Versioning**: Enable object versioning for backup and recovery
- **CORS configuration**: Set Cross-Origin Resource Sharing for web assets

### Object Operations
- **Upload/download**: Use `gsutil cp`, `gcloud storage cp`, or signed URLs
- **Streaming transfers**: Use `gsutil rsync` for efficient incremental sync
- **Object transforms**: Compose, rewrite, and transform objects
- **Transfer service**: Scheduled transfers from S3, HTTP sources, or on-prem

### Data Movement
- **Transfer Appliance**: Physical appliance for offline data transfer
- **Online transfer**: Transfer from AWS S3, Azure Blob, or HTTP sources
- **Storage Transfer Service**: Automated scheduled transfers

## Cloud SQL and Databases

### Cloud SQL
- **Instance creation**: MySQL, PostgreSQL, SQL Server with customized specs
- **HA configuration**: Enable high availability with automatic failover
- **Read replicas**: Scale read operations with cross-region replicas
- **Backup and restore**: Configure automated backups and point-in-time recovery
- **Connection pooling**: Cloud SQL Auth Proxy for secure connections

### Firestore & Datastore
- **NoSQL document database**: Create Firestore databases in native or datastore mode
- **Indexes**: Manage composite indexes for complex queries
- **Data modeling**: Design schemas for efficient queries

### Spanner
- **Globally distributed**: Create Spanner instances for globally consistent databases
- **Schema management**: Define tables, interleaved tables, and indexes

## BigQuery

### Dataset Operations
- **Create datasets**: `bq mk` with location, default table expiration
- **Access controls**: Dataset-level and column-level security
- **Federated queries**: Query external data sources without loading

### Table Operations
- **Load data**: From GCS, local files, or streaming
- **Export data**: To GCS in various formats (CSV, JSON, Avro, Parquet)
- **Partitioning**: Time-partitioned tables for query optimization
- **Clustering**: Clustered tables for improved query performance

### Query Operations
- **Standard SQL**: Full ANSI SQL 2011 support
- **Parameterized queries**: Safe query construction
- **Scripting**: Multi-statement SQL scripts
- **ML queries**: BigQuery ML for in-database machine learning

## Networking

### VPC Networks
- **Custom VPC**: Create with custom subnets, routing, and firewall rules
- **Shared VPC**: Share VPC across projects with host/service project setup
- **Private Google Access**: Access Google APIs without public IPs

### Load Balancing
- **HTTP(S) load balancer**: Global HTTP(S) with CDN integration
- **TCP/UDP load balancer**: Regional load balancing
- **Internal load balancer**: Private backend services
- **SSL proxy**: Terminate SSL for non-HTTP traffic

### DNS and Traffic Director
- **Cloud DNS**: Managed DNS service with DNSSEC
- **Traffic Director**: Service mesh traffic management
- **Cloud CDN**: Content delivery network integration

## Identity and Access Management

### Service Accounts
- **Create service accounts**: `gcloud iam service-accounts create`
- **Grant roles**: Bind roles to service accounts with `gcloud projects add-iam-policy-binding`
- **Key management**: Create and rotate service account keys
- **Workload Identity**: Federate identity for Kubernetes workloads

### IAM Policies
- **Policy binding**: Grant roles to users, groups, or service accounts
- **Conditional IAM**: Role bindings with conditions based on attributes
- **Organization policies**: Set organizational constraints
- **Audit logs**: View Cloud Audit Logs for access tracking

### Authentication
- **Application Default Credentials**: `gcloud auth application-default login`
- **Service account impersonation**: `gcloud auth activate-service-account`
- **OIDC tokens**: Generate tokens for workload federation

## Cloud Functions & Cloud Run

### Cloud Functions (2nd Gen)
- **Deploy functions**: `gcloud functions deploy` with triggers
- **HTTP functions**: Respond to HTTP requests
- **Background functions**: Triggered by events (Pub/Sub, Storage, Firestore)
- **Environment variables**: Configure runtime environment

### Cloud Run
- **Deploy services**: Container-based serverless
- **Revisions**: Manage revisions and traffic splitting
- **Jobs**: Run containerized batch workloads
- **Services**: Fully managed compute platform

## Pub/Sub and Messaging

### Topics and Subscriptions
- **Create topics**: `gcloud pubsub topics create`
- **Subscriptions**: Pull, push, or bigquery subscriptions
- **Dead letter topics**: Handle failed message delivery
- **Ordering**: Configure message ordering

### Publishing and Subscribing
- **Publish messages**: Use `gcloud pubsub topics publish`
- **Pull messages**: `gcloud pubsub subscriptions pull`
- **Push endpoints**: Configure webhook deliveries

## AI and Machine Learning

### Vertex AI
- **Workbench**: Managed Jupyter notebooks
- **Training jobs**: Custom training with custom containers
- **AutoML**: Train models without code
- **Prediction endpoints**: Deploy models for online prediction
- **Feature Store**: Manage ML features

### Vision, NLP, Speech APIs
- **Cloud Vision**: Label detection, OCR, face detection
- **Cloud Natural Language**: Entity extraction, sentiment analysis
- **Cloud Speech-to-Text**: Audio transcription
- **Cloud Text-to-Speech**: Speech synthesis
- **Translation API**: Translate text between languages

## DevOps and Deployment

### Deployment Manager
- **Templates**: Jinja2 or Python templates for infrastructure
- **Deployments**: Create and manage deployments
- **Preview**: Preview changes before applying

### Cloud Build
- **Build triggers**: Automate builds on code changes
- **Build config**: cloudbuild.yaml with steps
- **Artifacts**: Store build artifacts in Container Registry or Artifact Registry
- **Private pools**: Run builds in private VPC

## Monitoring and Logging

### Cloud Logging
- **Log sinks**: Export logs to BigQuery, Pub/Sub, or GCS
- **Log router**: Filter and route logs based on conditions
- **Structured logging**: Use JSON logging for better analysis

### Cloud Monitoring
- **Alerting policies**: Create alerts based on metrics
- **Dashboards**: Custom dashboards with charts
- **Uptime checks**: Monitor service availability

## Billing and Cost Management

### Billing Operations
- **View billing**: Access billing account information
- **Budget alerts**: Set budgets with alert thresholds
- **Cost breakdown**: Analyze costs by project, service, or label
- **Export**: Export billing data to BigQuery

## Resource Management

### Organization Hierarchy
- **Folders**: Organize projects under folders
- **Projects**: Create and manage projects
- **Resource hierarchy**: Understand organization, folder, project structure

### Deployment
- **Terraform**: Use Google Cloud Provider for Infrastructure as Code
- **Config Connector**: Kubernetes-based resource management
- **gcloud commands**: Direct resource manipulation

## Common gcloud Patterns

### Project Setup
```bash
# Set active project
gcloud config set project PROJECT_ID

# List configurations
gcloud config configurations list

# Configure region and zone
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

### Filtering and Formatting
```bash
# Filter resources
gcloud compute instances list --filter="status:running"

# Format output
gcloud projects list --format="table(name,projectId,createTime)"

# Quiet mode for scripts
gcloud compute instances list --quiet --format="value(name)"
```

### Scripting
```bash
# Iterate over resources
for zone in $(gcloud compute zones list --filter="region:us-central1" --format="value(name)"); do
  gcloud compute instances list --zone=$zone
done
```

## Troubleshooting

### Instance Issues
- **Serial console**: Check boot logs
- **Startup scripts**: Review serial port output
- **Firewall rules**: Verify ingress rules
- ** quotas**: Check quota availability

### Network Issues
- **VPC flow logs**: Analyze network traffic
- **Connectivity tests**: Use Network Intelligence Center
- **Firewall logs**: Review firewall rule logging

### Permission Issues
- **IAM policy analyzer**: Troubleshoot access
- **Service account impersonation**: Test service account access
- **Audit logs**: Review permission denied events
