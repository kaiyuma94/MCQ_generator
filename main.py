import sys
from pathlib import Path
import argparse
from modules.input_handler import InputHandler
from modules.question_processor import QuestionProcessor
from modules.output_generator import OutputGenerator
from modules.logger import setup_logger
from modules.config_manager import load_config

logger = setup_logger(__name__)
config = load_config()

def process_file(input_path: Path, output_path: Path) -> None:
    try:
        # Initialize components
        input_handler = InputHandler(config)
        processor = QuestionProcessor(config)
        output_generator = OutputGenerator(config)

        # Read input
        df = input_handler.read_excel(input_path)
        logger.info(f"Loaded {len(df)} questions")

        # Process in batches
        batch_size = config['processing']['batch_size']
        processed_data = []
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_results = processor.process_batch([row.to_dict() for _, row in batch.iterrows()])
            processed_data.extend(batch_results)
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(df)-1)//batch_size + 1}")

        # Write output
        output_generator.write_excel(processed_data, output_path)
        logger.info(f"Saved {len(processed_data)} questions")

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    input_dir = Path("data/input")
    output_dir = Path("data/output")
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    input_files = list(input_dir.glob("*.xlsx"))
    
    if not input_files:
        logger.error("No Excel files found in data/input directory")
        sys.exit(1)

    for input_file in input_files:
        try:
            output_file = f"processed_{input_file.name}"  # Just the filename, not the full path
            logger.info(f"Processing {input_file.name}...")
            process_file(input_file, output_file)
            logger.info(f"Completed processing {input_file.name}")
        except KeyboardInterrupt:
            logger.info("Process interrupted by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error processing {input_file.name}: {str(e)}")
            continue