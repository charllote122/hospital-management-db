import logging
from logger_config import setup_logging
from extract.extract_csv import extract_orders
from transform.transform_orders import transform_orders
from validation.validate_orders import validate_orders
from load.load_orders import load_orders

# Setup our advanced rotating logger
setup_logging()
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("========== PIPELINE STARTED ==========")
    try:
        # 1. Extract
        raw_df = extract_orders("data/raw/orders.csv")
        # 2. Transform
        clean_df = transform_orders(raw_df)

        # 3. Validate
        validate_orders(clean_df)

        # 4. Load
        load_orders(clean_df)

        logger.info("========== PIPELINE COMPLETED ==========")

    except Exception:
        # This will capture the FULL traceback in the log file
        logger.exception("========== PIPELINE FAILED ==========")
        raise


if __name__ == "__main__":
    run_pipeline()
