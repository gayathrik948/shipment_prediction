from shipment.entity.config_entity import (DataIngestionConfig, DataValidationConfig, DataTransformationConfig,
                                           ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig)
from shipment.entity.artifacts_entity import (DataIngestionArtifacts, DataValidationArtifacts,
                                              DataTransformationArtifacts, ModelTrainerArtifacts,
                                              ModelEvaluationArtifacts, ModelPusherArtifacts)
from shipment.components.data_ingestion import DataIngestion
from shipment.components.data_validation import DataValidation
from shipment.components.data_transformation import DataTransformation
from shipment.components.model_trainer import ModelTrainer
from shipment.components.model_evaluation import ModelEvaluation
from shipment.components.model_pusher import ModelPusher
from shipment.configuration.s3_operations import S3Operation
import sys
from shipment.exceptions import shippingException
from shipment.logger import logging
from shipment.configuration.mongo_operations import MongoDBOperation

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_pusher_config = ModelPusherConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.mongo_op = MongoDBOperation()
        self.S3 = S3Operation()

    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            logging.info(f"data_ingestion started")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config,
                                                    mongo_op=self.mongo_op)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data_ingestion completed successfully")
            return data_ingestion_artifact
        except Exception as e:
            raise shippingException(e,sys)


    def start_data_validation(self, data_ingestion_artifacts:DataIngestionArtifacts)->DataValidationArtifacts:
        try:
            logging.info(f"data_validation started")
            data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                             data_ingestion_artifacts=data_ingestion_artifacts)
            data_validation_artifacts = data_validation.initiate_data_validation()
            return data_validation_artifacts
        except Exception as e:
            raise shippingException(e, sys)


    def start_data_transformation(self, data_ingestion_artifacts:DataIngestionArtifacts)->DataTransformationArtifacts:
        try:
            logging.info(f"data_transformation started")
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,
                                                    data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise shippingException(e, sys)


    def start_model_training(self, data_transformation_artifacts:DataTransformationArtifacts)->ModelTrainerArtifacts:
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifacts,
                                         model_trainer_config=self.model_trainer_config)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            return model_trainer_artifacts
        except Exception as e:
            raise shippingException(e, sys)


    def start_model_evaluation(self, model_trainer_artifacts:ModelTrainerArtifacts,
                               data_ingestion_artifacts:DataIngestionArtifacts)->ModelEvaluationArtifacts:
        try:
            model_evaluation = ModelEvaluation(model_trainer_arifacts=model_trainer_artifacts,
                                               model_evaluation_config=self.model_evaluation_config,
                                               data_ingestion_artifacts=data_ingestion_artifacts)
            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifacts
        except Exception as e:
            raise shippingException(e, sys)

    def start_model_pusher(
            self,
            model_trainer_artifacts: ModelTrainerArtifacts,
            s3: S3Operation,
            data_transformation_artifacts: DataTransformationArtifacts,
    ) -> ModelPusherArtifacts:
        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_trainer_artifacts=model_trainer_artifacts,
                s3=s3,
                data_transformation_artifacts=data_transformation_artifacts,
            )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact= self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifact)
            data_transformation_artifacts = self.start_data_transformation(data_ingestion_artifacts=data_ingestion_artifact)
            model_trainer_artifacts = self.start_model_training(data_transformation_artifacts=data_transformation_artifacts)
            model_evaluation_artifacts = self.start_model_evaluation(model_trainer_artifacts=model_trainer_artifacts,
                                                                     data_ingestion_artifacts=data_ingestion_artifact)
            if not model_evaluation_artifacts.is_model_accepted:
                print("model not accepted")
                return None
            model_pusher_artifact = self.start_model_pusher(
                model_trainer_artifacts=model_trainer_artifacts,
                s3=self.S3,
                data_transformation_artifacts=data_transformation_artifacts,
            )

        except Exception as e:
            raise shippingException(e,sys)