import { FaEdit, FaTrash } from "react-icons/fa";
import { useEffect, useState } from "react";
import { getProducts, deleteProduct } from "../../services/productService";
function ProductTable({ onEdit, searchTerm , selectedCategory }) {
  const [products, setProducts] = useState([]);
  const role = localStorage.getItem("role");
  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };
const handleDelete = async (id) => {
  const confirmDelete = window.confirm(
    "Are you sure you want to delete this product?"
  );

  if (!confirmDelete) return;

  try {
    await deleteProduct(id);
    alert("Product deleted successfully!");
    loadProducts(); // Refresh table
  } catch (error) {
    console.error("Error deleting product:", error);
    alert("Failed to delete product.");
  }
};

const filteredProducts = products.filter((product) => {
  const matchesSearch =
    product.product_id.toString().includes(searchTerm) ||
    product.category.toLowerCase().includes(searchTerm.toLowerCase());

  const matchesCategory =
    selectedCategory === "All" ||
    product.category === selectedCategory;

  return matchesSearch && matchesCategory;
});
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-100">
          <tr>
            <th className="text-left p-4">Product ID</th>
            <th className="text-left p-4">Category</th>
            <th className="text-left p-4">Original Price</th>
            <th className="text-left p-4">Discount</th>
            <th className="text-left p-4">Final Price</th>
            <th className="text-left p-4">Payment</th>
            <th className="text-left p-4">Purchase Date</th>
            {role === "admin" && (
  <th className="text-center p-4">Actions</th>
)}
          </tr>
        </thead>

        <tbody>
          {filteredProducts.map((product) => (
            <tr key={product.id} className="border-t hover:bg-gray-50">
              <td className="p-4">{product.product_id}</td>
              <td className="p-4">{product.category}</td>
              <td className="p-4">₹{product.original_price}</td>
              <td className="p-4">{product.discount}%</td>
              <td className="p-4">₹{product.final_price}</td>
              <td className="p-4">{product.payment_method}</td>
              <td className="p-4">{product.purchase_date}</td>
{role === "admin" && (
  <td className="p-4">
    <div className="flex justify-center gap-4">
      <button
        onClick={() => onEdit(product)}
        className="text-blue-600 hover:text-blue-800"
      >
        <FaEdit />
      </button>

      <button
        onClick={() => handleDelete(product.id)}
        className="text-red-600 hover:text-red-800"
      >
        <FaTrash />
      </button>
    </div>
  </td>
)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProductTable;