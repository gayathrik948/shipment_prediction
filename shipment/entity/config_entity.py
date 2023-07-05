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