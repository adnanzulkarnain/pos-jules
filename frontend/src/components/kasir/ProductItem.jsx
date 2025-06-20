// frontend/src/components/kasir/ProductItem.jsx
import React from 'react';

const ProductItem = ({ product, onAddToCart }) => {
    return (
        <div className="border p-4 rounded-lg shadow hover:shadow-xl transition-shadow duration-200 ease-in-out flex flex-col justify-between">
            <div> {/* Added a div to group content and allow button to be at bottom */}
                <h2 className="text-lg font-semibold mb-1">{product?.nama || 'Product Name'}</h2>
                <p className="text-gray-700 mb-1">Rp {product?.harga?.toLocaleString() || '0'}</p>
                <p className="text-sm text-gray-500">Stok: {product?.stok || '0'}</p>
            </div>
            <button
                onClick={() => onAddToCart ? onAddToCart(product) : null}
                className="mt-3 w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md transition duration-150 ease-in-out"
            >
                Add to Cart
            </button>
        </div>
    );
};

export default ProductItem;
