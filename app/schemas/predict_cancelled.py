from pydantic import BaseModel, Field


class PredictCancelledRequest(BaseModel):
    OP_CARRIER_AIRLINE_ID: int = Field(..., alias="op_carrier_airline_id")
    ORIGIN_AIRPORT_ID: int = Field(..., alias="origin_airport_id")
    DEST_AIRPORT_ID: int = Field(..., alias="dest_airport_id")
    DISTANCE: int = Field(..., alias="distance")
    CRS_ELAPSED_TIME: int = Field(..., alias="crs_elapsed_time")
    DEP_HOUR: int = Field(..., alias="dep_hour")
    DEP_MINUTE: int = Field(..., alias="dep_minute")
    ARR_HOUR: int = Field(..., alias="arr_hour")
    ARR_MINUTE: int = Field(..., alias="arr_minute")

    class Config:
        validate_by_name = True