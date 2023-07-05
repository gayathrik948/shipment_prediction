from shipment.pipeline.training_pipeline import TrainingPipeline
from shipment.exceptions import shippingException
import sys

try:
    obj = TrainingPipeline()
    obj.run_pipeline()
except Exception as e:
    raise shippingException(e, sys)