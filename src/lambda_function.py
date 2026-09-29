import json
import time
import uuid
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB OUTSIDE the handler so Provisioned Concurrency pre-warms it!
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PaymentTransactions')

def lambda_handler(event, context):
    start_time = time.time()
    
    try:
        # Parse incoming JSON payment payload
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event
        
        transaction_id = body.get('transaction_id', f"txn_{uuid.uuid4().hex[:8]}")
        merchant_id = body.get('merchant_id', 'merch_default')
        amount = float(body.get('amount', 0.0))
        currency = body.get('currency', 'USD')
        card_token = body.get('card_token', '')

        # 1. Basic validation
        if amount <= 0 or not card_token:
            return _build_response(400, {
                "status": "DECLINED",
                "reason": "Invalid amount or missing card_token",
                "transaction_id": transaction_id
            })

        # 2. Fast Idempotency & State Write in DynamoDB (<10ms)
        auth_code = f"AUTH_{uuid.uuid4().hex[:6].upper()}"
        table.put_item(
            Item={
                'transaction_id': transaction_id,
                'merchant_id': merchant_id,
                'amount': str(amount),
                'currency': currency,
                'status': 'APPROVED',
                'auth_code': auth_code,
                'timestamp': int(time.time() * 1000)
            },
            ConditionExpression='attribute_not_exists(transaction_id)'
        )

        exec_ms = round((time.time() - start_time) * 1000, 2)
        return _build_response(200, {
            "status": "APPROVED",
            "transaction_id": transaction_id,
            "authorization_code": auth_code,
            "execution_time_ms": exec_ms
        })

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return _build_response(409, {
                "status": "DUPLICATE_TRANSACTION",
                "transaction_id": transaction_id
            })
        return _build_response(500, {"error": str(e)})
    except Exception as e:
        return _build_response(500, {"error": str(e)})

def _build_response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body_dict)
    }
