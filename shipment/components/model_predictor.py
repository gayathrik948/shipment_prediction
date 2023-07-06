import sys
from typing import Dict
from pandas import DataFrame
import pandas as pd
from shipment.constants import *
from shipment.configuration.s3_operations import S3Operation
from shipment.exceptions import shippingException


class shippingData:
    def __init__(self,
                 artist,
                 height,
                 width,
                 weight,
                 material,
                 priceOfSculpture,
                 baseShippingPrice,
                 international,
                 expressShipment,
                 installationIncluded,
                 transport,
                 fragile,
                 customerInformation,
                 remoteLocation,
                 ):
        self.artist = artist
        self.height = height
        self.width = width
        self.weight = weight
        self.material = material
        self.priceOfSculpture = priceOfSculpture
        self.baseShippingPrice = baseShippingPrice
        self.international = international
        self.expressShipment = expressShipment
        self.installationIncluded = installationIncluded
        self.transport = transport
        self.fragile = fragile
        self.customerInformation = customerInformation
        self.remoteLocation = remoteLocation


    def get_data(self)->Dict:
        try:
            input_data = {
                "Artist Reputation": [self.artist],
                "Height": [self.height],
                "Width": [self.width],
                "Weight": [self.weight],
                "Material": [self.material],
                "Price Of Sculpture": [self.priceOfSculpture],
                "Base Shipping Price": [self.baseShippingPrice],
                "International": [self.international],
                "Express Shipment": [self.expressShipment],
                "Installation Included": [self.installationIncluded],
                "Transport": [self.transport],
                "Fragile": [self.fragile],
                "Customer Information": [self.customerInformation],
                "Remote Location": [self.remoteLocation],
            }
            return input_data
        except Exception as e:
            raise shippingException(e, sys)

    def get_input_data_frame(self) -> DataFrame:
        try:
            input_dict = self.get_data()
            return pd.DataFrame(input_dict)
        except Exception as e:
            raise shippingException(e, sys)



class CostPredictor:
    def __init__(self):
        self.s3 = S3Operation()
        self.bucket_name = BUCKET_NAME


    def predict(self, X)->float:
        try:
            best_model = self.s3.load_model(MODEL_FILE_NAME,
                                            self.bucket_name)
            result = best_model.predict(X)
            return result
        except Exception as e:
            raise shippingException(e, sys)