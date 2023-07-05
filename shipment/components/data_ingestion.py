from shipment.entity.config_entity import DataIngestionConfig
from shipment.entity.artifacts_entity import DataIngestionArtifacts
from shipment.configuration.mongo_operations import MongoDBOperation
from shipment.constants import *
import os
import sys
from shipment.utils.main_utils import *
from shipment.exceptions import shippingException
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from typing import Tuple


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig,
                 mongo_op: MongoDBOperation):
        self.data_ingestion_config = data_ingestion_config
        self.mongo_op = mongo_op


    def get_data_from_mongodb(self)->DataFrame:
        try:
            df = self.mongo_op.get_collection_as_dataframe(
                                                    self.data_ingestion_config.DATABASE_NAME,
                                                    self.data_ingestion_config.COLLECTIONS_NAME)
            return df
        except Exception as e:
            raise shippingException(e,sys)


    def spilt_data_as_train_test(self, df:DataFrame)->Tuple[DataFrame, DataFrame]:
        try:
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACT_DIR, exist_ok=True)
            train_set, test_set = train_test_split(df, test_size=TEST_SIZE)
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_TRAIN_ARTIFACT_DIR, exist_ok=True)
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_TEST_ARTIFACT_DIR, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.DATA_INGESTION_TRAIN_FILE_PATH, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.DATA_INGESTION_TEST_FILE_PATH, index=False, header=True)
            return train_set, test_set
        except Exception as e:
            raise shippingException(e,sys)



    def initiate_data_ingestion(self):
        try:
            df = self.get_data_from_mongodb()
            df1 = df.drop(self.data_ingestion_config.DROP_COLS, axis=1)
            df1= df1.dropna()
            self.spilt_data_as_train_test(df1)
            data_ingestion_artifacts = DataIngestionArtifacts(
                train_data_file_path=self.data_ingestion_config.DATA_INGESTION_TRAIN_FILE_PATH,
                test_data_file_path=self.data_ingestion_config.DATA_INGESTION_TEST_FILE_PATH
            )
            return data_ingestion_artifacts
        except Exception as e:
            raise shippingException(e,sys)





