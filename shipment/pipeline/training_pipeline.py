from shipment.entity.config_entity import (DataIngestionConfig, DataValidationConfig)
from shipment.entity.artifacts_entity import (DataIngestionArtifacts, DataValidationArtifacts)
from shipment.components.data_ingestion import DataIngestion
from shipment.components.data_validation import DataValidation
import sys
from shipment.exceptions import shippingException
from shipment.logger import logging
from shipment.configuration.mongo_operations import MongoDBOperation

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.mongo_op = MongoDBOperation()

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


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact= self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifact)
        except Exception as e:
            raise shippingException(e,sys)