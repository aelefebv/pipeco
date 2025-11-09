import logging
from examples.models import ExampleCSVModel, ExampleDictModel, ExampleConfigModel, Nothing

######## Let's set up some steps
from pipeco import Step, register
import csv

@register("CSV path to dict")
class CSVPathToDict(Step[ExampleCSVModel, ExampleDictModel, ExampleConfigModel]):
    input_model = ExampleCSVModel
    output_model = ExampleDictModel
    config_model = ExampleConfigModel
    
    def process(self, data: ExampleCSVModel, ctx) -> ExampleDictModel:
        with open(data.csv_path, 'r', encoding='utf-8') as f:
            if self.config.header:
                reader = csv.DictReader(f, delimiter=self.config.delimiter)
                rows = list(reader)
            else:
                reader = csv.reader(f, delimiter=self.config.delimiter)
                rows = [{"col_" + str(i): val for i, val in enumerate(row)} for row in reader]
        dict_output = {"rows": rows}
        return ExampleDictModel(structured_dict=dict_output)

@register("Change favorite food")
class ChangeFavoriteFood(Step[ExampleDictModel, ExampleDictModel, Nothing]):
    input_model = ExampleDictModel
    output_model = ExampleDictModel
    config_model = Nothing
    
    valid_fav_food_cols = {"favorite_food", "fav_food", "favfood", "favoritefood"}
    
    def process(self, data: ExampleDictModel, ctx) -> ExampleDictModel:
        rows = data.structured_dict.get("rows", [])
        # Identify favorite food column
        fav_food_col = None
        for col in rows[0].keys():
            if col.lower() in self.valid_fav_food_cols:
                fav_food_col = col
                break
        # Change 'a' to 'o' in favorite food entries
        for row in rows:
            if fav_food_col in row:
                row[fav_food_col] = row[fav_food_col].replace('a', 'o').replace('A', 'O')
        return ExampleDictModel(structured_dict={"rows": rows})

class SaveToPathConfig(ExampleConfigModel):
    save_path: str
    overwrite: bool = False
    
@register("Save dict to CSV")
class SaveDictToCSV(Step[ExampleDictModel, Nothing, SaveToPathConfig]):
    input_model = ExampleDictModel
    output_model = Nothing
    config_model = SaveToPathConfig
    
    def process(self, data: ExampleDictModel, ctx) -> Nothing:
        rows = data.structured_dict.get("rows", [])
        if not rows:
            raise ValueError("No rows to save")
        
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            if self.config.header:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.config.delimiter)
                writer.writeheader()
                writer.writerows(rows)
            else:
                writer = csv.writer(f, delimiter=self.config.delimiter)
                for row in rows:
                    writer.writerow(row.values())
        
        return Nothing()
    
########## Now, let's use the pipeline with these steps
from pipeco import Pipeline

# Pipeline goes CSV path -> dict -> change all the a's to o's in the fav food -> save dict to CSV
csv_path = "examples/test.csv"
save_path = "examples/modified.csv"
# Initialize logger with date, time, level, and message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Option 1: Using get_step
from pipeco import get_step
pipe_with_steps = Pipeline(steps=[
    get_step("CSV path to dict")(),
    get_step("Change favorite food")(),
    get_step("Save dict to CSV")({"save_path": save_path, "overwrite": True}),
])

out = pipe_with_steps.run(ExampleCSVModel(csv_path=csv_path))

# Option 2: Directly using the classes
pipe_with_classes = Pipeline(steps=[
    CSVPathToDict(),
    ChangeFavoriteFood(),
    SaveDictToCSV({"save_path": save_path, "overwrite": True}),
])

out = pipe_with_classes.run(ExampleCSVModel(csv_path=csv_path))
