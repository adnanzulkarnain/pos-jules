import React from 'react';

const ShoppingCart = ({ cartItems, onUpdateQuantity, onRemoveFromCart, onCheckout, isSubmitting }) => {
    const calculateTotal = () => {
        return cartItems && cartItems.length > 0
               ? cartItems.reduce((acc, item) => acc + (item.product.harga * item.qty), 0)
               : 0;
    };

    const handleQuantityChange = (productId, currentQty, delta) => {
        const newQuantity = currentQty + delta;
        // onUpdateQuantity will handle newQuantity <= 0 by removing item
        // and also check against stock.
        onUpdateQuantity(productId, newQuantity);
    };

    // Direct input change handler
    const handleDirectQuantityInput = (productId, event) => {
        const newQuantity = parseInt(event.target.value, 10);
        if (isNaN(newQuantity)) {
            // Or handle more gracefully, e.g., set to 1 or previous value
            onUpdateQuantity(productId, 1);
            return;
        }
        onUpdateQuantity(productId, newQuantity);
    };

    return (
        <div className="border p-4 rounded-lg shadow-md bg-white">
            <h2 className="text-xl font-semibold mb-5 text-gray-600 border-b pb-2">Keranjang Belanja</h2>
            {(!cartItems || cartItems.length === 0) ? (
                <p className="text-gray-500">Keranjang kosong.</p>
            ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
                    {cartItems.map(item => (
                        <div key={item.product.id} className="flex justify-between items-center border-b pb-2">
                            <div>
                                <p className="font-medium text-gray-800">{item.product.nama}</p>
                                <p className="text-xs text-gray-500">
                                    Rp {item.product.harga.toLocaleString()} x {item.qty} = Rp {(item.product.harga * item.qty).toLocaleString()}
                                </p>
                            </div>
                            <div className="flex items-center space-x-2">
                                <button
                                    onClick={() => handleQuantityChange(item.product.id, item.qty, -1)}
                                    className="px-2 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                                >
                                    -
                                </button>
                                <input
                                    type="number"
                                    value={item.qty}
                                    onChange={(e) => handleDirectQuantityInput(item.product.id, e)}
                                    className="w-12 text-center border rounded p-1"
                                    min="1" // Let onUpdateQuantity handle 0 or less
                                    max={item.product.stok} // Visual cue, actual check in onUpdateQuantity
                                />
                                <button
                                    onClick={() => handleQuantityChange(item.product.id, item.qty, 1)}
                                    className="px-2 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                                >
                                    +
                                </button>
                                <button
                                    onClick={() => onRemoveFromCart(item.product.id)}
                                    className="ml-3 text-red-500 hover:text-red-700 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
            <div className="mt-6 pt-4 border-t">
                <h3 className="text-xl font-semibold text-gray-800 text-right">Total: Rp {calculateTotal().toLocaleString()}</h3>
                <button
                    onClick={onCheckout}
                    disabled={!cartItems || cartItems.length === 0 || isSubmitting}
                    className="mt-4 w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md shadow-sm disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                    {isSubmitting ? 'Memproses...' : 'Bayar'}
                </button>
            </div>
        </div>
    );
};

export default ShoppingCart;
