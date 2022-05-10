from streamsets.sdk import ControlHub

from secrets import secrets

sch = ControlHub(
    server_url=secrets.get('SERVER_URL'),
    credential_id=secrets.get('CRED_ID'),
    token=secrets.get('CRED_TOKEN'))

# Choose which stage to Add
stage_to_add = 'adls'

# Instantiate the PipelineBuilder instance to build the pipeline
pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector',
                                            engine_id=secrets.get('DATA_COLLECTOR_ENGINE_ID'))

# Add Cloud Migration Fragment
fragment = sch.pipelines.get(fragment=True, name=secrets.get('FRAGMENT_NAME'))
fragment_stage = pipeline_builder.add_fragment(fragment)


# Functions below configure stages
def add_adls_stage():
    adls = pipeline_builder.add_stage('Azure Data Lake Storage Gen2')
    adls.data_format = 'DELIMITED'
    connection = sch.connections.get(id=secrets.get('ADLS_CONNECTION_ID'))
    adls.use_connection(connection)
    return adls


def add_google_cloud_stage():
    gcs = pipeline_builder.add_stage('Google Cloud Storage', type='destination')
    gcs.bucket = 'brenna'
    gcs.data_format = 'DELIMITED'
    connection = sch.connections.get(id=secrets.get('GCS_CONNECTION_ID'))
    gcs.use_connection(connection)
    return gcs


# Use the chosen stage
if stage_to_add == 'gcs':
    stage = add_google_cloud_stage()
else:
    stage = add_adls_stage()

# Connect New Stage with a Fragment
fragment_stage >> stage

# Build the pipeline
pipeline = pipeline_builder.build('My first pipeline with Python SDK_'+stage_to_add)

# Publish the updated version of the pipeline
sch.publish_pipeline(pipeline)



