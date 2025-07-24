

def api_obj_config(api):
    data = {
        "FetchStockData": {
            "parent_method": api._yfinance.fetch,
            "kwargs": {
                "attribute": "stock"
            }
        },
        "SendDataBricksJob": {
            "parent_method": api._databricks.send_job,
            "kwargs": {
                "attribute": "job"
            }
        }, 
        "DownloadStockData": {
            "parent_method": api._yfinance.download,
            "kwargs": {
                "attribute": "stocks"
            }
        }
    }
    return data