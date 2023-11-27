import pandas as pd

class MrestateDataCleaner:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        index_estate_type = self.data[(self.data['real_estate_type'] == 'آپارتمان') | (
            self.data['real_estate_type'] == 'برج')].index
        self.data = self.data.loc[index_estate_type, :]


    def clean_prices(self):
        self.data.drop(self.data[self.data["price"] == 'توافقی'].index, inplace=True)
        self.data.reset_index(drop=True, inplace=True)
        self.data["price"] = self.data["price"].astype(float)

    def calculate_price_per_meter(self):
        self.data['price_per_meter'] = self.data["price"]/self.data['real_estate_area']
        self.data.price_per_meter = ((self.data.price_per_meter / 1000).round())*1000



    def one_hot_encode_facilities(self):
        exploded_mre = self.data['facilities'].str.split(',').explode()
        mre_get_dummy = pd.get_dummies(exploded_mre)
        mre_result = mre_get_dummy.groupby(mre_get_dummy.index).sum()
        mre_result.reset_index(drop=True, inplace=True)
        self.data = self.data.merge(mre_result, on=self.data.index.values)
        self.data.drop('key_0', axis=1, inplace=True)

    def drop_outliar(self):
        self.data.drop(
            self.data[self.data['price_per_meter'] < 2e7].index, inplace=True)
        self.data.drop(
            self.data[self.data['price_per_meter'] > 0.6e9].index, inplace=True)

        index_age_year = self.data['real_estate_age'][self.data['real_estate_age'] > 1300].index
        index_age_neg = self.data['real_estate_age'][self.data['real_estate_age'] < 0].index
        self.data.loc[index_age_year, 'real_estate_age'] = self.data.loc[index_age_year,
                                                                                'real_estate_age'].apply(lambda x: 1402-x)
        self.data.loc[index_age_neg, 'real_estate_age'] = self.data.loc[index_age_neg,
                                                                                'real_estate_age'].apply(lambda x: -x)

        self.data.drop(
            self.data[self.data['real_estate_area'] <= 20].index, inplace=True)

        self.data.drop(
            self.data[self.data['real_estate_area'] > 1000].index, inplace=True)

        self.data.drop(self.data[(self.data['total_rooms'] > 1) & (
            self.data['real_estate_area'] < 50)].index, inplace=True)
        self.data.drop(self.data[(self.data['total_rooms'] > 2) & (
            self.data['real_estate_area'] < 80) & (self.data['real_estate_area'] >= 50)].index, inplace=True)
        self.data.drop(self.data[(self.data['total_rooms'] > 3) & (
            self.data['real_estate_area'] < 120) & (self.data['real_estate_area'] >= 80)].index, inplace=True)
        self.data.drop(self.data[(self.data['total_rooms'] > 5) & (
            self.data['real_estate_area'] < 200) & (self.data['real_estate_area'] >= 120)].index, inplace=True)
        

    def drop_null(self):
        self.data.drop(
            self.data[self.data['real_estate_age'].isna()].index, inplace=True)
        
        self.data.drop(
            self.data[self.data['floor'].isna()].index, inplace=True)
        
        self.data.drop(
            self.data[self.data['real_estate_area'].isna()].index, inplace=True)

     

    def convert_parking_to_binary(self):
        self.data["parking"] = self.data.number_of_parking.apply(lambda x: 1 if x > 0 else 0)

    def clean_columns(self):
        self.data.rename(columns={"استخر": "pool",
                                    "اتاق مستر": "master_room",
                                    "آسانسور": "elevator",
                                    "بالکن": "balcony",
                                    "باشگاه": "gym",
                                    "انباری": "warehouse",
                                    "سرایداری": "janitor",
                                    "سالن اجتماعات": "conference_hall",
                                    "روف گاردن": "roof_garden",
                                    "جکوزی": "jacuzzi",
                                    "جاروبرقی مرکزی": "central_Vacuume_cleaner",
                                    "نگهبانی": "Guard",
                                    "لابی": "lobby",
                                    "لابی من": "lobby_man",
                                    "سونا": "sauna",
                                    "price_per_meter": "price_per_meter"},
                            inplace=True)
        
        self.data.drop(columns=["آبنما", "آلاچیق", "اعلام حریق", "اطفا حریق",
                            "نورپردازی", "پاسیو", "پارکینگ مهمان", "number_of_parking", "facilities", "real_estate_type"], inplace=True)


        column_list = ['district_name', 'real_estate_area', 'real_estate_age', 'total_rooms',
                    'price', 'price_per_meter', 'floor', 'elevator', 'parking', 'warehouse',
                    'balcony', 'pool', 'roof_garden', 'lobby', 'lobby_man', 'sauna',
                    'jacuzzi', 'gym', 'central_Vacuume_cleaner', 'janitor', 'Guard',
                    'master_room', 'conference_hall']

        self.data = self.data[column_list]


    def clean_data(self):
        self.clean_prices()
        self.calculate_price_per_meter()
        self.one_hot_encode_facilities()
        self.drop_outliar()
        self.drop_null()
        self.convert_parking_to_binary()
        self.clean_columns()

    
    def save_cleaned_data(self, data_path):
        self.data.to_csv(data_path, index=False)


if __name__ == "__main__":
    mre_cleaner = MrestateDataCleaner("../data/mrestate.csv")
    mre_cleaner.clean_data()
    mre_cleaner.save_cleaned_data("../data/mrestate_cleaned.csv")