import React from 'react';
import ProductItem from './ProductItem'; // Assuming path is correct

const ProductList = ({ products, onAddToCart }) => {
    if (!products || products.length === 0) {
        return <p className="text-gray-500">No products available at the moment.</p>;
    }

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {products.map((product) => (
                <ProductItem key={product.id} product={product} onAddToCart={onAddToCart} />
            ))}
        </div>
    );
};

export default ProductList;
