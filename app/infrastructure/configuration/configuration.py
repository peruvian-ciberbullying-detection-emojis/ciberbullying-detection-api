from app.infrastructure.utils import get_drive_url_from_file_id
import pandas as pd

def get_spanish_peruvian_dictionary():
    spanish_peruvian_dict_id = '17J9JgVzdSeXKMk6hhsA8Zv2XCjIdMH84'
    spanish_peruvian_dict_url = get_drive_url_from_file_id(spanish_peruvian_dict_id)
    spanish_peruvian_dict_df = pd.read_excel(spanish_peruvian_dict_url).dropna().reset_index(drop=True)
    return dict(zip(spanish_peruvian_dict_df['jerga'], spanish_peruvian_dict_df['significado']))