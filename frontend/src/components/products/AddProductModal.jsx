
import { useState, useEffect } from "react";
import {
  addProduct,
  updateProduct,
} from "../../services/productService";
const AddProductModal = ({
  isOpen,
  onClose,
  onProductAdded,
  editProduct,
}) => {
  const [formData, setFormData] = useState({
    product_id: "",
    category: "",
    original_price: "",
    discount: "",
    final_price: "",
    payment_method: "",
    purchase_date: "",
  });

  useEffect(() => {
  if (editProduct) {
    setFormData({
      product_id: editProduct.product_id,
      category: editProduct.category,
      original_price: editProduct.original_price,
      discount: editProduct.discount,
      final_price: editProduct.final_price,
      payment_method: editProduct.payment_method,
      purchase_date: editProduct.purchase_date,
    });
  } else {
    setFormData({
      product_id: "",
      category: "",
      original_price: "",
      discount: "",
      final_price: "",
      payment_method: "",
      purchase_date: "",
    });
  }
}, [editProduct]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editProduct) {
  await updateProduct(editProduct.id, formData);
  alert("Product updated successfully!");
} else {
  await addProduct(formData);
  alert("Product added successfully!");
}

      setFormData({
        product_id: "",
        category: "",
        original_price: "",
        discount: "",
        final_price: "",
        payment_method: "",
        purchase_date: "",
      });

      onProductAdded();
      onClose();
    } catch (err) {
      console.error(err);
      alert("Failed to save product");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center">
      <div className="bg-white rounded-lg shadow-lg p-6 w-[500px]">
        <h2 className="text-2xl font-bold mb-5">
  {editProduct ? "Edit Product" : "Add Product"}
</h2>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="number"
            name="product_id"
            placeholder="Product ID"
            value={formData.product_id}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <input
            type="text"
            name="category"
            placeholder="Category"
            value={formData.category}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <input
            type="number"
            name="original_price"
            placeholder="Original Price"
            value={formData.original_price}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <input
            type="number"
            name="discount"
            placeholder="Discount"
            value={formData.discount}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <input
            type="number"
            name="final_price"
            placeholder="Final Price"
            value={formData.final_price}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <input
            type="text"
            name="payment_method"
            placeholder="Payment Method"
            value={formData.payment_method}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <input
            type="date"
            name="purchase_date"
            value={formData.purchase_date}
            onChange={handleChange}
            className="border w-full p-2 rounded"
            required
          />

          <div className="flex justify-end gap-3 pt-3">

            <button
              type="button"
              onClick={onClose}
              className="bg-gray-500 text-white px-4 py-2 rounded"
            >
              Cancel
            </button>

            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              {editProduct ? "Update Product" : "Save Product"}
            </button>

          </div>
        </form>
      </div>
    </div>
  );
};

export default AddProductModal;