from shipment.entity.config_entity import ModelEvaluationConfig
from shipment.entity.artifacts_entity import (ModelTrainerArtifacts, DataIngestionArtifacts,
                                              ModelEvaluationArtifacts)
from dataclasses import dataclass
from shipment.constants import *
from shipment.exceptions import shippingException
import sys
import pandas as pd

@dataclass
class EvaluationModelResponse:
    trained_model_r2_score: float
    s3_model_r2_score: float
    is_model_accepted: bool
    difference: bool


class ModelEvaluation:
    def __init__(self,
                 model_trainer_arifacts:ModelTrainerArtifacts,
                 model_evaluation_config:ModelEvaluationConfig,
                 data_ingestion_artifacts:DataIngestionArtifacts):
        self.model_trainer_artifacts = model_trainer_arifacts
        self.model_evaluation_config = model_evaluation_config
        self.data_ingestion_artifacts = data_ingestion_artifacts


    def get_s3_model(self)->object:
        try:
            status = self.model_evaluation_config.S3_OPERATIONS.is_model_present(BUCKET_NAME,
                                                                                 S3_MODEL_NAME)
            if status == True:
                model = self.model_evaluation_config.S3_OPERATIONS.load_model(MODEL_FILE_NAME,
                                                                              BUCKET_NAME)
                return model
            else:
                None

        except Exception as e:
            raise shippingException(e, sys)


    def evaluate_model(self)-> EvaluationModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifacts.test_data_file_path)
            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]

            trained_model = self.model_evaluation_config.UTILS.load_object(
                self.model_trainer_artifacts.trained_model_file_path)

            y_hat_trained_model = trained_model.predict(x)

            trained_model_r2_score = self.model_evaluation_config.UTILS.get_model_score(y, y_hat_trained_model)

            s3_model_r2_score = None
            s3_model = self.get_s3_model()
            if s3_model is not None:
                y_hat_s3_model = s3_model.predict(x)
                s3_model_r2_score = self.model_evaluation_config.UTILS.get_model_score(y, y_hat_s3_model)

            temp_best_model_score = 0 if s3_model_r2_score is None else s3_model_r2_score

            result= EvaluationModelResponse(trained_model_r2_score=trained_model_r2_score,
                                            s3_model_r2_score=s3_model_r2_score,
                                            is_model_accepted=True,
                                            difference=trained_model_r2_score-temp_best_model_score)
            return result

        except Exception as e:
            raise shippingException(e, sys)


    def initiate_model_evaluation(self)->ModelEvaluationArtifacts:
        try:
            evaluate_model_response = self.evaluate_model()

            model_evaluation_artifacts = ModelEvaluationArtifacts(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                trained_model_path=self.model_trainer_artifacts.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference
            )
            return model_evaluation_artifacts
        except Exception as e:
            raise shippingException(e, sys)



