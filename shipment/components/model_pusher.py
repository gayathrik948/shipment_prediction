from shipment.exceptions import shippingException
from shipment.entity.config_entity import ModelPusherConfig
from shipment.entity.artifacts_entity import ModelPusherArtifacts, ModelTrainerArtifacts
from shipment.configuration.s3_operations import S3Operation
import sys


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_trainer_artifact: ModelTrainerArtifacts,
                 S3: S3Operation):
        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifact = model_trainer_artifact
        self.S3 = S3


    def initiate_model_pusher(self)->ModelPusherArtifacts:
        try:
            self.S3.upload_file(
                self.model_trainer_artifact.trained_model_file_path,
                self.model_pusher_config.S3_BUCKET_NAME,
                self.model_pusher_config.S3_MODEL_PATH)


            model_pusher_artifacts = ModelPusherArtifacts(
                s3_bucket_name=self.model_pusher_config.S3_BUCKET_NAME,
                s3_model_path=self.model_pusher_config.S3_MODEL_PATH
            )
            return model_pusher_artifacts

        except Exception as e:
            raise shippingException(e, sys)

