# FinDash README

## 🌟 Highlights
This repo contains the core framework for the FinDash app. Some of those core functionalities are: 
- SQL read and write methods
- S3 download and upload capabilities
- Asset price fetching and downloading
- Asset news fetching
- Databricks job sending for ETL

## Overview
FinDash is a framework written to store core functions of the project FinDash. For context, the project is a financial dashboard app that allows users to register, login, visualize asset prices with different visualizations (e.g. line graph, candlestock, etc), see a list of recent asset news, and do some basic predictions for the assets based on ARIMA, LSTM, and Regression models. 
### Author
I'm Joseph Schambach. I work as a software engineer for a start up that automates billing and intake processes for companies in the healthcare industry. I am building this project to showcase what I've learned about software, data engineering, and ML development. 

## Usage Instructions
This package is designed to be developer friendly. Once the context is initialized, using Pydantic models and class methods, the developer can trigger different types of events with a single line of code.
**Initializing Context**
```
from context.findash_context import FinDashContext

context = FinDashContext()
```
**Fetching Asset Price Data**
```
from models.yfinance_models import FetchAssetData, Asset

data = context.api.fetch(FetchAssetData(asset=Asset(asset='AAPL', period='1d', interval='1d'))
```
**Downloading Asset Price Data for Multiple Assets**
```
from models.yfinance_models import DownloadAssetData

data = context.api.fetch(DownloadAssetData(assets=['AAPL', 'MSFT', 'GOOG'], period='5d', interval='1d')
```
**Trigger Databricks Job Run**
```
from models.databricks_models import SendDataBricksJob, DatabricksJob

context.api.send(SendDataBricksJob(job=DatabricksJob(job_id=1234567))
```
The package uses YFinance for data fetching, which means it uses the same inputs for intervals and periods. 
- Intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
- Periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

Assets are any valid ticker that YFinance stores. This can be stocks, ETFs, and crypto currencies. 


