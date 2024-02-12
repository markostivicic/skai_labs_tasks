from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/unauthorized-sales', methods=['POST'])
def unauthorized_sales():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Check if the required fields are present in the JSON data
    if not data or 'productListings' not in data or 'salesTransactions' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Create a dictionary of product listings with product IDs as keys and authorized seller IDs as values
    product_listings = {product['productID']: product['authorizedSellerID'] for product in data['productListings']}
    unauthorized_sales = []

    # Iterate over sales transactions
    for sales in data['salesTransactions']:
        # Check if the seller ID matches the authorized seller ID for the product
        if sales['sellerID'] != product_listings.get(sales['productID']):
            # Check if the unauthorized sale is already recorded
            if {sales['sellerID']} not in unauthorized_sales:
                # If not recorded, add the unauthorized sale to the list
                unauthorized_sales.append({
                    "productID": sales['productID'],
                    "unauthorizedSellerID": [sales['sellerID']]
                })
            else:
                # If recorded, append the seller ID to the existing unauthorized sale entry
                unauthorized_sales[unauthorized_sales.index({"productID": sales['productID'], "unauthorizedSellerID": [sales['sellerID']]})]["unauthorizedSellerID"].append(sales['sellerID'])

    # Return JSON response with unauthorized sales information
    return jsonify({"unauthorizedSales": unauthorized_sales})

if __name__ == '__main__':
    app.run(debug=True)
