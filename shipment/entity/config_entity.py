from dataclasses import dataclass
from shipment.constants import *
from shipment.utils.main_utils import *
from shipment.logger import logging
from shipment.exceptions import shippingException
import os
from from_root import from_root

@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(filename=SCHEMA_FILE_PATH)
        self.DATABASE_NAME = DB_NAME
        self.COLLECTIONS_NAME = COLLECTION_NAME
        self.DROP_COLS = list(self.SCHEMA_CONFIG["drop_columns"])
        self.DATA_INGESTION_ARTIFACT_DIR:str = os.path.join(from_root(),
                                                             ARTIFACTS_DIR,
                                                             DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_INGESTION_TRAIN_ARTIFACT_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACT_DIR,
                                                     DATA_INGESTION_TRAIN_DIR)
        self.DATA_INGESTION_TEST_ARTIFACT_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACT_DIR,
                                                    DATA_INGESTION_TEST_DIR)
        self.DATA_INGESTION_TRAIN_FILE_PATH:str = os.path.join(self.DATA_INGESTION_TRAIN_ARTIFACT_DIR,
                                                           DATA_INGESTION_TRAIN_FILE_NAME)
        self.DATA_INGESTION_TEST_FILE_PATH:str = os.path.join(self.DATA_INGESTION_TEST_ARTIFACT_DIR,
                                                          DATA_INGESTION_TEST_FILE_NAME)


@dataclass
class DataValidationConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(filename=SCHEMA_FILE_PATH)
        self.DATA_VALIDATION_ARTIFACT_DIR: str = os.path.join(from_root(),
                                                             ARTIFACTS_DIR,
                                                             DATA_VALIDATION_ARTIFACTS_DIR)
        self.DATA_DRIFT_FILE_PATH: str = os.path.join(self.DATA_VALIDATION_ARTIFACT_DIR,
                                                      DATA_DRIFT_FILE_NAME)



@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(filename=SCHEMA_FILE_PATH)
        self.DATA_TRANSFORMATION_ARTIFACT_DIR: str = os.path.join(from_root(),
                                                                  ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)
        self.TRANSFORMED_TRAIN_ARTIFACT_DATA_DIR = os.path.join(self.DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                                TRANSFORMED_TRAIN_DATA_DIR)
        self.TRANSFORMED_TEST_ARTIFACT_DATA_DIR = os.path.join(self.DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                               TRANSFORMED_TEST_DATA_DIR)
        self.TRANSFORMED_TRAIN_ARTIFACT_DATA_FILE_NAME = os.path.join(self.TRANSFORMED_TRAIN_ARTIFACT_DATA_DIR,
                                                                      TRANSFORMED_TRAIN_DATA_FILE_NAME)
        self.TRANSFORMED_TEST_ARTIFACT_DATA_FILE_NAME = os.path.join(self.TRANSFORMED_TEST_ARTIFACT_DATA_DIR,
                                                                     TRANSFORMED_TEST_DATA_FILE_NAME)
        self.PREPROCESSOR_OBJECT_ARTIFACT_FILE_NAME = os.path.join(self.DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                                   PREPROCESSOR_OBJECT_FILE_NAME)


@dataclass
class ModelTrainerConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.MODEL_TRAINER_ARTIFACT_DIR:str = os.path.join(from_root(),
                                                           ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR)
        self.TRAINED_MODEL_FILE_PATH:str = os.path.join(self.MODEL_TRAINER_ARTIFACT_DIR, MODEL_FILE_NAME)
        