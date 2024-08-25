import pandas as pd
import joblib

def predict_mos(model_file, scaler_file, new_feature_file, output_file):
    svr_model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)

    new_features = pd.read_csv(new_feature_file, index_col=0, keep_default_na=False)
    new_features_scaled = scaler.transform(new_features)

    predicted_scores = svr_model.predict(new_features_scaled)
    predicted_scores = predicted_scores * 10

    result_df = pd.DataFrame(predicted_scores, index=new_features.index, columns=['Predicted_MOS'])
    result_df.to_csv(output_file)
    print(f'Predicted MOS scores saved to {output_file}')

def append_predictions_to_excel(predictions_file, excel_file, column_name):
    predicted_df = pd.read_csv(predictions_file, index_col=0)
    
    try:
        excel_df = pd.read_excel(excel_file, index_col=0)
    except FileNotFoundError:
        excel_df = pd.DataFrame()

    excel_df[column_name] = predicted_df['Predicted_MOS']
    excel_df.to_excel(excel_file)
    print(f'Appended predictions to {excel_file}')

def test_model(column_name):
    model_file = 'point_cloud_metrics/svr_model.joblib'
    scaler_file = 'point_cloud_metrics/scaler.joblib'
    new_feature_file = 'point_cloud_metrics/features.csv'
    output_file = 'point_cloud_metrics/predicted_mos.csv'
    excel_file = 'point_cloud_metrics/predictions.xlsx'

    predict_mos(model_file, scaler_file, new_feature_file, output_file)
    append_predictions_to_excel(output_file, excel_file, column_name)

if __name__ == '__main__':
    test_model("default_run")

