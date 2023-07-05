from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    train_data_file_path: str
    test_data_file_path: str


@dataclass
class DataValidationArtifacts:
    data_drift_file_path: str
    validation_status: bool

@dataclass
class DataTransformationArtifacts:
    transformed_object_path: str
    transformed_train_path: str
    transformed_test_path: str

@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path: str
