import React, { useState, useEffect } from 'react';
import ProductList from '../components/kasir/ProductList';
import ShoppingCart from '../components/kasir/ShoppingCart';

const KasirPage = () => {
    const [products, setProducts] = useState([]);
    const [cartItems, setCartItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false); // For loading state during submission

    const fetchProducts = async () => { // Moved fetchProducts out to be callable
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/products');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setProducts(data);
            setError(null);
        } catch (e) {
            setError(e.message);
            setProducts([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProducts();
    }, []);

    const handleAddToCart = (productToAdd) => {
        if (productToAdd.stok <= 0) {
            alert(`${productToAdd.nama} is out of stock!`);
            return;
        }

        setCartItems(prevItems => {
            const existingItem = prevItems.find(item => item.product.id === productToAdd.id);
            if (existingItem) {
                if (existingItem.qty < productToAdd.stok) {
                    return prevItems.map(item =>
                        item.product.id === productToAdd.id
                            ? { ...item, qty: item.qty + 1 }
                            : item
                    );
                } else {
                    alert(`Cannot add more ${productToAdd.nama}. Stock limit reached.`);
                    return prevItems;
                }
            } else {
                return [...prevItems, { product: productToAdd, qty: 1 }];
            }
        });
    };

    const handleRemoveFromCart = (productIdToRemove) => {
        setCartItems(prevItems => prevItems.filter(item => item.product.id !== productIdToRemove));
    };

    const handleUpdateQuantity = (productIdToUpdate, newQuantity) => {
        setCartItems(prevItems => {
            const itemToUpdate = prevItems.find(item => item.product.id === productIdToUpdate);
            if (!itemToUpdate) return prevItems;

            if (newQuantity <= 0) {
                return prevItems.filter(item => item.product.id !== productIdToUpdate);
            }

            if (newQuantity > itemToUpdate.product.stok) {
                alert(`Cannot set quantity for ${itemToUpdate.product.nama} beyond stock limit (${itemToUpdate.product.stok}).`);
                return prevItems;
            }

            return prevItems.map(item =>
                item.product.id === productIdToUpdate
                    ? { ...item, qty: newQuantity }
                    : item
            );
        });
    };

    const handleCheckout = async () => {
        if (cartItems.length === 0) {
            alert("Keranjang belanja kosong!");
            return;
        }

        setIsSubmitting(true);

        const transactionPayload = {
            kasir_id: 1, // Hardcoded for now
            items: cartItems.map(item => ({
                produk_id: item.product.id,
                qty: item.qty,
            })),
        };

        try {
            const response = await fetch('http://localhost:8000/transactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(transactionPayload),
            });

            if (response.ok) {
                alert('Transaksi berhasil!');
                setCartItems([]);
                fetchProducts(); // Re-fetch products to update stock display
            } else {
                let errorDetail = `HTTP error! status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorDetail = errorData.detail || errorDetail;
                } catch (jsonError) {
                    console.error("Could not parse error JSON:", jsonError);
                }
                alert(`Transaksi gagal: ${errorDetail}`);
            }
        } catch (error) {
            console.error("Checkout error:", error);
            alert(`Transaksi gagal: Terjadi kesalahan jaringan atau server tidak merespon. ${error.message}`);
        } finally {
            setIsSubmitting(false);
        }
    };

    if (loading && products.length === 0) return <p className="text-center mt-8">Loading products...</p>;
    if (error) return <p className="text-center mt-8 text-red-500">Error fetching products: {error}</p>;

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-8 text-center text-gray-700">Halaman Kasir</h1>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-2xl font-semibold mb-5 text-gray-600 border-b pb-2">Daftar Produk</h2>
                    {loading && products.length > 0 && <p>Refreshing products...</p>}
                    <ProductList products={products} onAddToCart={handleAddToCart} />
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md">
                     <ShoppingCart
                        cartItems={cartItems}
                        onUpdateQuantity={handleUpdateQuantity}
                        onRemoveFromCart={handleRemoveFromCart}
                        onCheckout={handleCheckout}
                        isSubmitting={isSubmitting} // Pass submitting state
                     />
                </div>
            </div>
        </div>
    );
};
export default KasirPage;
