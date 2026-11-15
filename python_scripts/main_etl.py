import logging
from extract.extract_csv import extract_orders
from transform.transform_orders import transform_orders
from validation.validate_orders import validate_orders
from load.load_orders import load_orders

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():
    try:
        logging.info("Pipeline started")

        # 1. Extract
        raw_df = extract_orders("data/raw/orders.csv")

        # 2. Transform
        clean_df = transform_orders(raw_df)

        # 3. Validate
        validate_orders(clean_df)

        # 4. Load
        load_orders(clean_df)

        logging.info("Pipeline completed successfully!")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()
