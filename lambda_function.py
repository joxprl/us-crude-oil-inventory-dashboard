import json
import os
import urllib.request
import boto3

S3_BUCKET_NAME = os.environ.get('BUCKET_NAME')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
EIA_API_KEY = os.environ.get('EIA_API_KEY')

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    url = (
        f"https://api.eia.gov/v2/petroleum/stoc/wstk/data/"
        f"?api_key={EIA_API_KEY}"
        f"&frequency=weekly"
        f"&data[0]=value"
        f"&facets[series][]=WCESTUS1"
        f"&sort[0][column]=period"
        f"&sort[0][direction]=desc"
        f"&length=2"
    )
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        records = result.get('response', {}).get('data', [])
        if len(records) < 2:
            return {'statusCode': 400, 'body': json.dumps('Insufficient data from EIA API.')}
            
        latest = records[0]
        previous = records[1]
        
        period = latest.get('period')
        current_stock = float(latest.get('value'))
        prev_stock = float(previous.get('value'))
        
        diff_thousand = current_stock - prev_stock
        diff_million = diff_thousand / 1000.0
        
        if diff_thousand < 0:
            status_en = "📉 Inventory Draw (Supply Decreased - Bullish for Oil Prices)"
            status_ar = "📉 سحب من المخزون (نقص المعروض - داعم لارتفاع الأسعار)"
            sign = ""
        elif diff_thousand > 0:
            status_en = "📈 Inventory Build (Supply Increased - Bearish for Oil Prices)"
            status_ar = "📈 زيادة في المخزون (فائض في المعروض - ضاغط لانخفاض الأسعار)"
            sign = "+"
        else:
            status_en = "⚖️ No Change (Neutral)"
            status_ar = "⚖️ استقرار في المخزون"
            sign = ""

        email_subject = f"US Crude Oil Inventory Report ({period}) - تقرير مخزونات النفط"
        
        email_message = f"""
[English]
Weekly US Commercial Crude Oil Inventory Report (EIA)
--------------------------------------------------
📅 Week Ending: {period}
🛢️ Current Inventory: {current_stock:,.0f} Thousand Barrels
🛢️ Previous Week: {prev_stock:,.0f} Thousand Barrels
📊 Weekly Change: {sign}{diff_million:.2f} Million Barrels ({sign}{diff_thousand:,.0f}k bbl)
Market Impact: {status_en}
Saved to S3: {S3_BUCKET_NAME}

--------------------------------------------------
[العربية]
التقرير الأسبوعي لمخزونات النفط الخام الأمريكية (EIA)
--------------------------------------------------
📅 نهاية الأسبوع: {period}
🛢️ المخزون الحالي: {current_stock:,.0f} ألف برميل
🛢️ الأسبوع السابق: {prev_stock:,.0f} ألف برميل
📊 التغير الأسبوعي: {sign}{diff_million:.2f} مليون برميل ({sign}{diff_thousand:,.0f} ألف برميل)
الأثر على السوق: {status_ar}
تم الحفظ في S3: {S3_BUCKET_NAME}

--------------------------------------------------
Automated Energy Data Pipeline - Prepared by Ahmed Mubarak
        """
        
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=email_subject,
            Message=email_message
        )
        
        csv_content = f"Period,Current_Stock_k_bbl,Previous_Stock_k_bbl,Change_Million_bbl\n{period},{current_stock},{prev_stock},{diff_million:.2f}"
        file_name = f"us_oil_inventory_{period}.csv"
        
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"weekly-inventory/{file_name}",
            Body=csv_content,
            ContentType='text/csv'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed inventory report for {period}!')
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error: {str(e)}")}
