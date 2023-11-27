import pandas as pd
from unidecode import unidecode


class DivarDataCleaner:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.data.drop(columns=["real_estate_agencey", "units_per_floor",
                                "document", "building_direction", "unit_status"], inplace=True)
        self.data = self.data[self.data['real_estate_type']
                              == 'apartment-sell']

    def clean_facilities(self):
        self.data['facilities'].fillna(',', inplace=True)
        self.data['facilities'] = self.data['facilities'].str.replace("[", "")
        self.data['facilities'] = self.data['facilities'].str.replace("]", "")
        self.data['facilities'] = self.data['facilities'].str.replace("'", "")

    def one_hot_encode_facilities(self):
        exploded_df = self.data['facilities'].map(
            lambda x: x.split(",")).explode()
        one_hot_encoded = pd.get_dummies(exploded_df, dtype="int")
        result_df = one_hot_encoded.groupby(one_hot_encoded.index).sum()
        result_df.drop(columns="",  inplace=True)
        # result_df.drop(columns=['facilities'], inplace=True)

        result_df = result_df.loc[:, ["بالکن", "بالکن ندارد", "انباری",
                                      "انباری ندارد", "آسانسور", "آسانسور ندارد", "پارکینگ", "پارکینگ ندارد"]]

        result_df.rename(columns={"پارکینگ": "has_parking",
                                  "پارکینگ ندارد": "no_parking",
                                  "آسانسور": "has_elevator",
                                  "آسانسور ندارد": "no_elevator",
                                  "انباری": "has_warehouse",
                                  "انباری ندارد": "no_warehouse",
                                  "بالکن": "has_balcony",
                                  "بالکن ندارد": "no_balcony"},
                         inplace=True)

        self.data = self.data.merge(
            result_df, left_index=True, right_index=True)

    def clean_prices(self):
        prices = ['price', 'price_per_meter']
        for price in prices:
            self.data[price] = self.data[price].str.replace('٬', '')
            self.data[price] = self.data[price].str.replace('تومان', '')
            self.data[price] = self.data[price].astype(str).apply(unidecode)
            self.data.drop(self.data[self.data[price]
                           == 'twfqy'].index, inplace=True)
            self.data[price] = self.data[price].astype("float")

    def clean_floor(self):
        self.data['floor'] = self.data['floor'].str.replace('زیرهمکف', '-1')
        self.data['floor'] = self.data['floor'].str.replace('همکف', '0')
        self.data['floor'] = self.data['floor'].str.replace('بیشتر از', '')
        self.data['floor'] = self.data['floor'].str.replace('از', '|')
        self.data['floor'] = self.data['floor'].astype(str).apply(unidecode)
        self.data['floor'] = self.data['floor'].str.split(
            "|").apply(lambda x: x[0])
        self.data['floor'] = self.data['floor'].str.replace('30+', '30')
        self.data['floor'] = self.data['floor'].str.replace('+30', '30')
        self.data.drop(self.data[self.data["floor"]
                       == 'nan'].index, inplace=True)
        self.data["floor"] = self.data["floor"].astype("int")

    def clean_real_estate_area(self):
        self.data['real_estate_area'] = self.data['real_estate_area'].astype(
            str).apply(unidecode)
        self.data["real_estate_area"] = self.data["real_estate_area"].astype(
            'float')

    def clean_real_estate_age(self):
        self.data['real_estate_age'] = self.data['real_estate_age'].astype(
            str).apply(unidecode)
        self.data['real_estate_age'] = self.data['real_estate_age'].str.replace(
            'qbl z 1370', '1370')
        self.data["real_estate_age"] = 1402 - \
            (self.data["real_estate_age"].astype('float'))

    def clean_total_rooms(self):
        self.data['total_rooms'] = self.data['total_rooms'].astype(
            str).apply(unidecode)
        self.data['total_rooms'] = self.data['total_rooms'].str.replace(
            'bdwn tq', '0')
        self.data['total_rooms'] = self.data['total_rooms'].str.replace(
            '+4', '5')
        self.data["total_rooms"] = self.data["total_rooms"].astype('float')

    def add_special_facilities(self):
        special_words = {
            'pool': 'استخر',
            'roof_garden': 'روف گاردن',
            'lobby': 'لابی',
            'lobby_man': 'لابی من',
            'balcony_d': 'بالکن',
            'sauna': 'سونا',
            'jacuzzi': 'جکوزی',
            'gym': 'باشگاه',
            'central_Vacuume_cleaner': 'جاروبرقی مرکزی',
            'janitor': 'سرایدار',
            'Guard': 'نگهبان',
            'master_room': 'مستر',
            'conference_hall': 'سالن اجتماعات',
            'parking_d': 'پارکینگ',
            'elevator_d': 'آسانسور',
            'warehouse_d': 'انباری'
        }

        for facility, word in special_words.items():
            self.data[facility] = self.data[['description1', 'description2', 'description3', 'title']].apply(
                lambda row: row.astype(str).str.contains(word, regex=True).any(), axis=1).astype(int)
    

    def cat_to_binary(self):
        column_objects = ['elevator', 'parking', 'warehouse']
        for item in column_objects:
            self.data[item] = self.data[item].apply(lambda x: 1 if x else 0)


    
    def fill_null(self):
        def row_mapping_function(row):   
            if row.parking == 0:
                if row.has_parking == 1:
                    row.parking = 1
                elif row.parking_d == 1:
                    row.parking = 1

            if row.elevator == 0:
                if row.has_elevator == 1:
                    row.elevator = 1
                elif row.elevator_d == 1:
                    row.elevator = 1

            if row.warehouse == 0:
                if row.has_warehouse == 1:
                    row.warehouse = 1
                elif row.warehouse_d == 1:
                    row.warehouse = 1

            if row.has_balcony == 0:
                if row.balcony_d == 1:
                    row.has_balcony = 1
                    
            return row
        
        self.data['has_balcony'].fillna(0, inplace=True)
        self.data = self.data.apply(row_mapping_function, axis=1)
    


    def drop_outliar(self):
        self.data.drop(
            self.data[self.data['price_per_meter'] < 2e7].index, inplace=True)
        self.data.drop(
            self.data[self.data['price_per_meter'] > 0.6e9].index, inplace=True)


        self.data.drop(
            self.data[self.data['real_estate_area'] <= 20].index, inplace=True)
        self.data.drop(
            self.data[self.data['real_estate_area'] > 1000].index, inplace=True)


        self.data.drop(self.data[(self.data['total_rooms'] > 1) & (self.data['real_estate_area'] < 50)].index, inplace=True)
        self.data.drop(self.data[(self.data['total_rooms'] > 2) & (self.data['real_estate_area'] < 80) & (self.data['real_estate_area'] >= 50)].index, inplace=True)
        self.data.drop(self.data[(self.data['total_rooms'] > 3) & (self.data['real_estate_area'] < 120) & (self.data['real_estate_area'] >= 80)].index, inplace=True)
        self.data.drop(self.data[(self.data['total_rooms'] > 5) & (self.data['real_estate_area'] < 200) & (self.data['real_estate_area'] >= 120)].index, inplace=True)

    def change_dtypy(self):
        self.data['balcony'] = self.data['balcony'].astype('int8')
        columns_int64 = self.data.select_dtypes('int64').columns
        for item in columns_int64:
            self.data[item] = self.data[item].astype('int8')

    def clean_columns(self):
        self.data.drop(columns=['has_elevator', 'no_elevator', 'elevator_d', 'has_warehouse', 'no_warehouse',  'warehouse_d', 'has_parking',
                'no_parking','parking_d', 'no_balcony',    'balcony_d', 'facilities', 'real_estate_type', 'title', 'description1', 'description2', 'description3'], inplace=True)
        self.data.rename(columns={"has_balcony": "balcony"}, inplace=True)

    def clean_index(self):
        self.data.reset_index(inplace=True)
        self.data.drop('index', inplace=True, axis=1)

    def clean_data(self):
        self.clean_facilities()
        self.one_hot_encode_facilities()
        self.clean_prices()
        self.clean_floor()
        self.clean_real_estate_area()
        self.clean_real_estate_age()
        self.clean_total_rooms()
        self.add_special_facilities()
        self.cat_to_binary()
        self.fill_null()
        self.clean_columns()
        self.clean_index()
        self.drop_outliar()
        self.change_dtypy()

    def save_cleaned_data(self, data_path):
        self.data.to_csv(data_path, index=False)


if __name__ == "__main__":
    mre_cleaner = DivarDataCleaner("../data/divar.csv")
    mre_cleaner.clean_data()
    mre_cleaner.save_cleaned_data("../data/divar_cleaned.csv")