import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from web3 import Web3
import sys

# 1. Configuration
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0xDFb2618DaAf55DD95638924cfA5f18698C653c83"

# Your Actual ABI
ABI = [
    {"inputs": [], "name": "batchCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_batchId", "type": "uint256"}], "name": "getBatch", "outputs": [{"components": [{"name": "timestamp", "type": "uint256"}, {"name": "moisture", "type": "uint256"}, {"name": "nitrogen", "type": "uint256"}, {"name": "phosphorus", "type": "uint256"}, {"name": "potassium", "type": "uint256"}, {"name": "status", "type": "string"}], "type": "tuple"}], "stateMutability": "view", "type": "function"}
]

# 2. Connect to Blockchain
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    print("❌ Error: Could not connect to Ganache. Is it running?")
    sys.exit()

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def fetch_blockchain_data():
    try:
        # FIX: Use batchCount() instead of getHistoryCount()
        total_records = contract.functions.batchCount().call()
        print(f"📊 Blockchain Sync: Found {total_records} records.") 
        
        if total_records < 2:
            print("⚠️ Not enough data to train AI (need at least 2 entries).")
            return pd.DataFrame()

        data = []
        # FIX: Loops from 1 to total_records (inclusive) because Solidity starts at 1
        for i in range(1, total_records + 1):
            # FIX: Use getBatch(i) instead of history(i)
            entry = contract.functions.getBatch(i).call()
            
            # entry structure based on your ABI:
            # entry[0] = timestamp, entry[1] = moisture, entry[2] = nitrogen (temp)
            data.append({
                'moisture': entry[1],
                'temp': entry[2],
                'yield': (entry[1] * 1.5) + (entry[2] * 0.5)  # Simulated logic
            })
        return pd.DataFrame(data)
    except Exception as e:
        print(f"❌ Blockchain Read Error: {e}")
        return pd.DataFrame()

def predict_yield(current_moisture, current_temp):
    df = fetch_blockchain_data()
    
    if df.empty:
        return "N/A (Insufficient Data)"
    
    # Train the model
    X = df[['moisture', 'temp']]
    y = df['yield']
    
    # Simple ML Model
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    
    # Make Prediction
    prediction = model.predict([[current_moisture, current_temp]])
    return round(prediction[0], 2)

# --- EXECUTION ---
if __name__ == "__main__":
    # Test with current sensor values
    test_moisture = 45
    test_temp = 28
    
    print("⏳ Running AgroChain AI Predictor...")
    result = predict_yield(test_moisture, test_temp)
    
    if result != "N/A (Insufficient Data)":
        print("-" * 30)
        print(f"✅ Prediction Successful!")
        print(f"Input Moisture: {test_moisture}%")
        print(f"Input Temp: {test_temp}°C")
        print(f"🚀 PREDICTED HARVEST YIELD: {result} kg/acre")
        print("-" * 30)
    else:
        print(result)