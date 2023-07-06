from shipment.exceptions import shippingException
from shipment.entity.config_entity import ModelPusherConfig
from shipment.entity.artifacts_entity import (DataTransformationArtifacts, ModelPusherArtifacts, ModelTrainerArtifacts)
from shipment.configuration.s3_operations import S3Operation
import sys


class ModelPusher:
    def __init__(
            self,
            model_pusher_config: ModelPusherConfig,
            model_trainer_artifacts: ModelTrainerArtifacts,
            data_transformation_artifacts: DataTransformationArtifacts,
            s3: S3Operation,
    ):

        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts
        self.s3 = s3

    # this is method is used to initiate model pusher
    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        try:
            self.s3.upload_file(
                self.model_trainer_artifacts.trained_model_file_path,
                self.model_pusher_config.S3_MODEL_PATH,
                self.model_pusher_config.S3_BUCKET_NAME,
                remove=False,
            )

            model_pusher_artifact = ModelPusherArtifacts(
                s3_bucket_name=self.model_pusher_config.S3_MODEL_PATH,
                s3_model_path=self.model_pusher_config.S3_MODEL_PATH,
            )

            return model_pusher_artifact

        except Exception as e:
            raise shippingException(e, sys) from e
