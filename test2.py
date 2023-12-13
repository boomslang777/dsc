import re
import requests

# Function to send data to the specified webhook
def send_to_webhook(webhook_url, ticker, action, sentiment):
    # Construct the JSON payload based on the provided data and source
    if "ngrok" in webhook_url:
        payload = construct_ngrok_payload(ticker, action)
    else:
        payload = construct_original_payload(ticker, action)

    # Send the POST request to the specified webhook
    response = requests.post(webhook_url, json=payload)

    # Print the response
    print(f"Response from Webhook ({webhook_url}): {response.status_code} - {response.text}")

# Function to construct payload for ngrok webhook
def construct_ngrok_payload(ticker, action):
    account = "Sim101"
    qty = "1"

    if "buy" in action:
        alert = "Market Long"
    elif "sell" in action:
        alert = "Market Short"
    else:
        alert = "Unknown Alert"

    return {
        "alert": alert,
        "account": account,
        "ticker": ticker,
        "qty": qty
    }

# Function to construct payload for original webhook
def construct_original_payload(ticker, action):
    # Adjust this function based on the actual structure required by the original webhook
    # This is just a placeholder implementation
    return {
        "ticker": f"{'ES1' if ticker.startswith('ES') else 'NQ1'}!",
        "action": action,
        "sentiment": "bullish" if 'buy' in action else "bearish" if 'sell' in action else "flat"
    }

# Function to process incoming messages
def process_message(source, message):
    webhook_url = webhook_mapping.get(source)

    if webhook_url:
        match = re.match(r'([A-Z]+) ([A-Z]+[0-9]+) @ (\d+) @.*(?: SL@(\d+))?(?: PT@(\d+)/(\d+)/(\d+))?', message)
        if match:
            action, contract, price, stop_loss, pt1, pt2, pt3 = match.groups()

            # Map the action to a valid Traderspost action
            mapped_action = action_mapping.get(action, action.lower())

            print(f"Source: {source}")
            print(f"Action: {mapped_action}")
            print(f"Contract: {contract}")
            print(f"Price: {price}")

            if stop_loss:
                print(f"Stop Loss: {stop_loss}")

            if pt1:
                print(f"Profit Targets: {pt1}/{pt2}/{pt3}")

            # Send data to the specified webhook
            send_to_webhook(webhook_url, contract, mapped_action, "bullish" if 'buy' in mapped_action else "bearish" if 'sell' in mapped_action else "flat")

            print("------")
    else:
        print(f"Unknown source: {source}")

# Map sources to webhook URLs
webhook_mapping = {
    "cedar": 'https://webhooks.traderspost.io/trading/webhook/7d9a4163-1f5e-4ab6-badd-f8e0648c15bd/42f31636b7b9a7f0cad3c494ecd135a5',
    "shadow": 'https://awake-whippet-many.ngrok-free.app',
    "ocean": 'https://webhooks.traderspost.io/trading/webhook/7d9a4163-1f5e-4ab6-badd-f8e0648c15bd/42f31636b7b9a7f0cad3c494ecd135a5'
}

# Map the actions from your messages to valid Traderspost actions
action_mapping = {
    "BTO": "buy",
    "STC": "sell",
    "STO": "sell",
    "BTC": "buy"
}

# Example usage of the process_message function
# process_message("cedar", "BTO NQZ3 @ 15775 @Cedar Alert SL@15770 PT@15775/15780/15785")
# process_message("shadow", "STC NQZ3 @ 15770 @Shadow Alert")
# process_message("ocean", "STO NQZ3 @ 15785 @Ocean Alert SL@17590 PT@1775/1770/1765")
