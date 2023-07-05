from shipment.entity.config_entity import DataValidationConfig
from shipment.entity.artifacts_entity import (DataIngestionArtifacts, DataValidationArtifacts)
from typing import Union
import json
from shipment.utils.main_utils import *
from shipment.exceptions import shippingException
from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *


class DataValidation:
    def __init__(self, data_ingestion_artifacts:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifacts = data_ingestion_artifacts


    def validate_columns(self, df:DataFrame)->bool:
        try:
            if len(df.columns) == len(self.data_validation_config.SCHEMA_CONFIG['columns']):
                validation_status = True
            else:
                validation_status = False
            return validation_status
        except Exception as e:
            raise shippingException(e, sys)


    def validate_numerical_columns(self, df:DataFrame)->bool:
        try:
            validation_status = False
            for column in self.data_validation_config.SCHEMA_CONFIG['numerical_columns']:
                if column not in df.columns:
                    logging.info('not found')
                else:
                    validation_status = True
            return validation_status
        except Exception as e:
            raise shippingException(e, sys)



    def validate_categorical_columns(self, df:DataFrame)->bool:
        try:
            validation_status = False
            for column in self.data_validation_config.SCHEMA_CONFIG['categorical_columns']:
                if column not in df.columns:
                    logging.info('not found')
                else:
                    validation_status = True
            return validation_status
        except Exception as e:
            raise shippingException(e, sys)


    def detect_dataset_drift(
            self, reference: DataFrame, production: DataFrame, get_ratio: bool = False) -> Union[bool, float]:
        try:
            data_drift_profile = Report(metrics=[DataDriftPreset(),])
            data_drift_profile.run(reference_data=reference, current_data=production)
            report = data_drift_profile.json()
            json_report = json.loads(report)

            data_drift_file_path = self.data_validation_config.DATA_DRIFT_FILE_PATH
            self.data_validation_config.UTILS.write_json_to_yaml_file(json_report, data_drift_file_path)

            n_features = []
            for i in json_report['metrics']:
                n_features.append(i['result']['number_of_columns'])
            n_features = n_features[0]

            n_drifted_features = []
            for i in json_report['metrics']:
                n_drifted_features.append(i['result']['number_of_drifted_columns'])
            n_drifted_features = n_drifted_features[0]

            status = []
            for i in json_report['metrics']:
                status.append(i['result']['dataset_drift'])
            status = status[0]

            if get_ratio:
                return n_drifted_features / n_features  # Calculating the drift ratio
            else:
                return status

        except Exception as e:
            raise shippingException(e, sys)


    def validate_dataset_columns(self) -> Tuple[bool, bool]:
        try:
            train_dataset_status = self.validate_columns(self.train_set)
            test_dataset_status = self.validate_columns(self.test_set)
            return train_dataset_status, test_dataset_status
        except Exception as e:
            raise shippingException(e, sys)


    def validate_dataset_numerical_columns(self) -> Tuple[bool, bool]:
        try:
            train_num_dataset_status = self.validate_numerical_columns(self.train_set)
            test_num_dataset_status = self.validate_numerical_columns(self.test_set)
            return train_num_dataset_status, test_num_dataset_status
        except Exception as e:
            raise shippingException(e, sys)



    def validate_dataset_categorical_columns(self) -> Tuple[bool, bool]:
        try:
            train_cat_dataset_status = self.validate_categorical_columns(self.train_set)
            test_cat_dataset_status = self.validate_categorical_columns(self.test_set)
            return train_cat_dataset_status, test_cat_dataset_status
        except Exception as e:
            raise shippingException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            self.train_set = pd.read_csv(self.data_ingestion_artifacts.train_data_file_path)
            self.test_set = pd.read_csv(self.data_ingestion_artifacts.test_data_file_path)
            os.makedirs(self.data_validation_config.DATA_VALIDATION_ARTIFACT_DIR, exist_ok=True)
            drift = self.detect_dataset_drift(self.train_set, self.test_set)
            (train_dataset_status,
             test_dataset_status) = self.validate_dataset_columns()
            (train_num_dataset_status,
             test_num_dataset_status) = self.validate_dataset_numerical_columns()
            (train_cat_dataset_status,
             test_cat_dataset_status) = self.validate_dataset_categorical_columns()
            drift_status = None
            if (train_dataset_status is True
                and test_dataset_status is True
                and train_num_dataset_status is True
                and test_num_dataset_status is True
                and train_cat_dataset_status is True
                and test_cat_dataset_status is True
                and drift is False):
                drift_status == True
            else:
                drift_status == False
            data_validation_artifacts = DataValidationArtifacts(
                data_drift_file_path=self.data_validation_config.DATA_DRIFT_FILE_PATH,
                validation_status=drift_status
            )
            return data_validation_artifacts

        except Exception as e:
            raise shippingException(e, sys)