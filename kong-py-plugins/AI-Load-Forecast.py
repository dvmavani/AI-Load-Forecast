import numpy as np
from sklearn.linear_model import LinearRegression
import kong_pdk.pdk.kong as kong
import pandas as pd
import json
from datetime import datetime

Schema = (
    {"Log_File_Path": {"type": "string"}},
)

version = '0.1.0'
priority = 30

# Plugin code

class Plugin(object):
    def __init__(self, config):
        self.config = config

    def access(self, kong: kong.kong):
        kong.log("########################## Inside Access Phase ######################################")

        # Extract log file path and service ID
        directory_path = self.config['Log_File_Path']
        service_id = kong.request.get_header("ServiceID")
        # Process logs
        try:
            with open(directory_path, 'r', encoding='utf-8', errors='ignore') as file:
                logs = [json.loads(line) for line in file.readlines()]

            # Filter logs by service ID
            filtered_logs = [log for log in logs if log['service']['id'] == service_id]

            # Extract relevant information
            data = []
            for log in filtered_logs:
                timestamp = datetime.fromtimestamp(log['started_at'] / 1000)  # Convert milliseconds to seconds
                second_timestamp = timestamp.replace(microsecond=0)  # Remove microseconds
                proxy_latency = log['latencies']['proxy']
                data.append((second_timestamp, proxy_latency))

            # Create DataFrame
            df = pd.DataFrame(data, columns=['timestamp', 'proxy_latency'])

            # Group by second and calculate metrics
            resulted_df = df.groupby('timestamp').agg(
                requests_per_second=('proxy_latency', 'count'),
                average_proxy_latency=('proxy_latency', 'mean')
            ).reset_index()

            # Model fitting
            X = resulted_df[['requests_per_second']].values  # Features (needs to be 2D array)
            y = resulted_df['average_proxy_latency'].values  # Target
            model = LinearRegression()
            model.fit(X, y)
            kong.log("########################## Model fitting is successful ##########################")

            # Get headers
            headerForRPS = kong.request.get_header("Ideal-RequestPerSecond")
            headerForLatency = kong.request.get_header("Ideal-Latency")

            # Perform predictions based on headers
            response = ""
            if headerForRPS is not None:
                kong.log("########################## Predicting Latency for given RPS ##########################")
                target_rps = float(headerForRPS)
                predicted_latency = model.predict([[target_rps]])[0]
                response = f"Predicted average latency when Request Per Second {target_rps} is : {predicted_latency}"
            elif headerForLatency is not None:
                kong.log("########################## Predicting RPS for given Latency ##########################")
                target_latency = float(headerForLatency)
                predicted_rps = (target_latency - model.intercept_) / model.coef_[0]
                response = f"Predicted Request Per Second when average latency is {target_latency}: {predicted_rps}"
            else:
                response = "Error: Header is missing for prediction."
        except Exception as e:
            response = f"Error processing logs: {str(e)}"

        kong.log(response)
        return kong.response.exit(200, {"message": response})

# Add below section to allow this plugin optionally be running in a dedicated process
if __name__ == "__main__":
    from kong_pdk.cli import start_dedicated_server
    start_dedicated_server("AI-Powered-Analytics", Plugin, version, priority, Schema)
